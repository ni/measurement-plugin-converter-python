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
    ArgsDescription,
    DebugMessage,
    TemplateFile,
    UserMessage,
)
from ni_measurement_plugin_converter.models import CliInputs, InvalidCliArgsError
from ni_measurement_plugin_converter.utils import (
    extract_inputs,
    extract_outputs,
    generate_input_params,
    generate_input_signature,
    generate_output_signature,
    get_measurement_function,
    get_nims_instrument,
    initialize_logger,
    remove_handlers,
    manage_session,
)

# Refactor
_drivers = ["nidcpower"]
instrument_type = ""
resource_name = ""
actual_session_name = ""


@click.command(context_settings=CONTEXT_SETTINGS)
@click.option("-d", "--display-name", help=ArgsDescription.DISPLAY_NAME, required=True)
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

        CliInputs(
            display_name=display_name,
            measurement_file_dir=measurement_file_dir,
            function=function,
            output_dir=output_dir,
        )

        remove_handlers(logger)
        logger = initialize_logger(name="debug_logger", log_directory=output_dir)
        logger.debug(DebugMessage.VERSION.format(version=__version__))

        logger.info(UserMessage.VALIDATE_CLI_ARGS)

        shutil.copy(measurement_file_dir, os.path.join(output_dir, MIGRATED_MEASUREMENT_FILENAME))
        logger.debug(DebugMessage.FILE_MIGRATED)

        logger.debug(DebugMessage.GET_FUNCTION)
        function_node = get_measurement_function(measurement_file_dir, function)

        logger.info(UserMessage.EXTRACT_INPUT_INFO)

        input_configurations = extract_inputs(function_node)
        input_param_names = generate_input_params(input_configurations)
        input_signature = generate_input_signature(input_configurations)

        logger.info(UserMessage.EXTRACT_OUTPUT_INFO)

        output_configurations, tuple_of_outputs = extract_outputs(function_node)
        output_param_types = generate_output_signature(output_configurations)

        logger.info(UserMessage.ADD_RESERVE_SESSION)

        migrated_file_dir = os.path.join(output_dir, MIGRATED_MEASUREMENT_FILENAME)
        instrument_type, resource_name = manage_session(migrated_file_dir, function_node, _drivers)

        logger.info(UserMessage.ADD_SESSION_INITIALIZATION)

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
            updated_file_name=f"{output_dir}.{Path(MIGRATED_MEASUREMENT_FILENAME).stem}",
            method_name=function,
            directory_out=output_dir,
            tuple_of_outputs=tuple_of_outputs,
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
        logger.error(UserMessage.ERROR_OCCURRED)
        logger.error(error)

    finally:
        logger.info(UserMessage.PROCESS_COMPLETED)


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
