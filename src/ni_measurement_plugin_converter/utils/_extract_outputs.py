"""Implementation of extraction of outputs from measurement function."""

import ast
import re
from typing import Any, List, Tuple

from ni_measurement_plugin_converter.models import OutputInfo

from ._measurement_service import extract_type, get_nims_datatype


def extract_outputs(function_node: ast.FunctionDef) -> Tuple[List[OutputInfo], bool]:
    """Extract outputs information from `function_node`.

    Args:
        function_node (ast.FunctionDef): Measurement function node.

    Returns:
        Tuple[List[Output], bool]: Measurement function outputs info and \
        boolean representing output type is tuple or not.
    """
    iterable_output, output_variables = extract_type_and_variable_names(function_node.body)
    output_types = extract_type(function_node.returns)

    if isinstance(output_types, str) and iterable_output:
        # Separate each output types from combined output types.
        output_types = re.findall(r"\b\w+\[[^\[\]]+\]|\b\w+", output_types)
        output_types = output_types[1:]

    elif isinstance(output_types, str) and not iterable_output:
        output_types = [output_types]

    output_configurations = get_output_info(output_variables, output_types)

    return output_configurations, iterable_output


def extract_type_and_variable_names(function_body: List[Any]) -> Tuple[bool, List[str]]:
    """Extract measurement function output type and variable names.

    Args:
        function_body (List[Any]): Measurement function body.

    Returns:
        Tuple[bool, List[str]]: Measurement function output type and variable names.
    """
    iterable_output = False
    output_variables = []

    for node in function_body:
        if isinstance(node, ast.Return):
            if isinstance(node.value, (ast.Tuple, ast.List)):
                iterable_output = True
                output_variables.extend(get_output_variables(node.value.elts))

            elif isinstance(node.value, ast.Name):
                output_variables.append(node.value.id)

    return iterable_output, output_variables


def get_output_variables(elements: List[ast.Name]) -> List[str]:
    """Get output variables of list and tuple type output.

    Args:
        elements (ast.Name): Return elements.

    Returns:
        List[str]: List of variable names.
    """
    output_variables = [element.id for element in elements]
    return output_variables


def get_output_info(
    output_variable_names: List[str],
    output_return_types: List[str],
) -> List[OutputInfo]:
    """Get outputs' information.

    1. Get `measurement_plugin_sdk_service` data type for each argument.
    2. Format outputs information to `OutputInfo`.

    Args:
        output_variable_names (List[str]): Output variable names.
        output_return_types (List[str]): Output variable types.

    Returns:
        List[OutputInfo]: Updated output info with `measurement_plugin_sdk_service` data type.
    """
    output_configurations = []

    for variable_name, return_type in zip(output_variable_names, output_return_types):
        output_type = get_nims_datatype(python_native_data_type=return_type)

        if not output_type:
            continue

        output_configurations.append(
            OutputInfo(
                variable_name=variable_name,
                variable_type=return_type,
                nims_type=output_type,
            )
        )

    return output_configurations


def generate_output_signature(outputs_info: List[OutputInfo]) -> str:
    """Generate string separated by comma where each element represents output data type.

    Args:
        outputs_info (List[Output]): Outputs information.

    Returns:
        str: Output data type as comma separated string.
    """
    variable_types = [info.variable_type for info in outputs_info]
    return ", ".join(variable_types)
