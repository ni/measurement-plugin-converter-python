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
        # Get combined output types to separate elements.
        output_types = re.findall(r"'([^']*)'", output_types)

    elif isinstance(output_types, str) and not iterable_output:
        output_types = [output_types]

    output_configurations = get_outputs_infos(output_variables, output_types)

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
            if isinstance(node.value, ast.Tuple) or isinstance(node.value, ast.List):
                iterable_output = True
                output_variables.extend(get_all_output_variables(node.value.elts))

            elif isinstance(node.value, ast.Name):
                output_variables.append(node.value.id)

    return iterable_output, output_variables


def get_all_output_variables(elements: List[ast.Name]) -> List[str]:
    """Get all output variables of list and tuple type output.

    Args:
        elements (ast.Return): Return elements.

    Returns:
        List[str]: List of variable names.
    """
    output_variables = []

    for element in elements:
        output_variables.append(element.id)

    return output_variables


def get_outputs_infos(
    output_variable_names: List[str],
    output_return_types: Tuple[str],
) -> List[OutputInfo]:
    """Get outputs' information.

    1. Get measurement service data type for each argument.
    2. Format outputs information to `OutputInfo`.

    Args:
        output_variable_names (List[str]): Output variable names.
        output_return_types (Tuple[str]): Output variable types.

    Returns:
        List[OutputInfo]: Updated output infos with measurement service data type.
    """
    output_configurations = []

    for variable_name, return_type in zip(output_variable_names, output_return_types):
        output_type = get_nims_datatype(return_type)
        output_configurations.append(
            OutputInfo(
                variable_name=variable_name,
                variable_type=return_type,
                nims_type=output_type,
            )
        )

    return output_configurations


def generate_output_signature(outputs_infos: List[OutputInfo]) -> str:
    """Generate string separated by comma where each element represents output data type.

    Args:
        outputs_infos (List[Output]): Outputs information.

    Returns:
        str: Output data type as comma separated string.
    """
    variable_types = [output_infos.variable_type for output_infos in outputs_infos]
    return ", ".join(variable_types)
