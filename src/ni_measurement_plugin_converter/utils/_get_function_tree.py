"""Implementation of Get measurement function."""

import ast
from typing import Union


def get_measurement_function(
    measurement_file_dir: str,
    function: str,
) -> Union[ast.FunctionDef, None]:
    """Get measurement `function` node from `measurement_file_dir`.

    1. Parse measurement file code into abstract syntax tree.
    2. Find the measurement function in the parsed code.
    3. If `function` is present in `measurement_file_dir`, the function node is returned. `None`
    is returned if not.

    Args:
        measurement_file_dir (str): Measurement file directory.
        function (str): Name of measurement function.

    Returns:
        Union[ast.FunctionDef, None]: Function node is returned if present. \
            `None` is returned if not.
    """
    function_node = None

    with open(measurement_file_dir, "r") as file:
        code = file.read()

    code_tree = ast.parse(code)

    for node in ast.walk(code_tree):
        if isinstance(node, ast.FunctionDef) and node.name == function:
            function_node = node
            break

    return function_node
