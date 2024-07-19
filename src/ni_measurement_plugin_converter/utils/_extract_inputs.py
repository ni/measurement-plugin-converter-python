"""Implementation of extraction of inputs from measurement function."""

import ast
from typing import Dict, List, Union

from ni_measurement_plugin_converter.constants import TYPE_DEFAULT_VALUES
from ni_measurement_plugin_converter.models import InputInfo

from ._measurement_service import extract_type, get_nims_datatype

_TYPE = "type"
_DEFAULT = "default"


def extract_inputs(function_node: ast.FunctionDef) -> List[InputInfo]:
    """Extract inputs' info from `function_node`.

    Args:
        function_node (FunctionDef): Measurement function node.

    Returns:
        List[InputInfo]: Measurement function input information.
    """
    inputs_infos = {}
    param_defaults = function_node.args.defaults or []

    params_without_defaults = function_node.args.args[
        : len(function_node.args.args) - len(param_defaults)
    ]
    params_with_defaults = function_node.args.args[len(params_without_defaults) :]

    inputs_infos.update(get_input_params_without_defaults(params_without_defaults))
    inputs_infos.update(get_input_params_with_defaults(params_with_defaults, param_defaults))

    inputs_infos = update_inputs_infos(inputs_infos=inputs_infos)

    return inputs_infos


def get_input_params_without_defaults(args: List[ast.arg]) -> Dict[str, Dict[str, str]]:
    """Get input parameters whose default values are not available.

    Args:
        args (List[ast.arg]): Input arguments object without default values.

    Returns:
        Dict[str, Dict[str, str]]: Parameter name as key and its type and default value as values.
    """
    input_params = {}
    for arg in args:
        param_name = arg.arg
        param_type = None

        param_type = extract_type(arg.annotation)

        try:
            default_value = TYPE_DEFAULT_VALUES[param_type]
        except KeyError:
            default_value = None

        input_params[param_name] = {_TYPE: param_type, _DEFAULT: default_value}

    return input_params


def get_input_params_with_defaults(
    args: List[ast.arg],
    defaults: List[Union[ast.Constant, ast.List]],
) -> Dict[str, Dict[str, str]]:
    """Get input parameters with its default values assigned.

    Args:
        args (List[ast.arg]): Input arguments object.
        defaults (List[Union[ast.Constant, ast.List]]): User inputted default values.

    Returns:
        Dict[str, Dict[str, str]]: Argument name as key and its type and default value as values.
    """
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
        input_params[param_name] = {_TYPE: param_type, _DEFAULT: default_value}

    return input_params


def update_inputs_infos(inputs_infos: Dict[str, Dict[str, str]]) -> List[InputInfo]:
    """Update inputs' information.

    1. Get measurement service data type for each argument.
    2. Format inputs information to `InputInfo`.

    Args:
        inputs_infos (Dict[str, Dict[str, str]]): Input info as dictionary.

    Returns:
        List[InputInfo]: Updated input info with measurement service data type.
    """
    updated_inputs_infos = []

    for param_name, param_info in inputs_infos.items():
        input_type = get_nims_datatype(param_info[_TYPE])
        updated_inputs_infos.append(
            InputInfo(
                param_name=param_name,
                param_type=param_info[_TYPE],
                nims_type=input_type,
                default_value=param_info[_DEFAULT],
            )
        )

    return updated_inputs_infos


def generate_input_params(inputs_infos: List[InputInfo]) -> str:
    """Generate string separated by comma where each element represents an input parameter.

    Args:
        inputs_infos (List[InputInfo]): Input details.

    Returns:
        str: Input parameters names as a comma separated string.
    """
    parameter_names = [input_infos.param_name for input_infos in inputs_infos]
    return ", ".join(parameter_names)


def generate_input_signature(inputs_infos: List[InputInfo]) -> str:
    """Generate string separated by comma where each element represents an \
        input parameter with its data type.

    Args:
        inputs_infos (List[InputInfo]): Input information.

    Returns:
        str: Each input parameters and its data type as a comma separated string.
    """
    parameter_info = [
        f"{input_infos.param_name}:{input_infos.param_type}" for input_infos in inputs_infos
    ]
    return ", ".join(parameter_info)
