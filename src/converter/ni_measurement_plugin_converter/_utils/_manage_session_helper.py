"""Helpers for session management."""

import ast
import re
from typing import Dict, List, Union

from ni_measurement_plugin_converter._constants import (
    ALPHANUMERIC_PATTERN,
    NI_DRIVERS,
    RESERVATION,
)
from ni_measurement_plugin_converter._models import PinInfo, RelayInfo, SessionMapping

SESSION_CONSTRUCTOR = "session_constructor"
INSTRUMENT_TYPE = "instrument_type"


def _get_session_details(child_node: ast.With) -> Dict[str, List[str]]:
    sessions_details: Dict[str, List[str]] = {}

    for item in child_node.items:
        if isinstance(item.context_expr, ast.Call) and (item.optional_vars is not None):
            call = item.context_expr

            if ni_drivers_supported_instrument(call):
                if (
                    isinstance(call.func, ast.Attribute)
                    and isinstance(call.func.value, ast.Name)
                    and isinstance(item.optional_vars, ast.Name)
                ):
                    driver_id = call.func.value.id
                    session_id = item.optional_vars.id

                    if driver_id not in sessions_details:
                        sessions_details[driver_id] = [session_id]
                    else:
                        sessions_details[driver_id].append(session_id)

            elif instrument_is_visa_type(call):
                resource_name = _get_resource_name(call)

                if isinstance(item.optional_vars, ast.Name):
                    session_id = item.optional_vars.id

                    if resource_name not in sessions_details:
                        sessions_details[resource_name] = [session_id]
                    else:
                        sessions_details[resource_name].append(session_id)

    return sessions_details


def _get_resource_name(call: ast.Call) -> str:
    resource_name = None

    for keyword in call.keywords:
        if keyword.arg == "resource_name":
            resource_name = ast.literal_eval(keyword.value)
            break

    if resource_name is None and call.args and len(call.args) > 0:
        resource_name = ast.literal_eval(call.args[0])

    resource_name = re.sub(ALPHANUMERIC_PATTERN, "_", str(resource_name))

    return resource_name


def _get_ni_driver_session_initialization(driver: str) -> str:
    if driver == "nidaqmx":
        return f"{RESERVATION}.create_nidaqmx_tasks()"

    return f"{RESERVATION}.initialize_{driver}_sessions()"


def _get_visa_driver_plugin_session_initialization(driver: str) -> str:
    return f"{RESERVATION}.initialize_sessions({driver}_{SESSION_CONSTRUCTOR}, {driver}_{INSTRUMENT_TYPE})"


def get_sessions_details(function_node: ast.FunctionDef) -> Dict[str, List[str]]:
    """Get drivers used and their corresponding session instance variable.

    Args:
        function_node: The code tree of the measurement function.

    Returns:
        A dictionary with drivers as keys and lists of session instance variables as values.
    """
    sessions_details = {}

    for child_node in ast.walk(function_node):
        if isinstance(child_node, ast.With) and hasattr(child_node, "items") and child_node.items:
            sessions_details = _get_session_details(child_node)
            break

    return sessions_details


def get_plugin_session_initializations(sessions_details: Dict[str, List[str]]) -> str:
    """Get plugin session initializations.

    1. Create plugin session initialization for NI-Drivers.
    2. Create plugin session initialization for VISA.

    Args:
        sessions_details: A dictionary containing session details.

    Returns:
        The plugin session initializations for each driver.
    """
    session_initialization_code = []

    for driver in list(sessions_details.keys()):
        if driver in NI_DRIVERS:
            session_initialization_code.append(_get_ni_driver_session_initialization(driver))

        else:
            session_initialization_code.append(
                _get_visa_driver_plugin_session_initialization(driver)
            )

    return ", ".join(session_initialization_code)


def ni_drivers_supported_instrument(call: ast.Call) -> bool:
    """Check if the instrument used is one of the supported NI drivers.

    Args:
        call: Function call code tree.

    Returns:
        True if instrument is one of the supported NI drivers, else False.
    """
    if (
        isinstance(call.func, ast.Attribute)
        and isinstance(call.func.value, ast.Name)
        and call.func.value.id in NI_DRIVERS
        and call.func.value.id in NI_DRIVERS
        and (call.func.attr == "Session" or call.func.attr == "Task")
    ):
        return True

    return False


def instrument_is_visa_type(call: ast.Call) -> bool:
    """Check if the instrument used is of VISA type.

    Args:
        call: Function call code tree.

    Returns:
        bool: True if instrument is VISA type, else False.
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


def check_for_visa(sessions_details: Dict[str, List[str]]) -> bool:
    """Check for VISA instruments used.

    Args:
        sessions_details: A dictionary containing session details.

    Returns:
        True if a VISA driver is used, else False.
    """
    for driver in list(sessions_details.keys()):
        if driver not in NI_DRIVERS:
            return True

    return False


def get_pin_and_relay_names_signature(pins_and_relays: List[Union[PinInfo, RelayInfo]]) -> str:
    """Get pin and relay names signature.

    Args:
        pins_and_relays: A list of PinInfo or RelayInfo objects.

    Returns:
        Pin and relay names signature.
    """
    pin_or_relay_signature = [f"{pin_and_relay.name}: str" for pin_and_relay in pins_and_relays]
    return ", ".join(pin_or_relay_signature)


def get_sessions_signature(session_mappings: List[SessionMapping]) -> str:
    """Get session signature.

    Args:
        session_mappings: A list of SessionMapping objects.

    Returns:
        Session mapping signature.
    """
    sessions = [
        f"{session_mapping.name}={session_mapping.name}" for session_mapping in session_mappings
    ]
    return ", ".join(sessions)
