"""Helpers for session management."""

import ast
import re
from typing import Dict, List

from ni_measurement_plugin_converter.constants import ALPHANUMERIC_PATTERN, SessionManagement


def get_sessions_details(function_node: ast.FunctionDef) -> Dict[str, List[str]]:
    """Get drivers used and its session variable.

    Args:
        function_node (ast.FunctionDef): Measurement function code tree.

    Returns:
        Dict[str, List[str]]: Drivers as keys and list of session instance variables as values.
    """
    sessions_details = {}

    for child_node in ast.walk(function_node):
        if isinstance(child_node, ast.With) and hasattr(child_node, "items") and child_node.items:
            sessions_details = __get_session_details(child_node)
            break

    return sessions_details


def __get_session_details(child_node: ast.With) -> Dict[str, List[str]]:
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


def get_plugin_session_initializations(function_node: ast.Module) -> Dict[str, List[ast.withitem]]:
    """Get plugin session initializations.

    1. Create session initialization `withitem` for NI drivers.
    2. Create session initialization `withitem` for VISA type.

    Args:
        function_node (ast.FunctionDef): Measurement function code tree.

    Returns:
        Dict[str, List[ast.withitem]]: Drivers as keys and their respective `withitems` as values.
    """
    session_initializations = {}

    for child_node in ast.walk(function_node):
        if isinstance(child_node, ast.With) and hasattr(child_node, "items") and child_node.items:
            for item in child_node.items:
                if isinstance(item.context_expr, ast.Call):
                    session_initializations.update(
                        __get_plugin_session_initializations(item.context_expr)
                    )

    return session_initializations


def __get_plugin_session_initializations(call: ast.Call) -> Dict[str, List[ast.withitem]]:
    session_initializations = {}

    if (
        ni_drivers_supported_instrument(call)
        and call.func.value.id not in session_initializations
    ):
        session_initializations[call.func.value.id] = get_ni_driver_session_initialization(
            call.func.value.id
        )

    elif instrument_is_visa_type(call) and get_resource_name(call) not in session_initializations:
        resource_name = get_resource_name(call)
        session_initializations[resource_name] = get_visa_driver_plugin_session_initialization(
            resource_name
        )

    return session_initializations


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
        and call.func.value.id in SessionManagement.NI_DRIVERS
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


def get_ni_driver_session_initialization(driver: str) -> ast.withitem:
    """Get NI driver session initialization as a `withitem`.

    Args:
        driver (str): NI instrument driver name.

    Returns:
        ast.withitem: NI driver plug-in session initialization as a `withitem`.
    """
    if driver == "nidaqmx":
        attribute = "create_nidaqmx_tasks"

    else:
        attribute = f"initialize_{driver}_sessions"

    plugin_session = ast.withitem(
        context_expr=ast.Call(
            func=ast.Attribute(
                value=ast.Name(id=SessionManagement.RESERVATION, ctx=ast.Load()),
                attr=attribute,
                ctx=ast.Load(),
            ),
            args=[],
            keywords=[],
        ),
        optional_vars=ast.Name(id=f"{driver}_{SessionManagement.SESSION_INFO}", ctx=ast.Store()),
    )
    return plugin_session


def get_visa_driver_plugin_session_initialization(driver: str) -> ast.withitem:
    """Get VISA session initialization.

    Args:
        driver (str): VISA instrument driver name.

    Returns:
        ast.withitem: VISA driver plugin session initialization as a `withitem`.
    """
    plugin_session = ast.withitem(
        context_expr=ast.Call(
            func=ast.Attribute(
                value=ast.Name(id=SessionManagement.RESERVATION, ctx=ast.Load()),
                attr="initialize_sessions",
                ctx=ast.Load(),
            ),
            args=[
                ast.Name(id=f"{driver}_{SessionManagement.SESSION_CONSTRUCTOR}", ctx=ast.Load()),
                ast.Name(id=f"{driver}_{SessionManagement.INSTRUMENT_TYPE}", ctx=ast.Load()),
            ],
            keywords=[],
        ),
        optional_vars=ast.Name(id=f"{driver}_{SessionManagement.SESSION_INFO}", ctx=ast.Store()),
    )

    return plugin_session
