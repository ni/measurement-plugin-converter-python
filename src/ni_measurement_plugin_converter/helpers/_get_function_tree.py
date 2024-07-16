"""Get measurement function tree."""

import ast


def get_measurement_function(measurement_file_dir: str, function: str):

    with open(measurement_file_dir, "r") as file:
        code = file.read()

    code_tree = ast.parse(code)
    function_node = next(
        (
            node
            for node in ast.walk(code_tree)
            if isinstance(node, ast.FunctionDef) and node.name == function
        ),
        None,
    )

    return function_node
