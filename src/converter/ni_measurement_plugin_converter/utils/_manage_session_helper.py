"""Helpers for session management."""

import ast
import re
from typing import Dict, List, Union

from ni_measurement_plugin_converter.models import PinInfo, RelayInfo, SessionMapping
from ni_measurement_plugin_converter.utils._constants import *


def get_sessions_details(function_node: ast.FunctionDef) -> Dict[str, List[str]]:
    """Get drivers used and its corresponding session instance variable.

    Args:
        function_node (ast.FunctionDef): Measurement function code tree.

    Returns:
        Dict[str, List[str]]: Drivers as keys and list of session instance variables as values.
    """
    sessions_details = {}

    for child_node in ast.walk(function_node):
        if isinstance(child_node, ast.With) and hasattr(child_node, "items") and child_node.items:
            sessions_details = _get_session_details(child_node)
            break

    return sessions_details


def _get_session_details(child_node: ast.With) -> Dict[str, List[str]]:
    sessions_details = {}

    for item in child_node.items:
        if isinstance(item.context_expr, ast.Call):
            call = item.context_expr

            if ni_drivers_supported_instrument(call):
                if call.func.value.id not in sessions_details:
                    sessions_details[call.func.value.id] = [item.optional_vars.id]
                else:
                    sessions_details[call.func.value.id].append(item.optional_vars.id)

            elif instrument_is_visa_type(call):
                resource_name = get_resource_name(call)

                if resource_name not in sessions_details:
                    sessions_details[resource_name] = [item.optional_vars.id]
                else:
                    sessions_details[resource_name].append(item.optional_vars.id)

    return sessions_details


def get_plugin_session_initializations(sessions_details: Dict[str, List[str]]) -> str:
    """Get plugin session initializations.

    1. Create plugin session initialization for NI-Drivers.
    2. Create plugin session initialization for VISA.

    Args:
        sessions_details (Dict[str, List[str]]): Session details.

    Returns:
        str: Plugin session initializations.
    """
    session_initialization_code = []

    for driver in list(sessions_details.keys()):
        if driver in NI_DRIVERS:
            session_initialization_code.append(get_ni_driver_session_initialization(driver))

        else:
            session_initialization_code.append(
                get_visa_driver_plugin_session_initialization(driver)
            )

    return ", ".join(session_initialization_code)


def ni_drivers_supported_instrument(call: ast.Call) -> bool:
    """Check if the instrument used is one of the supported NI drivers.

    Args:
        call (ast.Call): Function call code tree.

    Returns:
        bool: True if instrument is one of the supported NI drivers. Else False.
    """
    if (
        isinstance(call.func, ast.Attribute)
        and isinstance(call.func.value, ast.Name)
        and call.func.value.id in NI_DRIVERS
        and (call.func.attr == "Session" or call.func.attr == "Task")
    ):
        return True

    return False


def instrument_is_visa_type(call: ast.Call) -> bool:
    """Check if the instrument used is of VISA type.

    Args:
        call (ast.Call): Function call code tree.

    Returns:
        bool: True if instrument is VISA type. Else False.
    """
    if (
        isinstance(call.func, ast.Attribute)
        and isinstance(call.func.value, ast.Name)
        and (
            call.func.attr == "open_resource"
            or call.func.attr == "get_instrument"
            or call.func.attr == "instrument"
        )
    ):
        return True

    return False


def get_resource_name(call: ast.Call) -> str:
    """Get resource_name.

    1. Get `resource_name` if it is a keyword argument.
    2. If it is an argument, use the first argument as `resource_name`.
    3. Sanitize `resource_name` to have only alphanumeric characters.

    Args:
        call (ast.Call): Function call code tree.

    Returns:
        str: Alphanumeric `resource_name`.
    """
    resource_name = None

    for keyword in call.keywords:
        if keyword.arg == "resource_name":
            resource_name = ast.literal_eval(keyword.value)
            break

    if resource_name is None and call.args and len(call.args) > 0:
        resource_name = ast.literal_eval(call.args[0])

    resource_name = re.sub(ALPHANUMERIC_PATTERN, "_", resource_name)

    return resource_name


def get_ni_driver_session_initialization(driver: str) -> str:
    """Get NI driver session initialization as a string.

    Args:
        driver (str): NI instrument driver name.

    Returns:
        str: NI driver plug-in session initialization as a string.
    """
    if driver == "nidaqmx":
        return f"{RESERVATION}.create_nidaqmx_tasks()"

    return f"{RESERVATION}.initialize_{driver}_sessions()"


def get_visa_driver_plugin_session_initialization(driver: str) -> str:
    """Get VISA session initialization.

    Args:
        driver (str): VISA instrument driver name.

    Returns:
        str: VISA driver plugin session initialization as a string.
    """
    return f"{RESERVATION}.initialize_sessions({driver}_{SESSION_CONSTRUCTOR}, {driver}_{INSTRUMENT_TYPE})"


def check_for_visa(sessions_details: Dict[str, List[str]]) -> bool:
    """Check for VISA instruments used.

    Args:
        sessions_details (Dict[str, List[str]]): Session details.

    Returns:
        bool: True if VISA driver is used.
    """
    for driver in list(sessions_details.keys()):
        if driver not in NI_DRIVERS:
            return True

    return False


def get_pin_and_relay_names_signature(pins_and_relays: List[Union[PinInfo, RelayInfo]]) -> str:
    """Get pin and relay names signature.

    Args:
        pins_and_relays (List[Union[PinInfo, RelayInfo]]): Pin info and relay info.

    Returns:
        str: Pin and relay names signature.
    """
    pin_or_relay_signature = [f"{pin_and_relay.name}: str" for pin_and_relay in pins_and_relays]
    return ", ".join(pin_or_relay_signature)


def get_sessions_signature(session_mappings: List[SessionMapping]) -> str:
    """Get session signature.

    Args:
        session_mappings (List[SessionMapping]): Session mappings.

    Returns:
        str: Session mapping signature.
    """
    sessions = [
        f"{session_mapping.name}={session_mapping.name}"
        for session_mapping in session_mappings
    ]
    return ", ".join(sessions)
