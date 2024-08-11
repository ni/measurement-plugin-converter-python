"""Implementation of command line interface and measurement plugin conversion."""

import os
import re
import shutil
from pathlib import Path

import click
from click import ClickException
from mako.exceptions import CompileException, TemplateLookupException

from ni_measurement_plugin_converter import __version__
from ni_measurement_plugin_converter.constants import (
    CONSOLE_LOGGER,
    CONTEXT_SETTINGS,
    DEBUG_LOGGER,
    MEASUREMENT_VERSION,
    MIGRATED_MEASUREMENT_FILENAME,
    ArgsDescription,
    DebugMessage,
    TemplateFile,
    UserMessage,
)
from ni_measurement_plugin_converter.models import CliInputs, InvalidCliArgsError
from ni_measurement_plugin_converter.utils import (
    create_file,
    extract_inputs,
    extract_outputs,
    generate_input_params,
    generate_input_signature,
    generate_output_signature,
    get_measurement_function,
    get_nims_instrument,
    initialize_logger,
    manage_session,
    print_logger_location,
    remove_handlers,
)


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
    """NI Measurement Plug-In Converter is a Command Line tool to convert \
        Python measurements to measurement plug-ins."""
    try:
        log_directory = None
        logger = initialize_logger(name=CONSOLE_LOGGER, log_directory=log_directory)
        logger.info(UserMessage.STARTING_EXECUTION)

        CliInputs(
            display_name=display_name,
            measurement_file_dir=measurement_file_dir,
            function=function,
            output_dir=output_dir,
        )

        remove_handlers(logger)

        log_directory = output_dir
        logger = initialize_logger(name=DEBUG_LOGGER, log_directory=log_directory)
        logger.debug(DebugMessage.VERSION.format(version=__version__))

        logger.info(UserMessage.VALIDATE_CLI_ARGS)

        migrated_file_dir = os.path.join(output_dir, MIGRATED_MEASUREMENT_FILENAME)
        shutil.copy(measurement_file_dir, migrated_file_dir)
        logger.debug(DebugMessage.FILE_MIGRATED)

        logger.debug(DebugMessage.GET_FUNCTION)
        function_node = get_measurement_function(measurement_file_dir, function)

        logger.info(UserMessage.EXTRACT_INPUT_INFO)

        inputs_info = extract_inputs(function_node)
        input_param_names = generate_input_params(inputs_info)
        input_signature = generate_input_signature(inputs_info)

        logger.info(UserMessage.EXTRACT_OUTPUT_INFO)

        outputs_info, iterable_outputs = extract_outputs(function_node)
        output_signature = generate_output_signature(outputs_info)

        # Manage session.
        instrument_type = manage_session(migrated_file_dir, function)

        nims_instrument = get_nims_instrument(instrument_type)
        service_class = f"{display_name}_Python"
        display_name_for_filenames = re.sub(r"\s+", "", display_name)

        create_file(
            TemplateFile.MEASUREMENT_TEMPLATE,
            os.path.join(output_dir, TemplateFile.MEASUREMENT_FILENAME),
            display_name=display_name,
            version=MEASUREMENT_VERSION,
            serviceconfig_file=(
                f"{display_name_for_filenames}{TemplateFile.SERVICE_CONFIG_FILE_EXTENSION}"
            ),
            instrument_type=instrument_type,
            nims_instrument=nims_instrument,
            inputs_info=inputs_info,
            outputs_info=outputs_info,
            input_signature=input_signature,
            input_param_names=input_param_names,
            output_signature=output_signature,
            migrated_file=Path(MIGRATED_MEASUREMENT_FILENAME).stem,
            function_name=function,
            directory_out=output_dir,
            iterable_outputs=iterable_outputs,
        )
        logger.debug(DebugMessage.MEASUREMENT_FILE_CREATED)

        create_file(
            TemplateFile.SERVICE_CONFIG_TEMPLATE,
            os.path.join(
                output_dir,
                f"{display_name_for_filenames}{TemplateFile.SERVICE_CONFIG_FILE_EXTENSION}",
            ),
            display_name=display_name,
            service_class=service_class,
            directory_out=output_dir,
        )
        logger.debug(DebugMessage.SERVICE_CONFIG_CREATED)

        create_file(
            TemplateFile.BATCH_TEMPLATE,
            os.path.join(output_dir, TemplateFile.BATCH_FILENAME),
            directory_out=output_dir,
        )
        logger.debug(DebugMessage.BATCH_FILE_CREATED)

        create_file(
            TemplateFile.HELPER_TEMPLATE,
            os.path.join(output_dir, TemplateFile.HELPER_FILENAME),
            directory_out=output_dir,
        )
        logger.debug(DebugMessage.HELPER_FILE_CREATED)

        logger.info(UserMessage.MEASUREMENT_PLUGIN_CREATED.format(plugin_dir=output_dir))

    except (
        InvalidCliArgsError,
        ClickException,
        TemplateLookupException,
        CompileException,
    ) as error:
        logger.error(error)
        print_logger_location(log_directory)

    except Exception as error:
        logger.debug(error, exc_info=True)
        logger.error(UserMessage.ERROR_OCCURRED)
        print_logger_location(log_directory)

    finally:
        logger.info(UserMessage.PROCESS_COMPLETED)
