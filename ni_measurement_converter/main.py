"""Utilizes command line args to create a measurement using template files."""

import os
import pathlib
import re
import shutil
from logging import Logger
from pathlib import Path
from typing import Any, Tuple

import click
from click import BadParameter, ClickException
from mako.template import Template

from ni_measurement_converter import __version__
from ni_measurement_converter.constants import (
    MEASUREMENT_VERSION,
    MIGRATED_MEASUREMENT_FILENAME,
    TemplateFile,
    UserMessages,
)
from ni_measurement_converter.helpers import (
    add_file_handler,
    add_parameter_to_method,
    add_stream_handler,
    extract_input_details,
    get_return_details,
    initialize_logger,
    insert_session_assigning,
    remove_handlers,
    replace_session_initialization,
)
from ni_measurement_converter.models import CliInputs

_drivers = ["nidcpower"]
instrument_type = ""
resource_name = ""
actual_session_name = ""


@click.command(context_settings = {"help_option_names": ["-h", "--help"]})
@click.option("-d", "--display-name", help="Display Name", required=True)
@click.option(
    "-f",
    "--file-dir",
    help="Directory of the Measurement file",
    required=True,
)
@click.option(
    "-m",
    "--method-name",
    help="Name of the Measurement method",
    required=True,
)
def convert_measurement(
    display_name: str,
    file_dir: str,
    method_name: str,
) -> None:
    try:
        log_folder_path = None
        logger, log_folder_path = __initialize_logger(
            name="console_logger",
            folder_path=log_folder_path,
        )

        logger.info(UserMessages.STARTED_EXECUTION)
        cli_args = CliInputs(display_name=display_name, file_dir=file_dir, method_name=method_name)

        measurement_plugin_path = os.path.normpath(
            os.path.join(
                os.path.dirname(cli_args.file_dir),
                cli_args.display_name,
            )
        )

        logger.debug(UserMessages.FILE_MIGRATED)
        shutil.copy(file_dir, os.path.join(measurement_plugin_path, MIGRATED_MEASUREMENT_FILENAME))

        remove_handlers(logger)

        logger, log_folder_path = __initialize_logger(
            name="debug_logger",
            folder_path=measurement_plugin_path,
        )

        logger.info(UserMessages.EXTRACT_INPUTS)
        input_parameters = extract_input_details(file_dir, method_name)

        output_variable_names, output_variable_types = get_return_details(file_dir, method_name)

        tuple_of_output = True
        if isinstance(output_variable_types, str):
            output_variable_types = (output_variable_types,)
            tuple_of_output = False

        input_configurations = _extract_inputs(input_parameters)

        logger.info(UserMessages.EXTRACT_OUTPUTS)
        output_configurations = _extract_outputs(output_variable_names, output_variable_types)

        input_signature = _generate_method_signature(input_configurations)

        input_param_names = _get_input_names(input_configurations)
        output_param_types = _get_ouput_types(output_configurations)

        migrated_file_directory = os.path.join(
            measurement_plugin_path,
            MIGRATED_MEASUREMENT_FILENAME,
        )

        add_parameter_to_method(
            migrated_file_directory,
            method_name,
            "reservation",
        )
        session_details = replace_session_initialization(
            migrated_file_directory,
            method_name,
            _drivers,
        )
        for driver_name, param_value, actual_name in session_details:
            instrument_type = driver_name
            resource_name = param_value
            actual_session_name = actual_name

        insert_session_assigning(
            migrated_file_directory,
            method_name,
            actual_session_name + " = session_info.session",
        )

        nims_instrument = _get_nims_instrument(instrument_type)

        service_class = f"{display_name}_Python"
        display_name_for_filenames = re.sub(r"\s+", "", display_name)
        serviceconfig_file = os.path.join(
            measurement_plugin_path,
            f"{display_name_for_filenames}.serviceconfig",
        )

        logger.debug(UserMessages.MEASUREMENT_FILE_CREATED)
        _create_file(
            TemplateFile.MEASUREMENT_TEMPLATE,
            os.path.join(measurement_plugin_path, TemplateFile.MEASUREMENT_FILENAME),
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
            method_name=method_name,
            directory_out=measurement_plugin_path,
            tuple_of_output=tuple_of_output,
        )
        logger.debug(UserMessages.SERVICE_CONFIG_CREATED)
        _create_file(
            TemplateFile.SERVICE_CONFIG_TEMPLATE,
            serviceconfig_file,
            display_name=display_name,
            service_class=service_class,
            directory_out=measurement_plugin_path,
        )
        logger.debug(UserMessages.BATCH_FILE_CREATED)
        _create_file(
            TemplateFile.BATCH_TEMPLATE,
            os.path.join(measurement_plugin_path, TemplateFile.BATCH_FILENAME),
            directory_out=measurement_plugin_path,
        )
        logger.debug(UserMessages.HELPER_FILE_CREATED)
        _create_file(
            TemplateFile.HELPER_TEMPLATE,
            os.path.join(measurement_plugin_path, TemplateFile.HELPER_FILENAME),
            directory_out=measurement_plugin_path,
        )
        logger.info(
            UserMessages.MEASUREMENT_PLUGIN_CREATED.format(file_dir=measurement_plugin_path)
        )

    except ClickException:
        logger.error(UserMessages.TEMPLATE_ERROR)

    except (PermissionError, OSError):
        logger.error(UserMessages.ACCESS_DENIED)

    except Exception as error:
        logger.debug(error)
        logger.error(UserMessages.CHECK_LOG_FILE)

    finally:
        logger.info(UserMessages.PROCESS_COMPLETED)


