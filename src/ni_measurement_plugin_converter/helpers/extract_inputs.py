"""Implementation of inputs extraction."""

import ast


def extract_input_details(file_path, method_name):
    # Parse the Python file to extract the AST
    with open(file_path, "r") as file:
        code = file.read()
    tree = ast.parse(code)

    # Find the method node in the AST
    method_node = next(
        (
            node
            for node in ast.walk(tree)
            if isinstance(node, ast.FunctionDef) and node.name == method_name
        ),
        None,
    )
    if method_node is None:
        print(f"Method '{method_name}' not found in the file.")
        return {}

    # Analyze types of default values for parameters
    parameter_types = {}
    defaults = method_node.args.defaults or []
    args_without_defaults = method_node.args.args[: len(method_node.args.args) - len(defaults)]

    for arg in args_without_defaults:
        param_name = arg.arg
        param_type = None

        # Extract parameter type from annotation
        param_type = extract_type(arg.annotation)

        # Assign default value based on parameter type if it's not provided
        default_value = None
        if param_type == "int":
            default_value = 0
        elif param_type == "str":
            default_value = ""

        # Store parameter name, type, and default value
        parameter_types[param_name] = {"type": param_type, "default": default_value}

    # Assign default values for the remaining parameters
    for arg, default_node in zip(method_node.args.args[len(args_without_defaults) :], defaults):
        param_name = arg.arg
        param_type = None

        # Extract parameter type from annotation
        if arg.annotation:
            param_type = extract_type(arg.annotation)
                

        # Extract default value
        default_value = ast.literal_eval(default_node)

        # Store parameter name, type, and default value
        parameter_types[param_name] = {"type": param_type, "default": default_value}

    return parameter_types


def extract_type(node):
    if isinstance(node, ast.Name):
        return node.id

    elif isinstance(node, ast.Subscript):
        generic_type = extract_type(node.value)

        if isinstance(node.slice.value, ast.Tuple):
            inner_types = [extract_type(elt) for elt in node.slice.value.elts]
            return inner_types

        elif isinstance(node.slice, ast.Index):
            slice_id = extract_type(node.slice.value)
            return f"{generic_type}[{slice_id}]"

        else:
            slice_id = extract_type(node.slice)
            return f"{generic_type}[{slice_id}]"

    else:
        return ""