"""Implementation of session management."""

import ast
import itertools
from enum import Enum
from logging import getLogger
from typing import Any, Dict, List, Tuple, Union

import astor
import black

from ni_measurement_plugin_converter._constants import (
    ADD_SESSION,
    DEBUG_LOGGER,
    ENCODING,
    NI_DRIVERS,
    RESERVATION,
)
from ni_measurement_plugin_converter.models import PinInfo, RelayInfo, SessionMapping
from ni_measurement_plugin_converter._utils import get_function_node
from ni_measurement_plugin_converter._utils._manage_session_helper import (
    get_sessions_details,
    instrument_is_visa_type,
    ni_drivers_supported_instrument,
)

SESSION_CONSTRUCTOR = "session_constructor"
INSTRUMENT_TYPE = "instrument_type"
INVALID_DRIVERS = "Invalid/No driver used. Supported drivers: {supported_drivers}"
EXTRACT_DRIVER_SESSIONS = "Extracting driver sessions from measurement function..."
MIGRATED_FILE_MODIFIED = "Migrated file is modified."


class DriverSession(Enum):
    """Instrument drivers' session."""

    nidcpower = "nims.session_management.INSTRUMENT_TYPE_NI_DCPOWER"
    nidmm = "nims.session_management.INSTRUMENT_TYPE_NI_DMM"
    nidigital = "nims.session_management.INSTRUMENT_TYPE_NI_DIGITAL_PATTERN"
    nifgen = "nims.session_management.INSTRUMENT_TYPE_NI_FGEN"
    niscope = "nims.session_management.INSTRUMENT_TYPE_NI_SCOPE"
    niswitch = "nims.session_management.INSTRUMENT_TYPE_NI_RELAY_DRIVER"
    nidaqmx = "nims.session_management.INSTRUMENT_TYPE_NI_DAQMX"


def _add_params(function_node: ast.FunctionDef, params: List[str]) -> ast.FunctionDef:
    for param in params[::-1]:
        function_node.args.args.insert(0, param)

    return function_node


def _get_with_removed_function(function_node: ast.FunctionDef) -> List[Any]:
    body = []

    for child_node in function_node.body:
        if (
            isinstance(child_node, ast.With)
            and hasattr(child_node, "items")
            and child_node.items
            and _check_driver_session(child_node)
        ):
            body.extend(child_node.body)
        else:
            body.append(child_node)

    return body


def _check_driver_session(child_node: ast.With) -> bool:
    for item in child_node.items:
        if isinstance(item.context_expr, ast.Call):
            if ni_drivers_supported_instrument(item.context_expr) or instrument_is_visa_type(
                item.context_expr
            ):
                return True

    return False


def manage_session(migrated_file_dir: str, function: str) -> Dict[str, List[str]]:
    """Manage session.

    1. Get sessions details.
    2. Add session variables to migrated file.

    Args:
        migrated_file_dir (str): Migrated measurement file directory.
        function (str): Measurement function name.

    Returns:
        Dict[str, List[str]]: Drivers as keys and list of session variables as values.
    """
    logger = getLogger(DEBUG_LOGGER)

    measurement_function_node = get_function_node(file_dir=migrated_file_dir, function=function)

    logger.info(EXTRACT_DRIVER_SESSIONS)

    sessions_details = get_sessions_details(function_node=measurement_function_node)
    if not sessions_details:
        raise ValueError(INVALID_DRIVERS.format(supported_drivers=NI_DRIVERS + ["VISA"]))

    logger.info(ADD_SESSION)

    params_added_function = _add_params(
        function_node=measurement_function_node,
        params=list(itertools.chain.from_iterable(list(sessions_details.values()))),
    )

    with open(migrated_file_dir, "r", encoding=ENCODING) as file:
        source_code = file.read()

    source_code_tree = ast.parse(source_code)

    for node in ast.walk(source_code_tree):
        if isinstance(node, ast.FunctionDef) and node.name == function:
            node.args = params_added_function.args
            node.body = _get_with_removed_function(function_node=params_added_function)
            break

    source_code = astor.to_source(source_code_tree)
    formatted_code = black.format_str(source_code, mode=black.FileMode())

    with open(migrated_file_dir, "w", encoding=ENCODING) as file:
        file.write(formatted_code)

    logger.debug(MIGRATED_FILE_MODIFIED)

    return sessions_details


def get_pins_and_relays_info(
    sessions_details: Dict[str, List[str]]
) -> Tuple[List[PinInfo], List[RelayInfo]]:
    """Get pins and relays info.

    1. Get pins for sessions of instrument drivers other than niswitch driver.
    2. Get relays for sessions of niswitch driver.

    Args:
        sessions_details (Dict[str, List[str]]): Session details.

    Returns:
        Tuple[List[PinInfo], List[RelayInfo]]: List of pins and List of relays.
    """
    pins_info = []
    relays_info = []

    for driver, session_vars in sessions_details.items():
        if driver == DriverSession.niswitch.name:
            for session_var in session_vars:
                relays_info.append(
                    RelayInfo(
                        name=f"{session_var}_pin",
                        default_value=f"{driver}_pin",
                    )
                )
            continue

        if driver not in [driver.name for driver in DriverSession]:
            instrument_type = f"{driver}_instrument_type"
        else:
            instrument_type = f"{DriverSession[driver].value}"

        for session_var in session_vars:
            pins_info.append(
                PinInfo(
                    name=f"{session_var}_pin",
                    instrument_type=instrument_type,
                    default_value=f"{driver}_pin",
                )
            )

    return pins_info, relays_info


def get_session_mapping(sessions_details: Dict[str, List[str]]) -> List[SessionMapping]:
    """Get session mapping.

    1. Get session mapping using `get_connection` as strings.
    2. Create `SessionMapping` model.

    Args:
        sessions_details (Dict[str, List[str]]): Session details.

    Returns:
        List[SessionMapping]: Sessions and its mappings.
    """
    sessions_connections = []

    for driver, session_vars in sessions_details.items():
        for session_var in session_vars:
            if driver in NI_DRIVERS:
                connection = f"{RESERVATION}.get_{driver}_connection({session_var}_pin).session"
            else:
                connection = (
                    f"{RESERVATION}.get_connection({driver}.Session, {session_var}_pin).session"
                )

            sessions_connections.append(SessionMapping(name=session_var, mapping=connection))

    return sessions_connections


def get_pin_and_relay_names(pins_and_relays: List[Union[PinInfo, RelayInfo]]) -> str:
    """Get pin and relay names.

    Args:
        pins_and_relays (List[Union[PinInfo, RelayInfo]]): Pin info and relay info.

    Returns:
        str: pin and relay names.
    """
    pin_and_relay_names = [f"{pin_and_relay.name}" for pin_and_relay in pins_and_relays]
    return ", ".join(pin_and_relay_names)
