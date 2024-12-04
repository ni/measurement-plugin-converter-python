"""Implementation of get measurement function."""

import ast
from typing import Union

from ni_measurement_plugin_converter._constants import ENCODING

FUNCTION_NODE_NOT_FOUND = "Function node could not be found for function: {function}"

def get_function_node(
    file_dir: str,
    function: str,
) -> ast.FunctionDef:
    """Get `function` node from `file_dir`.

    1. Parse file code into abstract syntax tree.
    2. Find the function in the parsed code.
    3. If `function` is present in `file_dir`, then the function node is returned. If \
    not, then `None` is returned.

    Args:
        file_dir (str): File directory.
        function (str): Name of function.

    Returns:
        ast.FunctionDef: If `function` is present in `file_dir`, \
        then the function node is returned. If not, then raises ValueError.
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
