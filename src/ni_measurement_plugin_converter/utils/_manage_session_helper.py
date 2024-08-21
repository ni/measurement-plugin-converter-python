import ast
from typing import Dict, List

from ni_measurement_plugin_converter.constants import DriverSession

_RESERVATION = "reservation"
_SESSION_INFO = "session_info"
_SESSION_CONSTRUCTOR = "session_constructor"
_INSTRUMENT_TYPE = "instrument_type"


def instrument_is_visa_type(call: ast.Call) -> bool:
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


def is_supported_drivers(call: ast.Call):
    if (
        isinstance(call.func, ast.Attribute)
        and isinstance(call.func.value, ast.Name)
        and call.func.value.id in [driver.name for driver in DriverSession]
        and (call.func.attr == "Session" or call.func.attr == "Task")
    ):
        return True

    if instrument_is_visa_type(call):
        return True

    return False


def get_sessions(code_tree: ast.Module, function: str) -> Dict[str, List[str]]:
    drivers = {}

    for node in ast.walk(code_tree):
        if isinstance(node, ast.FunctionDef) and node.name == function:
            for child_node in ast.walk(node):
                if (
                    isinstance(child_node, ast.With)
                    and hasattr(child_node, "items")
                    and child_node.items
                ):
                    for item in child_node.items:
                        if isinstance(item.context_expr, ast.Call):
                            call = item.context_expr
                            if is_supported_drivers(call):
                                if call.func.value.id not in drivers:
                                    drivers[call.func.value.id] = [item.optional_vars.id]
                                else:
                                    drivers[call.func.value.id].append(item.optional_vars.id)
            break

    return drivers


session_drivers = ["nidcpower", "nidmm", "nidigital", "niscope", "nifgen", "niswitch"]


def get_visa_with_item(driver: str, sessions: Dict[str, List[str]]) -> ast.withitem:
    if len(sessions[driver]) == 1:
        plugin_session = ast.withitem(
            context_expr=ast.Call(
                func=ast.Attribute(
                    value=ast.Name(id=_RESERVATION, ctx=ast.Load()),
                    attr="initialize_session",
                    ctx=ast.Load(),
                ),
                args=[
                    ast.Name(id=_SESSION_CONSTRUCTOR, ctx=ast.Load()),
                    ast.Name(id=_INSTRUMENT_TYPE, ctx=ast.Load()),
                ],
                keywords=[],
            ),
            optional_vars=ast.Name(id=f"visa_{_SESSION_INFO}", ctx=ast.Store()),
        )
    elif len(sessions[driver]) > 1:
        plugin_session = ast.withitem(
            context_expr=ast.Call(
                func=ast.Attribute(
                    value=ast.Name(id=_RESERVATION, ctx=ast.Load()),
                    attr="initialize_sessions",
                    ctx=ast.Load(),
                ),
                args=[
                    ast.Name(id=_SESSION_CONSTRUCTOR, ctx=ast.Load()),
                    ast.Name(id=_INSTRUMENT_TYPE, ctx=ast.Load()),
                ],
                keywords=[],
            ),
            optional_vars=ast.Name(id=f"visa_{_SESSION_INFO}", ctx=ast.Store()),
        )

    return plugin_session


def get_nidriver_with_item(driver: str, sessions: Dict[str, List[str]]) -> ast.withitem:
    if driver == "nidaqmx" and len(sessions[driver]) == 1:
        plugin_session = ast.withitem(
            context_expr=ast.Call(
                func=ast.Attribute(
                    value=ast.Name(id=_RESERVATION, ctx=ast.Load()),
                    attr="create_nidaqmx_task",
                    ctx=ast.Load(),
                ),
                args=[],
                keywords=[],
            ),
            optional_vars=ast.Name(id=f"nidaqmx_{_SESSION_INFO}", ctx=ast.Store()),
        )
    elif driver == "nidaqmx" and len(sessions[driver]) > 1:
        plugin_session = ast.withitem(
            context_expr=ast.Call(
                func=ast.Attribute(
                    value=ast.Name(id=_RESERVATION, ctx=ast.Load()),
                    attr="create_nidaqmx_task",
                    ctx=ast.Load(),
                ),
                args=[],
                keywords=[],
            ),
            optional_vars=ast.Name(id=f"nidaqmx_{_SESSION_INFO}s", ctx=ast.Store()),
        )

    elif len(sessions[driver]) == 1:
        plugin_session = ast.withitem(
            context_expr=ast.Call(
                func=ast.Attribute(
                    value=ast.Name(id=_RESERVATION, ctx=ast.Load()),
                    attr=f"initialize_{driver}_session",
                    ctx=ast.Load(),
                ),
                args=[],
                keywords=[],
            ),
            optional_vars=ast.Name(id=f"{driver}_{_SESSION_INFO}", ctx=ast.Store()),
        )
    elif len(sessions[driver]) > 1:
        plugin_session = ast.withitem(
            context_expr=ast.Call(
                func=ast.Attribute(
                    value=ast.Name(id=_RESERVATION, ctx=ast.Load()),
                    attr=f"initialize_{driver}_sessions",
                    ctx=ast.Load(),
                ),
                args=[],
                keywords=[],
            ),
            optional_vars=ast.Name(id=f"{driver}_{_SESSION_INFO}s", ctx=ast.Store()),
        )

    return plugin_session


def get_plugin_session_initializations(
    code_tree: ast.Module,
    function: str,
    sessions: Dict[str, List[str]],
) -> Dict[str, List[ast.withitem]]:
    new_with_items = {}
    for node in ast.walk(code_tree):
        if isinstance(node, ast.FunctionDef) and node.name == function:
            for child_node in ast.walk(node):
                if (
                    isinstance(child_node, ast.With)
                    and hasattr(child_node, "items")
                    and child_node.items
                ):
                    for item in child_node.items:
                        if isinstance(item.context_expr, ast.Call):
                            call = item.context_expr
                            if (
                                isinstance(call.func, ast.Attribute)
                                and isinstance(call.func.value, ast.Name)
                                and (
                                    call.func.value.id in session_drivers
                                    or call.func.value.id == "nidaqmx"
                                )
                                and (call.func.attr == "Session" or call.func.attr == "Task")
                                and call.func.value.id not in new_with_items
                            ):
                                new_with_items[call.func.value.id] = get_nidriver_with_item(
                                    call.func.value.id,
                                    sessions,
                                )
                            elif (
                                isinstance(call.func, ast.Attribute)
                                and isinstance(call.func.value, ast.Name)
                                and (
                                    call.func.attr == "open_resource"
                                    or call.func.attr == "get_instrument"
                                    or call.func.attr == "instrument"
                                )
                                and call.func.value.id not in new_with_items
                            ):
                                new_with_items[call.func.value.id] = get_visa_with_item(
                                    call.func.value.id,
                                    sessions,
                                )
    return new_with_items


def replace_session_initializations(
    code_tree: ast.Module,
    function: str,
    plugin_session_initializations: Dict[str, List[ast.withitem]],
) -> ast.Module:
    for node in ast.walk(code_tree):
        if isinstance(node, ast.FunctionDef) and node.name == function:
            for child_node in ast.walk(node):
                if (
                    isinstance(child_node, ast.With)
                    and hasattr(child_node, "items")
                    and child_node.items
                ):
                    child_node.items = [
                        withitem for withitem in plugin_session_initializations.values()
                    ]
                    break
            break

    return code_tree
