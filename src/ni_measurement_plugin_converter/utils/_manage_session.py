"""Implementation of session management."""

import ast
from typing import List

import astor


def manage_session(migrated_file_dir: str, function_node: ast.FunctionDef, driver_names: List[str]):

    source_code = get_source_code(migrated_file_dir)

    add_reservation_param(migrated_file_dir, source_code, function_node)
    session_details = replace_session_initialization(migrated_file_dir, source_code, function_node, driver_names)

    for driver_name, param_value, actual_name in session_details:
        instrument_type = driver_name
        resource_name = param_value
        actual_session_name = actual_name

    insert_session_assigning(migrated_file_dir, source_code, function_node, f"{actual_session_name} = session_info.session")

    return instrument_type, resource_name


def get_source_code(migrated_file_dir: str):

    with open(migrated_file_dir, "r") as file:
        source_code = file.read()

    return source_code


def add_reservation_param(
    migrated_file_dir: str,
    source_code: str,
    function_node: ast.FunctionDef,
) -> None:
    """Add reservation parameter to migrated measurement file.

    Args:
        migrated_file_dir (str): Migrated measurement file directory.
        function_node (ast.FunctionDef): Measurement function node.
    """
    code_tree = ast.parse(source_code)

    # Add the new parameter as the first parameter in the method's arguments
    new_param = ast.arg(arg="reservation", annotation=None)
    function_node.args.args.insert(0, new_param)

    modified_source = astor.to_source(code_tree)

    with open(migrated_file_dir, "w") as file:
        file.write(modified_source)


def replace_session_initialization(
    migrated_file_dir: str,
    source_code: str,
    function_node: str,
    driver_names: List[str],
):
    replacements = []

    code_tree = ast.parse(source_code)

    # Helper function to replace session initialization
    def replace_session(node, driver_name):
        if isinstance(node, ast.With):
            if hasattr(node, "items") and node.items:
                for item in node.items:
                    if isinstance(item.context_expr, ast.Call):
                        call = item.context_expr
                        if isinstance(call.func, ast.Attribute) and isinstance(
                            call.func.value,
                            ast.Name,
                        ):
                            if call.func.value.id == driver_name and call.func.attr == "Session":
                                actual_session_name = item.optional_vars.id
                                item.optional_vars.id = "session_info"
                                call.func.attr = f"initialize_{driver_name}_session"
                                call.func.value.id = "reservation"
                                replacements.append(
                                    (
                                        driver_name,
                                        call.keywords[0].value.s,
                                        actual_session_name,
                                    )
                                )
                                call.keywords.clear()

    for driver_name in driver_names:
        for child_node in ast.walk(function_node):
            replace_session(child_node, driver_name)

    modified_source = astor.to_source(code_tree)

    with open(migrated_file_dir, "w") as file:
        file.write(modified_source)

    return replacements


def insert_session_assigning(
    migrated_file_dir: str,
    source_code: str,
    function_node: ast.FunctionDef,
    text_to_insert: str,
) -> None:
    for _, child_node in enumerate(function_node.body):
        if isinstance(child_node, ast.With):
            # Get the indentation level of the with statement
            indent = " " * (child_node.col_offset + 4)  # Assuming 4 spaces per level
            # Construct the text to insert with proper indentation
            text_line = f"{indent}{text_to_insert}\n"
            # Insert the text immediately after the with block
            source_lines = source_code.split("\n")
            source_lines.insert(child_node.lineno, text_line)
            # Join the modified source lines
            modified_source = "\n".join(source_lines)
            return modified_source

    with open(migrated_file_dir, "w") as file:
        file.write(modified_source)
