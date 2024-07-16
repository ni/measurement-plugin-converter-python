"""Utilizes command line args to create a measurement using template files."""

import os
import pathlib
import re
import shutil
from pathlib import Path
from typing import Any

import click
from click import ClickException
from mako.template import Template

from ni_measurement_plugin_converter import __version__
from ni_measurement_plugin_converter.constants import (
    CONTEXT_SETTINGS,
    MEASUREMENT_VERSION,
    MIGRATED_MEASUREMENT_FILENAME,
    NIMS_TYPE,
    ArgsDescription,
    DriverSession,
    TemplateFile,
    UserMessage,
    DebugMessage,
)
from ni_measurement_plugin_converter.helpers import (
    add_parameter_to_method,
    get_measurement_function,
    extract_inputs,
    get_return_details,
    initialize_logger,
    insert_session_assigning,
    remove_handlers,
    replace_session_initialization,
)
from ni_measurement_plugin_converter.models import CliInputs, InvalidCliArgsError

# Refactor
_drivers = ["nidcpower"]
instrument_type = ""
resource_name = ""
actual_session_name = ""


@click.command(context_settings=CONTEXT_SETTINGS)
@click.option("-d", "--display-name", help=ArgsDescription.SERVICE, required=True)
@click.option(
    "-m",
    "--measurement-file-dir",
    help=ArgsDescription.MEASUREMENT_FILE_DIR,
    required=True,
)
@click.option("-f", "--function", help=ArgsDescription.FUNCTION, required=True)
@click.option("-o", "--output-dir", help=ArgsDescription.OUTPUT_DIR, required=True)
def run(
    display_name: str,
    measurement_file_dir: str,
    function: str,
    output_dir: str,
) -> None:
    try:
        log_directory = None
        logger = initialize_logger(name="console_logger", log_directory=log_directory)
        logger.info(UserMessage.STARTING_EXECUTION)

        cli_args = CliInputs(display_name=display_name, measurement_file_dir=measurement_file_dir, function=function, output_dir=output_dir)

        remove_handlers(logger)
        logger = initialize_logger(name="debug_logger", log_directory=output_dir)

        logger.info(UserMessage.VALIDATE_CLI_ARGS)

        shutil.copy(output_dir, os.path.join(output_dir, MIGRATED_MEASUREMENT_FILENAME))
        logger.debug(DebugMessage.FILE_MIGRATED)

        logger.debug(DebugMessage.GET_FUNCTION)
        function_node = get_measurement_function(measurement_file_dir, function)

        logger.info(UserMessage.EXTRACT_INPUT_INFO)

        inputs = extract_inputs(function_node)
        input_configurations = get_input_configurations(inputs)
        input_param_names = get_input_variables(input_configurations)
        input_signature = generate_method_signature(input_configurations)

        logger.info(UserMessage.EXTRACT_OUTPUT_INFO)

        output_variable_names, output_variable_types = get_return_details(
            measurement_file_dir,
            function,
        )
        output_configurations = _extract_outputs(output_variable_names, output_variable_types)
        output_param_types = _get_ouput_types(output_configurations)

        tuple_of_output = True
        if isinstance(output_variable_types, str):
            output_variable_types = (output_variable_types,)
            tuple_of_output = False

        migrated_file_directory = os.path.join(output_dir, MIGRATED_MEASUREMENT_FILENAME)

        logger.info(UserMessage.ADD_RESERVE_SESSION)
        add_parameter_to_method(
            migrated_file_directory,
            function,
            "reservation",
        )

        logger.info(UserMessage.ADD_SESSION_INITIALIZATION)
        session_details = replace_session_initialization(
            migrated_file_directory,
            function,
            _drivers,
        )
        for driver_name, param_value, actual_name in session_details:
            instrument_type = driver_name
            resource_name = param_value
            actual_session_name = actual_name

        insert_session_assigning(
            migrated_file_directory,
            function,
            actual_session_name + " = session_info.session",
        )

        nims_instrument = get_nims_instrument(instrument_type)

        service_class = f"{display_name}_Python"
        display_name_for_filenames = re.sub(r"\s+", "", display_name)
        serviceconfig_file = os.path.join(
            output_dir,
            f"{display_name_for_filenames}.serviceconfig",
        )

        _create_file(
            TemplateFile.MEASUREMENT_TEMPLATE,
            os.path.join(output_dir, TemplateFile.MEASUREMENT_FILENAME),
            display_name=display_name,
            version=MEASUREMENT_VERSION,
            service_class=service_class,
            serviceconfig_file=f"{display_name_for_filenames}.serviceconfig",
            resource_name=resource_name,
            instrument_type=instrument_type,
            nims_instrument=nims_instrument,
            input_configurations=input_configurations,
            output_configurations=output_configurations,
            input_signature=input_signature,
            input_param_names=input_param_names,
            output_param_types=output_param_types,
            updated_file_name=f"{cli_args.display_name}.{Path(MIGRATED_MEASUREMENT_FILENAME).stem}",
            method_name=function,
            directory_out=output_dir,
            tuple_of_output=tuple_of_output,
        )
        logger.debug(DebugMessage.MEASUREMENT_FILE_CREATED)
        _create_file(
            TemplateFile.SERVICE_CONFIG_TEMPLATE,
            serviceconfig_file,
            display_name=display_name,
            service_class=service_class,
            directory_out=output_dir,
        )
        logger.debug(DebugMessage.SERVICE_CONFIG_CREATED)
        _create_file(
            TemplateFile.BATCH_TEMPLATE,
            os.path.join(output_dir, TemplateFile.BATCH_FILENAME),
            directory_out=output_dir,
        )
        logger.debug(DebugMessage.BATCH_FILE_CREATED)
        _create_file(
            TemplateFile.HELPER_TEMPLATE,
            os.path.join(output_dir, TemplateFile.HELPER_FILENAME),
            directory_out=output_dir,
        )
        logger.debug(DebugMessage.HELPER_FILE_CREATED)
        logger.info(UserMessage.MEASUREMENT_PLUGIN_CREATED.format(plugin_dir=output_dir))

    except InvalidCliArgsError as input_error:
        logger.error(input_error)

    except ClickException as e:
        logger.error(e.message)

    except Exception as error:
        logger.error(error)
        logger.error(UserMessage.CHECK_LOG_FILE)

    finally:
        logger.info(UserMessage.PROCESS_COMPLETED)


