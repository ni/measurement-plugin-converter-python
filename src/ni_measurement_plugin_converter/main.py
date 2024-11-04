"""Implementation of command line interface and measurement plug-in conversion."""

'''I don't know how good of an idea it is have both __main__.py and main.py.
Probably, this file should be renamed or this logic could be moved to __init__.py'''

import os
import re
import shutil
from pathlib import Path

import click
from click import ClickException
from mako.exceptions import CompileException, TemplateLookupException

from ni_measurement_plugin_converter import __version__
from ni_measurement_plugin_converter.constants import (
    ALPHANUMERIC_PATTERN,
    CONTEXT_SETTINGS,
    DEBUG_LOGGER,
    MEASUREMENT_VERSION,
    MIGRATED_MEASUREMENT_FILENAME,
    ArgsDescription,
    DebugMessage,
    TemplateFile,
    UserMessage,
)
from ni_measurement_plugin_converter.models import (
    CliInputs,
    InvalidCliArgsError,
    UnsupportedDriverError,
)
from ni_measurement_plugin_converter.utils import (
    check_for_visa,
    create_file,
    create_measui_file,
    extract_inputs,
    extract_outputs,
    generate_input_params,
    generate_input_signature,
    generate_output_signature,
    get_function_node,
    get_pin_and_relay_names,
    get_pin_and_relay_names_signature,
    get_pins_and_relays_info,
    get_plugin_session_initializations,
    get_session_mapping,
    get_sessions_signature,
    initialize_logger,
    manage_session,
    print_log_file_location,
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
@click.option("-o", "--output-dir", help=ArgsDescription.OUTPUT_DIR, required=True) # directory-out is more conventional
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
        logger = initialize_logger(name="console_logger", log_directory=log_directory)
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

        # Use pathlib for Path operation.
        migrated_file_dir = os.path.join(output_dir, MIGRATED_MEASUREMENT_FILENAME)
        shutil.copy(measurement_file_dir, migrated_file_dir)
        logger.debug(DebugMessage.FILE_MIGRATED)

        logger.debug(DebugMessage.GET_FUNCTION)
        function_node = get_function_node(file_dir=measurement_file_dir, function=function)

        logger.info(UserMessage.EXTRACT_INPUT_INFO)

        inputs_info = extract_inputs(function_node)
        input_param_names = generate_input_params(inputs_info)
        input_signature = generate_input_signature(inputs_info)

        logger.info(UserMessage.EXTRACT_OUTPUT_INFO)

        outputs_info, iterable_outputs = extract_outputs(function_node)
        output_signature = generate_output_signature(outputs_info)

        # Manage session.
        sessions_details = manage_session(migrated_file_dir, function)

        logger.info(UserMessage.DEFINE_PINS_RELAYS)

        pins_info, relays_info = get_pins_and_relays_info(sessions_details)

        pins_and_relays = pins_info[:]
        pins_and_relays.extend(relays_info)

        pin_and_relay_signature = get_pin_and_relay_names_signature(pins_and_relays)
        pin_or_relay_names = get_pin_and_relay_names(pins_and_relays)

        logger.info(UserMessage.ADD_SESSION_MAPPING)

        session_mappings = get_session_mapping(sessions_details)
        sessions = get_sessions_signature(session_mappings)

        logger.info(UserMessage.ADD_SESSION_INITIALIZATION)

        plugin_session_initializations = get_plugin_session_initializations(sessions_details)

        is_visa = check_for_visa(sessions_details)

        sanitized_display_name = re.sub(ALPHANUMERIC_PATTERN, "_", display_name)
        service_class = f"{sanitized_display_name}_Python"

        # Use pathlib for Path operation.
        create_file(
            TemplateFile.MEASUREMENT_TEMPLATE,
            os.path.join(output_dir, TemplateFile.MEASUREMENT_FILENAME),
            display_name=sanitized_display_name,
            pins_info=pins_info,
            relays_info=relays_info,
            session_mappings=session_mappings,
            session_initializations=plugin_session_initializations,
            pin_and_relay_signature=pin_and_relay_signature,
            pin_or_relay_names=pin_or_relay_names,
            sessions=sessions,
            version=MEASUREMENT_VERSION,
            serviceconfig_file=(
                f"{sanitized_display_name}{TemplateFile.SERVICE_CONFIG_FILE_EXTENSION}"
            ),
            inputs_info=inputs_info,
            outputs_info=outputs_info,
            input_signature=input_signature,
            input_param_names=input_param_names,
            output_signature=output_signature,
            is_visa=is_visa,
            migrated_file=Path(MIGRATED_MEASUREMENT_FILENAME).stem,
            function_name=function,
            directory_out=output_dir,
            iterable_outputs=iterable_outputs,
        )
        logger.debug(DebugMessage.MEASUREMENT_FILE_CREATED)

        create_measui_file(
            pins=pins_info,
            relays=relays_info,
            inputs=inputs_info,
            outputs=outputs_info,
            file_path=output_dir,
            measurement_name=sanitized_display_name,
        )
        logger.debug(DebugMessage.MEASUI_FILE_CREATED)

        create_file(
            TemplateFile.SERVICE_CONFIG_TEMPLATE,
            os.path.join( # Use pathlib for Path operation.
                output_dir,
                f"{sanitized_display_name}{TemplateFile.SERVICE_CONFIG_FILE_EXTENSION}",
            ),
            display_name=sanitized_display_name,
            service_class=service_class,
            directory_out=output_dir,
        )
        logger.debug(DebugMessage.SERVICE_CONFIG_CREATED)

        create_file(
            TemplateFile.BATCH_TEMPLATE,
            os.path.join(output_dir, TemplateFile.BATCH_FILENAME), # Use pathlib for Path operation.
            directory_out=output_dir,
        )
        logger.debug(DebugMessage.BATCH_FILE_CREATED)

        create_file(
            TemplateFile.HELPER_TEMPLATE,
            os.path.join(output_dir, TemplateFile.HELPER_FILENAME), # Use pathlib for Path operation.
            directory_out=output_dir,
        )
        logger.debug(DebugMessage.HELPER_FILE_CREATED)

        logger.info(
            UserMessage.MEASUREMENT_PLUGIN_CREATED.format(plugin_dir=os.path.abspath(output_dir)) # Use pathlib for Path operation.
        )

    except PermissionError as error:
        logger.debug(error)
        logger.error(UserMessage.ACCESS_DENIED)
        print_log_file_location()

    except (
        InvalidCliArgsError,
        ClickException,
        TemplateLookupException,
        CompileException,
        UnsupportedDriverError,
    ) as error:
        logger.error(error)
        print_log_file_location()

    except Exception as error:
        logger.debug(error, exc_info=True)
        logger.error(UserMessage.ERROR_OCCURRED)
        print_log_file_location()

    finally:
        logger.info(UserMessage.PROCESS_COMPLETED)
