"""Get measurement function node."""

from ast import FunctionDef, parse, walk
from typing import Union


def get_measurement_function(measurement_file_dir: str, function: str) -> Union[None, FunctionDef]:
    """Get measurement `function` node from `measurement_file_dir`.

    1. Read the measurement file.
    2. Parse the measurement file code.
    3. Find the measurement function in the parsed code.
    4. If `function` is present in `measurement_file_dir`, the function node is returned. `None`
    is returned if not.

    Args:
        measurement_file_dir (str): Measurement file directory.
        function (str): Name of measurement function.

    Returns:
        Union[None, FunctionDef]: Function node is returned if present. `None` is returned if not.
    """
    function_node = None

    with open(measurement_file_dir, "r") as file:
        code = file.read()

    code_tree = parse(code)

    for node in walk(code_tree):
        if isinstance(node, FunctionDef) and node.name == function:
            function_node = node
            break

    return function_node
