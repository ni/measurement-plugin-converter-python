"""Implementation of extraction of inputs from measurement function."""

import ast
from logging import getLogger
from typing import Dict, List, Union

from ni_measurement_plugin_converter._constants import (
    DEBUG_LOGGER,
)
from ni_measurement_plugin_converter._models import InputInfo
from ni_measurement_plugin_converter._utils._measurement_service import (
    extract_type,
    get_nims_datatype,
)

PYTHON_DATATYPE = "python datatype"
_DEFAULT = "default"
# Default values for datatypes.
TYPE_DEFAULT_VALUES = {
    "int": 1,
    "float": 1.1,
    "str": "",
    "bool": True,
    "List[int]": [1],
    "List[float]": [1.1],
    "List[str]": [""],
    "List[bool]": [True],
}
UNSUPPORTED_INPUTS = "The inputs {params} are skipped because their data types are unsupported."


def _get_input_params_without_defaults(args: List[ast.arg]) -> Dict[str, Dict[str, str]]:
    input_params = {}
    for arg in args:
        param_name = arg.arg
        param_type = None

        # Extract parameter type from annotation
        if arg.annotation:
            param_type = extract_type(arg.annotation)

        try:
            default_value = TYPE_DEFAULT_VALUES[param_type]
        except KeyError:
            default_value = None

        input_params[param_name] = {PYTHON_DATATYPE: param_type, _DEFAULT: default_value}

    return input_params


def _get_input_params_with_defaults(
    args: List[ast.arg],
    defaults: List[Union[ast.Constant, ast.List]],
) -> Dict[str, Dict[str, str]]:
    input_params = {}

    # Assign default values for the remaining parameters
    for arg, default_node in zip(args, defaults):
        param_name = arg.arg
        param_type = None

        # Extract parameter type from annotation
        if arg.annotation:
            param_type = extract_type(arg.annotation)

        # Extract default value
        default_value = ast.literal_eval(default_node)

        # Store parameter name, type, and default value
        input_params[param_name] = {PYTHON_DATATYPE: param_type, _DEFAULT: default_value}

    return input_params


def _update_inputs_info(inputs_info: Dict[str, Dict[str, str]]) -> List[InputInfo]:
    logger = getLogger(DEBUG_LOGGER)
    updated_inputs_info = []
    unsupported_inputs = []

    for param_name, param_info in inputs_info.items():
        input_type = get_nims_datatype(python_native_data_type=param_info[PYTHON_DATATYPE])

        if not input_type:
            unsupported_inputs.append(param_name)
            continue

        updated_inputs_info.append(
            InputInfo(
                param_name=param_name,
                param_type=param_info[PYTHON_DATATYPE],
                nims_type=input_type,
                default_value=param_info[_DEFAULT],
            )
        )

    if unsupported_inputs:
        logger.info(UNSUPPORTED_INPUTS.format(params=unsupported_inputs))

    return updated_inputs_info


def extract_inputs(function_node: ast.FunctionDef) -> List[InputInfo]:
    """Extract inputs' info from `function_node`.

    Args:
        function_node (FunctionDef): Measurement function node.

    Returns:
        List[InputInfo]: Measurement function input information.
    """
    inputs_info = {}
    param_defaults = function_node.args.defaults or []

    params_without_defaults = function_node.args.args[
        : len(function_node.args.args) - len(param_defaults)
    ]
    params_with_defaults = function_node.args.args[len(params_without_defaults) :]

    inputs_info.update(_get_input_params_without_defaults(params_without_defaults))
    inputs_info.update(_get_input_params_with_defaults(params_with_defaults, param_defaults))

    inputs_info = _update_inputs_info(inputs_info=inputs_info)

    return inputs_info


def generate_input_params(inputs_info: List[InputInfo]) -> str:
    """Generate string separated by comma where each element represents an input parameter.

    Args:
        inputs_info (List[InputInfo]): Input details.

    Returns:
        str: Input parameters names as a comma separated string.
    """
    parameter_names = [f"{info.param_name}={info.param_name}" for info in inputs_info]
    return ", ".join(parameter_names)


def generate_input_signature(inputs_info: List[InputInfo]) -> str:
    """Generate string separated by comma where each element represents an \
        input parameter with its data type.

    Args:
        inputs_info (List[InputInfo]): Input information.

    Returns:
        str: Each input parameters and its data type as a comma separated string.
    """
    parameter_info = [f"{info.param_name}:{info.param_type}" for info in inputs_info]
    return ", ".join(parameter_info)
