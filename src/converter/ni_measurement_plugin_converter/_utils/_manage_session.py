"""Implementation of session management."""

import ast
import itertools
from enum import Enum
from logging import Logger, getLogger
from pathlib import Path
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
from ni_measurement_plugin_converter._models import PinInfo, RelayInfo, SessionMapping
from ni_measurement_plugin_converter._utils import get_function_node
from ni_measurement_plugin_converter._utils._manage_session_helper import (
    check_for_visa,
    get_pin_and_relay_names_signature,
    get_plugin_session_initializations,
    get_sessions_details,
    get_sessions_signature,
    instrument_is_visa_type,
    ni_drivers_supported_instrument,
)

SESSION_CONSTRUCTOR = "session_constructor"
INSTRUMENT_TYPE = "instrument_type"
INVALID_DRIVERS = "Invalid/No driver used. Supported drivers: {supported_drivers}"
EXTRACT_DRIVER_SESSIONS = "Extracting driver sessions from measurement function..."
MIGRATED_FILE_MODIFIED = "Migrated file is modified."
ADD_SESSION_INITIALIZATION = "Adding session initialization..."
ADD_SESSION_MAPPING = "Adding session mapping..."
DEFINE_PINS_RELAYS = "Defining pins and relays..."


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
        arg_node = ast.arg(arg=param, annotation=None)
        function_node.args.args.insert(0, arg_node)

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


def _manage_session(migrated_file_dir: str, function: str) -> Dict[str, List[str]]:
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


def _get_pins_and_relays_info(
    sessions_details: Dict[str, List[str]], plugin_metadata: Dict[str, Any]
) -> Tuple[List[PinInfo], List[RelayInfo]]:
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

    plugin_metadata["pins_info"] = pins_info
    plugin_metadata["relays_info"] = relays_info
    pins_and_relays = pins_info[:] + relays_info
    plugin_metadata["pin_and_relay_signature"] = get_pin_and_relay_names_signature(pins_and_relays)
    plugin_metadata["pin_or_relay_names"] = _get_pin_and_relay_names(pins_and_relays)

    return pins_info, relays_info


def _get_session_mapping(sessions_details: Dict[str, List[str]]) -> List[SessionMapping]:
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


def _get_pin_and_relay_names(pins_and_relays: List[Union[PinInfo, RelayInfo]]) -> str:
    pin_and_relay_names = [f"{pin_and_relay.name}" for pin_and_relay in pins_and_relays]
    return ", ".join(pin_and_relay_names)


def process_sessions_and_update_metadata(
    migrated_file_path: Path, function: str, plugin_metadata: Dict[str, Any], logger: Logger
) -> Tuple[List[PinInfo], List[RelayInfo]]:
    """Process session details and update plugin metadata.

    This function retrieves session information from the migrated file and updates the
    provided plugin metadata with session initializations, mappings, pins, and relays.

    Args:
        migrated_file_path: Path to the migrated Python file.
        function: Name of the measurement function.
        plugin_metadata: Metadata dictionary to be updated with session data.
        logger: Logger instance.

    Returns:
        Information about pins and relays.
    """
    sessions_details = _manage_session(str(migrated_file_path), function)

    logger.info(DEFINE_PINS_RELAYS)
    pins_info, relays_info = _get_pins_and_relays_info(sessions_details, plugin_metadata)

    logger.info(ADD_SESSION_MAPPING)
    sessions_connections = _get_session_mapping(sessions_details)

    plugin_metadata["session_mappings"] = sessions_connections
    plugin_metadata["sessions"] = get_sessions_signature(sessions_connections)

    logger.info(ADD_SESSION_INITIALIZATION)

    plugin_metadata["session_initializations"] = get_plugin_session_initializations(
        sessions_details
    )
    plugin_metadata["is_visa"] = check_for_visa(sessions_details)
    return pins_info, relays_info
