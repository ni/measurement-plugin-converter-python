"""Implementation of get measurement function."""

import ast

from ni_measurement_plugin_converter._constants import ENCODING

FUNCTION_NODE_NOT_FOUND = "Function node could not be found for function: {function}"


def get_function_node(
    file_dir: str,
    function: str,
) -> ast.FunctionDef:
    """Retrieve the function node for a given function name from a file.

    1. Parse the file content into an abstract syntax tree (AST).
    2. Search for the specified function in the AST.
    3. Return the function node if found; otherwise, raise a ValueError.

    Args:
        file_dir: The path to the file containing the function.
        function: The name of the function to find.

    Returns:
        The AST node representing the function.

    Raises:
        ValueError: If the specified function is not found in the file.
    """
    function_node = None

    with open(file_dir, "r", encoding=ENCODING) as file:
        code = file.read()

    code_tree = ast.parse(code)

    for node in ast.walk(code_tree):
        if isinstance(node, ast.FunctionDef) and node.name == function:
            function_node = node
            break

    if function_node is None:
        raise ValueError(FUNCTION_NODE_NOT_FOUND.format(function=function))

    return function_node
