"""Implementation of command line interface and measurement plug-in conversion."""

__version__ = "1.0.0-dev8"

import re
import shutil
from pathlib import Path
from typing import Any, Dict, List, Union

import click
from click import ClickException
from mako.exceptions import CompileException, TemplateLookupException

from ni_measurement_plugin_converter._constants import (
    ACCESS_DENIED,
    ALPHANUMERIC_PATTERN,
    DEBUG_LOGGER,
)
from ni_measurement_plugin_converter._models import CliInputs, PinInfo, RelayInfo
from ni_measurement_plugin_converter._utils import (
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

CONTEXT_SETTINGS = {"help_option_names": ["-h", "--help"]}

STARTING_EXECUTION = "Starting NI Measurement Plug-In Converter..."
VERSION = "NI Measurement Plug-In Converter - {version}"
PROCESS_COMPLETED = "Process completed."
ERROR_OCCURRED = (
    "Error occurred. Please verify that the provided measurement is in the expected format."
)
MEASUREMENT_PLUGIN_CREATED = "Measurement plug-in is created at {plugin_dir}"
MEASUI_FILE_CREATED = "Measurement UI file is created."
MEASUREMENT_FILE_CREATED = "Measurement file is created."
FILE_MIGRATED = "Migrated file is created."
BATCH_FILE_CREATED = "Batch file is created."
HELPER_FILE_CREATED = "Helper file is created."
SERVICE_CONFIG_CREATED = "Service config is created."
GET_FUNCTION = "Getting function node tree..."
VALIDATE_CLI_ARGS = "Inputs validated successfully."
EXTRACT_INPUT_INFO = "Extracting inputs information from measurement function..."
EXTRACT_OUTPUT_INFO = "Extracting outputs information from measurement function..."
DEFINE_PINS_RELAYS = "Defining pins and relays..."
ADD_SESSION_MAPPING = "Adding session mapping..."
ADD_SESSION_INITIALIZATION = "Adding session initialization..."
LOG_FILE = "Please find the log file at {log_file_path}"

MEASUREMENT_TEMPLATE = "measurement.py.mako"
MEASUREMENT_FILENAME = "measurement.py"
HELPER_TEMPLATE = "_helpers.py.mako"
HELPER_FILENAME = "_helpers.py"
SERVICE_CONFIG_TEMPLATE = "measurement.serviceconfig.mako"
SERVICE_CONFIG_FILE_EXTENSION = ".serviceconfig"
BATCH_TEMPLATE = "start.bat.mako"
BATCH_FILENAME = "start.bat"
MIGRATED_MEASUREMENT_FILENAME = "_migrated.py"

MEASUREMENT_VERSION = 1.0

MEASUREMENT_FILE_PATH_OPTION = "--measurement-file-path"


@click.command(context_settings=CONTEXT_SETTINGS)
@click.option(
    "-d",
    "--display-name",
    help="Display name for the plug-in that will be converted.",
    required=True,
)
@click.option(
    "-m",
    MEASUREMENT_FILE_PATH_OPTION,
    help="Path to the directory containing the Python measurement file to be converted.",
    required=True,
)
@click.option(
    "-f",
    "--function",
    help=f"Name of the function within the measurement file {MEASUREMENT_FILE_PATH_OPTION} that contains the measurement logic.",
    required=True,
)
@click.option(
    "-o", "--directory-out", help="Output directory for measurement plug-in files.", required=True
)
def convert_to_plugin(
    display_name: str,
    measurement_file_path: str,
    function: str,
    directory_out: str,
) -> None:
    """Convert Python measurements to Python Measurement plug-ins."""
    try:
        log_directory = None
        logger = initialize_logger(name="console_logger", log_directory=log_directory)
        logger.info(STARTING_EXECUTION)

        CliInputs(
            display_name=display_name,
            measurement_file_dir=measurement_file_path,
            function=function,
            output_dir=directory_out,
        )

        remove_handlers(logger)

        log_directory = directory_out
        logger = initialize_logger(name=DEBUG_LOGGER, log_directory=log_directory)
        logger.debug(VERSION.format(version=__version__))

        logger.info(VALIDATE_CLI_ARGS)

        directory_out_path = Path(directory_out)
        migrated_file_path = directory_out_path / MIGRATED_MEASUREMENT_FILENAME
        shutil.copy(Path(measurement_file_path), migrated_file_path)
        logger.debug(FILE_MIGRATED)

        logger.debug(GET_FUNCTION)
        function_node = get_function_node(
            file_dir=str(Path(measurement_file_path)), function=function
        )

        plugin_metadata: Dict[str, Any] = {}

        sanitized_display_name = re.sub(ALPHANUMERIC_PATTERN, "_", display_name)
        plugin_metadata["display_name"] = sanitized_display_name

        logger.info(EXTRACT_INPUT_INFO)
        inputs_info = extract_inputs(function_node)
        plugin_metadata["inputs_info"] = inputs_info
        plugin_metadata["input_param_names"] = generate_input_params(inputs_info)
        plugin_metadata["input_signature"] = generate_input_signature(inputs_info)

        logger.info(EXTRACT_OUTPUT_INFO)
        outputs_info, iterable_outputs = extract_outputs(function_node)
        plugin_metadata["outputs_info"] = outputs_info
        plugin_metadata["output_signature"] = generate_output_signature(outputs_info)
        plugin_metadata["iterable_outputs"] = iterable_outputs

        sessions_details = manage_session(str(migrated_file_path), function)

        logger.info(DEFINE_PINS_RELAYS)
        pins_info, relays_info = get_pins_and_relays_info(sessions_details)
        plugin_metadata["pins_info"] = pins_info
        plugin_metadata["relays_info"] = relays_info

        pins_and_relays = pins_info[:] + relays_info
        plugin_metadata["pin_and_relay_signature"] = get_pin_and_relay_names_signature(
            pins_and_relays
        )
        plugin_metadata["pin_or_relay_names"] = get_pin_and_relay_names(pins_and_relays)

        logger.info(ADD_SESSION_MAPPING)
        session_mappings = get_session_mapping(sessions_details)
        plugin_metadata["session_mappings"] = session_mappings
        plugin_metadata["sessions"] = get_sessions_signature(session_mappings)

        logger.info(ADD_SESSION_INITIALIZATION)
        plugin_metadata["session_initializations"] = get_plugin_session_initializations(
            sessions_details
        )

        plugin_metadata["is_visa"] = check_for_visa(sessions_details)
        plugin_metadata["version"] = MEASUREMENT_VERSION
        plugin_metadata["serviceconfig_file"] = (
            f"{sanitized_display_name}{SERVICE_CONFIG_FILE_EXTENSION}"
        )
        plugin_metadata["migrated_file"] = migrated_file_path.stem
        plugin_metadata["function_name"] = function
        plugin_metadata["directory_out"] = str(directory_out_path)

        create_file(
            MEASUREMENT_TEMPLATE,
            directory_out_path / MEASUREMENT_FILENAME,
            **plugin_metadata,
        )
        logger.debug(MEASUREMENT_FILE_CREATED)

        create_measui_file(
            pins=pins_info,
            relays=relays_info,
            inputs=inputs_info,
            outputs=outputs_info,
            file_path=str(directory_out_path),
            measurement_name=sanitized_display_name,
        )
        logger.debug(MEASUI_FILE_CREATED)

        create_file(
            SERVICE_CONFIG_TEMPLATE,
            directory_out_path / f"{sanitized_display_name}{SERVICE_CONFIG_FILE_EXTENSION}",
            display_name=sanitized_display_name,
            service_class=f"{sanitized_display_name}_Python",
            directory_out=str(directory_out_path),
        )
        logger.debug(SERVICE_CONFIG_CREATED)

        create_file(
            BATCH_TEMPLATE,
            directory_out_path / BATCH_FILENAME,
            directory_out=str(directory_out_path),
        )
        logger.debug(BATCH_FILE_CREATED)

        create_file(
            HELPER_TEMPLATE,
            directory_out_path / HELPER_FILENAME,
            directory_out=str(directory_out_path),
        )
        logger.debug(HELPER_FILE_CREATED)

        logger.info(MEASUREMENT_PLUGIN_CREATED.format(plugin_dir=str(directory_out_path.resolve())))

    except PermissionError as error:
        logger.debug(error)
        logger.error(ACCESS_DENIED)
        print_log_file_location()

    except (
        FileNotFoundError,
        NameError,
        OSError,
        PermissionError,
        ClickException,
        TemplateLookupException,
        CompileException,
        ValueError,
    ) as error:
        logger.error(error)
        print_log_file_location()

    except Exception as error:
        logger.debug(error, exc_info=True)
        logger.error(ERROR_OCCURRED)
        print_log_file_location()

    finally:
        logger.info(PROCESS_COMPLETED)
