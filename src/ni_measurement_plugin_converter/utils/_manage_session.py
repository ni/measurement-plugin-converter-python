"""Implementation of session management."""

import ast
from logging import Logger
from typing import List, Tuple

import astor

from ni_measurement_plugin_converter.constants import (
    ENCODING,
    DebugMessage,
    DriverSession,
    UserMessage,
)

_RESERVATION = "reservation"
_SESSION_INFO = "session_info"


def manage_session(migrated_file_dir: str, function: str, logger: Logger) -> str:
    """Manage session.

    1. Add session reservation variable to migrated file.
    2. Replace session initialization in migrated file.
    3. Insert session assignment into migrated file.

    Args:
        migrated_file_dir (str): Migrated measurement file directory.
        function (str): Measurement function name.
        logger (Logger): Logger object.

    Returns:
        str: Instrument name.
    """
    with open(migrated_file_dir, "r", encoding=ENCODING) as file:
        source_code = file.read()

    code_tree = ast.parse(source_code)

    logger.info(UserMessage.ADD_RESERVE_SESSION)
    reservation_added_source_code = add_reservation_param(code_tree, function)

    logger.info(UserMessage.REPLACE_SESSION_INITIALIZATION)
    session_replaced_source_code, session_details = replace_session_initialization(
        source_code=reservation_added_source_code,
        function=function,
    )

    for driver, actual_name in session_details:
        instrument_type = driver
        actual_session_name = actual_name

    logger.info(UserMessage.ASSIGN_SESSION_INFO)
    session_inserted_source_code = insert_session_assignment(
        source_code=session_replaced_source_code,
        function=function,
        session_info=f"{actual_session_name} = {_SESSION_INFO}.session",
    )

    with open(migrated_file_dir, "w", encoding=ENCODING) as file:
        file.write(session_inserted_source_code)

    logger.debug(DebugMessage.MIGRATED_FILE_MODIFIED)

    return instrument_type


def add_reservation_param(code_tree: ast.Module, function: str) -> str:
    """Add reservation parameter to source code.

    Args:
        code_tree (ast.Module): Migrated measurement source code tree.
        function (str): Measurement function name.

    Returns:
        str: Updated source code with reservation parameter.
    """
    for node in code_tree.body:
        if isinstance(node, ast.FunctionDef) and node.name == function:
            node.args.args.insert(0, _RESERVATION)

    added_source = astor.to_source(code_tree)

    return added_source


def replace_session_initialization(
    source_code: str,
    function: str,
) -> Tuple[str, List[Tuple[str, str, str]]]:
    """Replace session initialization in the migrated file.

    Args:
        source_code (str): Migrated measurement source code.
        function (str): Measurement function name.

    Returns:
        Tuple[str, List[Tuple[str, str]]]: Updated source code and List of tuple of \
            replaced drivers, sessions.
    """
    replacements = []
    code_tree = ast.parse(source_code)

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

    modified_source = astor.to_source(code_tree)

    return modified_source, replacements


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

            elif (
                isinstance(call.func, ast.Attribute)
                and isinstance(call.func.value, ast.Name)
                and call.func.value.id == driver
                and call.func.attr == "Task"
            ):
                actual_session_name = item.optional_vars.id

                item.optional_vars.id = _SESSION_INFO
                call.func.attr = f"create_nidaqmx_task"
                call.func.value.id = _RESERVATION

                replacements.append(
                    (
                        driver,
                        actual_session_name,
                    )
                )

                call.keywords.clear()

    return replacements


def insert_session_assignment(
    source_code: str,
    function: str,
    session_info: str,
) -> None:
    """Insert session assignment into migrated measurement file source code.

    Args:
        source_code (str): Migrated measurement source code.
        function (str): Measurement function name.
        session_info (str): Session information.
    """
    code_tree = ast.parse(source_code)

    for node in ast.walk(code_tree):
        if isinstance(node, ast.FunctionDef) and node.name == function:
            for _, child_node in enumerate(node.body):
                if isinstance(child_node, ast.With):
                    # Get the start position of the `with` statement.
                    indent = " " * (child_node.col_offset + 4)

                    # Construct the text to insert with proper indentation.
                    text_line = f"{indent}{session_info}\n"

                    # Insert the text immediately after the with block.
                    source_lines = source_code.split("\n")
                    source_lines.insert(child_node.lineno, text_line)
                    modified_source = "\n".join(source_lines)

    return modified_source