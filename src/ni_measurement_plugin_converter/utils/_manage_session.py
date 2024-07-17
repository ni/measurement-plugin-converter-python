"""Implementation of session management."""

import ast
from logging import Logger
from typing import List, Tuple

import astor

from ni_measurement_plugin_converter.constants import DriverSession, UserMessage


def manage_session(
    migrated_file_dir: str,
    function_node: ast.FunctionDef,
    logger: Logger,
) -> Tuple[str, str]:
    """Manage session.

    1. Add session reservation variable to migrated file.
    2. Replace session initialization.
    3. Insert session assignment to migrated file.

    Args:
        migrated_file_dir (str): Migrated file directory.
        function_node (ast.FunctionDef): Function node object.
        logger (Logger): Logger object.

    Returns:
        Tuple[str, str]: Instrument name and resource name.
    """
    source_code = __get_source_code(migrated_file_dir)
    drivers = [driver.name for driver in DriverSession]

    logger.info(UserMessage.ADD_RESERVE_SESSION)
    add_reservation_param(migrated_file_dir, source_code, function_node)

    logger.info(UserMessage.ADD_SESSION_INITIALIZATION)
    session_details = replace_session_initialization(
        migrated_file_dir,
        source_code,
        function_node,
        drivers,
    )

    for driver, param_value, actual_name in session_details:
        instrument_type = driver
        resource_name = param_value
        actual_session_name = actual_name

    insert_session_assignment(
        migrated_file_dir,
        source_code,
        function_node,
        f"{actual_session_name} = session_info.session",
    )

    return instrument_type, resource_name


def __get_source_code(migrated_file_dir: str):

    with open(migrated_file_dir, "r") as file:
        source_code = file.read()

    return source_code


def add_reservation_param(
    migrated_file_dir: str,
    source_code: ast.Module,
    function_node: ast.FunctionDef,
) -> None:
    """Add reservation parameter to migrated measurement file.

    Args:
        migrated_file_dir (str): Migrated measurement file directory.
        source_code (ast.Moduel): Source code object.
        function_node (ast.FunctionDef): Measurement function node.
    """
    code_tree = ast.parse(source_code)

    # Add the new parameter as the first parameter in the function's arguments
    new_param = ast.arg(arg="reservation", annotation=None)
    function_node.args.args.insert(0, new_param)

    modified_source = astor.to_source(code_tree)

    with open(migrated_file_dir, "w") as file:
        file.write(modified_source)


def replace_session_initialization(
    migrated_file_dir: str,
    source_code: ast.Module,
    function_node: ast.FunctionDef,
    drivers: List[str],
) -> List[Tuple[str, str, str]]:
    """Replace session initialization in the migrated file.

    Args:
        migrated_file_dir (str): Migrated file directory.
        source_code (ast.Module): Source code object.
        function_node (ast.FunctionDef): Function node object.
        drivers (List[str]): Drivers

    Returns:
        List[Tuple[str, str, str]]: List of replaced drivers, resource names, sessions.
    """
    replacements = []
    code_tree = ast.parse(source_code)

    for driver in drivers:
        for node in ast.walk(function_node):
            if isinstance(node, ast.With) and hasattr(node, "items") and node.items:
                replacements.extend(__replace_session(node, driver))

    modified_source = astor.to_source(code_tree)

    with open(migrated_file_dir, "w") as file:
        file.write(modified_source)

    return replacements


def __replace_session(node: ast.With, driver: List[str]) -> List[Tuple[str, str, str]]:
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

                item.optional_vars.id = "session_info"
                call.func.attr = f"initialize_{driver}_session"
                call.func.value.id = "reservation"

                replacements.append(
                    (
                        driver,
                        call.keywords[0].value.s,
                        actual_session_name,
                    )
                )

                call.keywords.clear()

    return replacements


def insert_session_assignment(
    migrated_file_dir: str,
    source_code: ast.Module,
    function_node: ast.FunctionDef,
    session_info: str,
) -> None:
    """Insert session assignment.

    Args:
        migrated_file_dir (str): Migrated file directory.
        source_code (ast.Module): Source code object.
        function_node (ast.FunctionDef): Function node object.
        session_info (str): Session information.
    """
    for _, child_node in enumerate(function_node.body):
        if isinstance(child_node, ast.With):
            # Get the indentation level of the with statement
            indent = " " * (child_node.col_offset + 4)

            # Construct the text to insert with proper indentation
            text_line = f"{indent}{session_info}\n"

            # Insert the text immediately after the with block
            source_lines = source_code.split("\n")
            source_lines.insert(child_node.lineno, text_line)
            modified_source = "\n".join(source_lines)

            return modified_source

    with open(migrated_file_dir, "w") as file:
        file.write(modified_source)
