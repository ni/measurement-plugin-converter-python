"""Implementation of extraction of outputs from measurement function."""

import ast
from typing import List, Tuple

from ni_measurement_plugin_converter.models import OutputConfigurations
from ._measurement_service import extract_type, get_nims_datatype


def extract_outputs(function_node: ast.FunctionDef) -> Tuple[List[OutputConfigurations], bool]:
    """Extract outputs from `function_node`

    Args:
        function_node (ast.FunctionDef): Measurement function node.

    Returns:
        Tuple[List[OutputConfigurations], bool]: Measurement function output details and \
        boolean representing output is tuple or not.
    """
    output_variables = extract_variables(function_node.body)
    output_types = extract_type(function_node.returns)

    if isinstance(output_types, str):
        tuple_of_outputs = False
        output_types = (output_types,)

    output_configurations = get_output_configuration(output_variables, output_types)

    return output_configurations, tuple_of_outputs


def extract_variables(function_body:ast.FunctionDef) -> List[str]:
    """Extract measurement funciton output variables.

    Args:
        function_body (ast.FunctionDef.body): Measurement function body.

    Returns:
        List[str]: Measurement function output variables.
    """
    output_variables = []

    for node in function_body:
        if isinstance(node, ast.Return):
            if isinstance(node.value, ast.Tuple):  # Check if return value is a tuple
                for element in node.value.elts:
                    output_variables.extend(expand_list_type(element))

            elif isinstance(node.value, ast.Name):
                output_variables.append(node.value.id)

    return output_variables


def expand_list_type(node) -> List[str]:
    """_summary_

    Args:
        node (_type_): _description_

    Returns:
        List[str]: 
    """
    if isinstance(node, ast.Name):
        return [node.id]
    elif isinstance(node, List):
        inner_types = [extract_type(elt) for elt in node.elts]
        return inner_types
    elif isinstance(node, ast.Call) and isinstance(node.func, ast.Name) and node.func.id == "List":
        return [extract_type(arg) for arg in node.args]
    else:
        return []


def get_output_configuration(
    output_variable_names: List[str],
    output_return_types: Tuple[str],
) -> List[OutputConfigurations]:
    """

    Args:
        output_variable_names (List[str]): _description_
        output_return_types (Tuple[str]): _description_

    Returns:
        List[OutputConfigurations]: _description_
    """
    output_configurations = []

    for variable_name, return_type in zip(output_variable_names, output_return_types):
        output_type = get_nims_datatype(return_type)
        output_configurations.append(
            OutputConfigurations(
                variable_name=variable_name,
                variable_type=return_type,
                nims_type=output_type,
            )
        )

    return output_configurations


def generate_output_signature(output_configurations: List[OutputConfigurations]) -> str:
    """Generate string separated by comma where each element represents output data type.

    Args:
        output_configurations (List[OutputConfigurations]): Output configurations.

    Returns:
        str: Output data type as comma separated string.
    """
    variable_types = []

    for output_config in output_configurations:
        variable_types.append(output_config.variable_type)

    return ", ".join(variable_types)
