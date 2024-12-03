"""Implementation of extraction of outputs from measurement function."""

import ast
import re
from logging import getLogger
from typing import Any, List, Tuple

from ni_measurement_plugin_converter._constants import DEBUG_LOGGER
from ni_measurement_plugin_converter.models import OutputInfo
from ni_measurement_plugin_converter.utils._measurement_service import (
    extract_type,
    get_nims_datatype,
)

UNSUPPORTED_OUTPUTS = (
    "The outputs {variables} are skipped because their data types are unsupported."
)


def _extract_type_and_variable_names(function_body: List[Any]) -> Tuple[bool, List[str]]:
    iterable_output = False
    output_variables = []

    for node in function_body:
        if isinstance(node, ast.Return):
            if isinstance(node.value, (ast.Tuple, ast.List)):
                iterable_output = True
                output_variables.extend(_get_output_variables(node.value.elts))

            elif isinstance(node.value, ast.Name):
                output_variables.append(node.value.id)

    return iterable_output, output_variables


def _get_output_variables(elements: List[ast.Name]) -> List[str]:
    output_variables = [element.id for element in elements]
    return output_variables


def _get_output_info(
    output_variable_names: List[str],
    output_return_types: List[str],
) -> List[OutputInfo]:
    logger = getLogger(DEBUG_LOGGER)
    output_configurations = []
    unsupported_outputs = []

    for variable_name, return_type in zip(output_variable_names, output_return_types):
        output_type = get_nims_datatype(python_native_data_type=return_type)

        if not output_type:
            unsupported_outputs.append(variable_name)
            continue

        output_configurations.append(
            OutputInfo(
                variable_name=variable_name,
                variable_type=return_type,
                nims_type=output_type,
            )
        )

    if unsupported_outputs:
        logger.info(UNSUPPORTED_OUTPUTS.format(variables=unsupported_outputs))

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


def extract_outputs(function_node: ast.FunctionDef) -> Tuple[List[OutputInfo], bool]:
    """Extract outputs information from `function_node`.

    Args:
        function_node (ast.FunctionDef): Measurement function node.

    Returns:
        Tuple[List[Output], bool]: Measurement function outputs info and \
        boolean representing output type is tuple or not.
    """
    iterable_output, output_variables = _extract_type_and_variable_names(function_node.body)
    output_types = extract_type(function_node.returns)

    if isinstance(output_types, str) and iterable_output:
        # Separate each output types from combined output types.
        output_types = re.findall(r"\b\w+\[[^\[\]]+\]|\b\w+", output_types)
        output_types = output_types[1:]

    elif isinstance(output_types, str) and not iterable_output:
        output_types = [output_types]

    output_configurations = _get_output_info(output_variables, output_types)

    return output_configurations, iterable_output