def get_input_configurations(inputs):
    input_data = []

    for param_name, param_info in inputs.items():
        input_type = get_nims_datatype(param_info["type"])
        input_data.append(
            {
                "name": param_name,
                "actual_type": param_info["type"],
                "type": input_type,
                "default_value": param_info["default"],
            }
        )

    return input_data


def _extract_outputs(output_variable_names, output_return_types):
    output_data = []

    for var_name, return_type in zip(output_variable_names, output_return_types):
        output_type = get_nims_datatype(return_type)
        output_data.append({"name": var_name, "actual_type": return_type, "type": output_type})

    return output_data


def get_nims_datatype(type):
    try:
        return NIMS_TYPE[type]
    except KeyError:
        ...


def get_nims_instrument(instrument_type):
    try:
        return DriverSession[instrument_type].value
    except KeyError:
        ...


def generate_method_signature(inputs):
    parameter_info = []
    for input_param in inputs:
        parameter_info.append(f"{input_param['name']}:{input_param['actual_type']}")

    return ", ".join(parameter_info)


def get_input_variables(inputs):
    parameter_names = [param["name"] for param in inputs]
    return ", ".join(parameter_names)


def _get_ouput_types(outputs):
    parameter_types = []
    for param in outputs:
        parameter_types.append(param["actual_type"])
    return ", ".join(parameter_types)


def _create_file(
    template_name: str,
    file_name: str,
    **template_args: Any,
) -> None:
    output = _render_template(template_name, **template_args)

    with open(file_name, "wb") as f:
        f.write(output)


def _render_template(template_name: str, **template_args: Any) -> bytes:
    file_dir = str(pathlib.Path(__file__).parent / "templates" / template_name)

    template = Template(
        filename=file_dir,
        input_encoding=TemplateFile.ENCODING,
        output_encoding=TemplateFile.ENCODING,
    )
    try:
        return template.render(**template_args)
    except Exception as e:
        raise e
