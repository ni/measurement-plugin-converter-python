"""Implementation of session management."""

import ast
from logging import getLogger
from typing import List, Tuple

import astor

from ni_measurement_plugin_converter.constants import (
    DEBUG_LOGGER,
    ENCODING,
    DebugMessage,
    DriverSession,
    UserMessage,
)

_RESERVATION = "reservation"
_SESSION_INFO = "session_info"
_SESSION_CONSTRUCTOR = "session_constructor"
_INSTRUMENT_TYPE = "instrument_type"


def manage_session(migrated_file_dir: str, function: str) -> str:
    """Manage session.

    1. Add session reservation variable to migrated file.
    2. Replace session initialization in migrated file.
    3. Insert session assignment into migrated file.

    Args:
        migrated_file_dir (str): Migrated measurement file directory.
        function (str): Measurement function name.

    Returns:
        str: Instrument name.
    """
    logger = getLogger(DEBUG_LOGGER)

    with open(migrated_file_dir, "r", encoding=ENCODING) as file:
        source_code = file.read()

    code_tree = ast.parse(source_code)

    logger.info(UserMessage.ADD_RESERVE_SESSION)
    reservation_added_code_tree = add_param(
        code_tree=code_tree,
        function=function,
        param=_RESERVATION,
    )

    logger.info(UserMessage.REPLACE_SESSION_INITIALIZATION)
    session_replaced_code_tree, session_details = replace_session_initialization(
        code_tree=reservation_added_code_tree,
        function=function,
    )

    for driver, session_name in session_details:
        instrument_type = driver
        session_name = session_name

    logger.info(UserMessage.ASSIGN_SESSION_INFO)

    session_inserted_code_tree = insert_session_assignment(
        code_tree=session_replaced_code_tree,
        function=function,
        session_name=session_name,
    )

    code_tree = astor.to_source(session_inserted_code_tree)

    with open(migrated_file_dir, "w", encoding=ENCODING) as file:
        file.write(code_tree)

    logger.debug(DebugMessage.MIGRATED_FILE_MODIFIED)

    return instrument_type


def replace_session_initialization(
    code_tree: ast.Module,
    function: str,
) -> Tuple[str, List[Tuple[str, str, str]]]:
    """Replace session initialization in the migrated file.

    Args:
        code_tree (ast.Module): Migrated measurement source code tree.
        function (str): Measurement function name.

    Returns:
        Tuple[str, List[Tuple[str, str]]]: Updated source code tree and List of tuple of \
            replaced drivers, sessions.
    """
    replacements = []

    for node in ast.walk(code_tree):
        if isinstance(node, ast.FunctionDef) and node.name == function:
            for driver in DriverSession:
                for child_node in ast.walk(node):
                    if (
                        isinstance(child_node, ast.With)
                        and hasattr(child_node, "items")
                        and child_node.items
                    ):
                        replacements.extend(__replace_session(child_node, driver.name))

            if replacements and replacements[0][0] == DriverSession.nivisa.name:
                instrument_type_added_code_tree = add_param(
                    code_tree=code_tree,
                    function=function,
                    param=_INSTRUMENT_TYPE,
                )

                code_tree = add_param(
                    code_tree=instrument_type_added_code_tree,
                    function=function,
                    param=_SESSION_CONSTRUCTOR,
                )

    return code_tree, replacements


def add_param(code_tree: ast.Module, function: str, param: str) -> ast.Module:
    """Add a parameter to user measurement function in code tree.

    Args:
        code_tree (ast.Module): Migrated measurement source code tree.
        function (str): Measurement function name.
        param (str): Parameter to be added.

    Returns:
        ast.Module: Updated measurement function with parameter.
    """
    for node in code_tree.body:
        if isinstance(node, ast.FunctionDef) and node.name == function:
            node.args.args.insert(0, param)

    return code_tree


def __replace_session(node: ast.With, driver: str) -> List[Tuple[str, str, str]]:
    replacements = []

    for item in node.items:
        if isinstance(item.context_expr, ast.Call):
            call = item.context_expr
            if (
                isinstance(call.func, ast.Attribute)
                and isinstance(call.func.value, ast.Name)
                and call.func.value.id == driver
                and call.func.attr == "Session"
            ):
                actual_session_name = item.optional_vars.id

                item.optional_vars.id = _SESSION_INFO
                call.func.attr = f"initialize_{driver}_session"
                call.func.value.id = _RESERVATION

                replacements.append(
                    (
                        driver,
                        actual_session_name,
                    )
                )

                call.keywords.clear()
                call.args.clear()

            elif (
                isinstance(call.func, ast.Attribute)
                and isinstance(call.func.value, ast.Name)
                and call.func.value.id == driver
                and call.func.attr == "Task"
            ):
                actual_session_name = item.optional_vars.id

                item.optional_vars.id = _SESSION_INFO
                call.func.attr = "create_nidaqmx_task"
                call.func.value.id = _RESERVATION

                replacements.append(
                    (
                        driver,
                        actual_session_name,
                    )
                )

                call.keywords.clear()
                call.args.clear()

            elif (
                isinstance(call.func, ast.Attribute)
                and isinstance(call.func.value, ast.Name)
                and (
                    call.func.attr == "open_resource"
                    or call.func.attr == "get_instrument"
                    or call.func.attr == "instrument"
                )
            ):
                actual_session_name = item.optional_vars.id

                item.optional_vars.id = _SESSION_INFO
                call.func.attr = "initialize_session"
                call.func.value.id = _RESERVATION

                replacements.append(
                    (
                        DriverSession.nivisa.name,
                        actual_session_name,
                    )
                )

                call.keywords.clear()
                call.args.clear()

                call.args = [
                    ast.Name(id=_SESSION_CONSTRUCTOR, ctx=ast.Load()),
                    ast.Name(id=_INSTRUMENT_TYPE, ctx=ast.Load()),
                ]

    return replacements


def insert_session_assignment(
    code_tree: ast.Module,
    function: str,
    session_name: str,
) -> ast.Module:
    """Insert session assignment into migrated measurement file source code.

    Args:
        source_code (ast.Module): Migrated measurement source code tree.
        function (str): Measurement function name.
        session_name (str): Session name from user measurement.

    Returns:
        ast.Module: Session assignment inserted source code tree.
    """
    session_info = ast.Assign(
        targets=[ast.Name(id=session_name, ctx=ast.Store())],
        value=ast.Attribute(
            value=ast.Name(id=_SESSION_INFO, ctx=ast.Load()),
            attr="session",
            ctx=ast.Load(),
        ),
    )

    for node in ast.walk(code_tree):
        if isinstance(node, ast.FunctionDef) and node.name == function:
            for child_node in node.body:
                if isinstance(child_node, ast.With):
                    child_node.body.insert(0, session_info)

    return code_tree
