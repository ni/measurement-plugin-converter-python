"""Implementation of extraction of inputs from measurement function."""

import ast
from typing import Dict, List, Union

from ni_measurement_plugin_converter.constants import TYPE_DEFAULT_VALUES
from ni_measurement_plugin_converter.models import InputConfigurations

from ._measurement_service import extract_type, get_nims_datatype


def extract_inputs(function_node: ast.FunctionDef) -> List[InputConfigurations]:
    """Extract inputs from `function_node`.

    Args:
        function_node (FunctionDef): Measurement function node.

    Returns:
        List[Inputs]: Measurement function input details.
    """
    # Analyze types of default values for parameters
    parameter_types = {}
    defaults = function_node.args.defaults or []

    args_without_defaults = function_node.args.args[: len(function_node.args.args) - len(defaults)]
    args_with_defaults = function_node.args.args[len(args_without_defaults) :]

    parameter_types.update(get_input_params_with_defaults(args_with_defaults, defaults))
    parameter_types.update(get_input_params_without_defaults(args_without_defaults))

    input_configuration = get_input_configurations(inputs=parameter_types)

    return input_configuration


def get_input_params_without_defaults(args: List[ast.arg]) -> Dict[str, Dict[str, str]]:
    """Get input parameters with its default values assigned externally.

    Args:
        args (List[ast.arg]): Input arguments object without default values.

    Returns:
        Dict[str, Dict[str, str]]: Argument name as key and its type and default value as values.
    """
    parameter_types = {}
    for arg in args:
        param_name = arg.arg
        param_type = None

        # Extract parameter type from annotation
        param_type = extract_type(arg.annotation)

        # Assign default value based on parameter type if it's not provided
        try:
            default_value = TYPE_DEFAULT_VALUES[param_type]
        except KeyError:
            default_value = None

        # Store parameter name, type, and default value
        parameter_types[param_name] = {"type": param_type, "default": default_value}

    return parameter_types


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
    parameter_types = {}

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
        parameter_types[param_name] = {"type": param_type, "default": default_value}

    return parameter_types


def get_input_configurations(inputs: Dict[str, Dict[str, str]]) -> List[InputConfigurations]:
    """Get input configurations.

    1. Get measurement service data type for each argument.
    2. Format input configurations to `InputConfigurations`.

    Args:
        inputs (Dict[str, Dict[str, str]]): Input configurations as dictionary.

    Returns:
        List[InputConfigurations]: Updated input with measurement service data type.
    """
    input_data = []

    for param_name, param_info in inputs.items():
        input_type = get_nims_datatype(param_info["type"])
        input_data.append(
            InputConfigurations(
                param_name=param_name,
                param_type=param_info["type"],
                nims_type=input_type,
                default_value=param_info["default"],
            )
        )

    return input_data


def generate_input_params(input_configurations: List[InputConfigurations]) -> str:
    """Generate string separated by comma where each element represents an input parameter.

    Args:
        input_configurations (List[InputConfigurations]): Input configurations.

    Returns:
        str: Input parameters as a comma separated string.
    """
    parameter_names = [input_config.param_name for input_config in input_configurations]
    return ", ".join(parameter_names)


def generate_input_signature(input_configurations: List[InputConfigurations]) -> str:
    """Generate string separated by comma where each element represents an \
        input parameter with its data type.

    Args:
        input_configurations (List[InputConfigurations]): Input configurations.

    Returns:
        str: Each input parameters and its data type as a comma separated string.
    """
    parameter_info = []
    for input_config in input_configurations:
        parameter_info.append(f"{input_config.param_name}:{input_config.param_type}")

    return ", ".join(parameter_info)