def __add_file_handler(output_path: str, logger: Logger) -> Tuple[Logger, str]:
    log_folder_path = output_path
    add_file_handler(logger=logger, log_folder_path=log_folder_path)
    logger.debug(UserMessages.VERSION.format(version=__version__))

    return logger, log_folder_path


def __initialize_logger(name: str, folder_path: str) -> Tuple[Logger, str]:
    logger = initialize_logger(name=name)

    if folder_path:
        logger, folder_path = __add_file_handler(output_path=folder_path, logger=logger)

    add_stream_handler(logger=logger)

    return logger, folder_path


def _extract_inputs(inputs):
    input_data = []

    for param_name, param_info in inputs.items():
        input_type = _to_nims_type(param_info["type"])
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
        output_type = _to_nims_type(return_type)
        output_data.append({"name": var_name, "actual_type": return_type, "type": output_type})

    return output_data


# To Enum
def _to_nims_type(type):
    if type == "int":
        return "nims.DataType.Int32"
    elif type == "bool":
        return "nims.DataType.Boolean"
    elif type == "float":
        return "nims.DataType.Double"
    elif type == "List[float]":
        return "nims.DataType.FloatArray1D"
    else:
        raise click.BadParameter("Invalid parameter")


def _generate_method_signature(inputs):
    parameter_info = []
    for input_param in inputs:
        parameter_info.append(f"{input_param['name']}:{input_param['actual_type']}")

    return ", ".join(parameter_info)


def _get_input_names(inputs):
    parameter_names = [param["name"] for param in inputs]
    return ", ".join(parameter_names)


def _get_ouput_types(outputs):
    parameter_types = []
    for param in outputs:
        parameter_types.append(param["actual_type"])
    return ", ".join(parameter_types)


# To Enum
def _get_nims_instrument(instrument_type):
    if instrument_type == "nidcpower":
        return "nims.session_management.INSTRUMENT_TYPE_NI_DCPOWER"
    else:
        raise click.BadParameter("Invalid instrument")


def _create_file(
    template_name: str,
    file_name: str,
    directory_out: pathlib.Path,
    **template_args: Any,
) -> None:
    output = _render_template(template_name, **template_args)

    with open(file_name, "wb") as f:
        f.write(output)


def _render_template(template_name: str, **template_args: Any) -> bytes:
    file_dir = str(pathlib.Path(__file__).parent / "templates" / template_name)

    template = Template(filename=file_dir, input_encoding="utf-8", output_encoding="utf-8")
    try:
        return template.render(**template_args)
    except Exception as e:
        raise e
