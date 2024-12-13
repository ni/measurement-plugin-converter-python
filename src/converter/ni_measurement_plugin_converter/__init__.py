"""Implementation of command line interface and measurement plug-in conversion."""

__version__ = "1.0.0"

import ast
import re
import shutil
from pathlib import Path
from typing import Any, Dict

import click
from click import ClickException
from mako.exceptions import CompileException, TemplateLookupException

from ni_measurement_plugin_converter._constants import (
    ACCESS_DENIED,
    ALPHANUMERIC_PATTERN,
    DEBUG_LOGGER,
    ENCODING,
)
from ni_measurement_plugin_converter._utils import (
    create_file,
    create_measui_file,
    extract_inputs,
    extract_outputs,
    get_function_node,
    initialize_logger,
    print_log_file_location,
    process_sessions_and_update_metadata,
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

MEASUREMENT_VERSION = "1.0.0.0"

MEASUREMENT_FILE_PATH_OPTION = "--measurement-file-path"

INVALID_FILE_DIR = (
    "Invalid measurement file directory. Please provide valid measurement file directory."
)
FUNCTION_NOT_FOUND = "Measurement function {function} not found in the file {measurement_file_path}"


def _validate_measurement_file(file_path: Path):
    if not file_path.exists() or not file_path.is_file():
        raise click.BadParameter(INVALID_FILE_DIR)


def _validate_function(function_name: str, measurement_file_path: Path):
    with measurement_file_path.open("r", encoding=ENCODING) as file:
        code = file.read()
    code_tree = ast.parse(code)

    if not any(
        isinstance(node, ast.FunctionDef) and node.name == function_name
        for node in ast.walk(code_tree)
    ):
        raise click.BadParameter(
            FUNCTION_NOT_FOUND.format(
                function=function_name, measurement_file_path=measurement_file_path
            )
        )


def _validate_output_directory(output_dir: Path):
    try:
        output_dir.mkdir(parents=True, exist_ok=True)
    except PermissionError:
        raise click.BadParameter(
            "Permission denied: Unable to create or access the output directory."
        )
    except OSError as e:
        raise click.BadParameter(f"An error occurred: {e}")


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
    help="Path of the Python measurement file to be converted.",
    required=True,
)
@click.option(
    "-f",
    "--function",
    help="Name of the function in the measurement file that contains the logic for the measurement.",
    required=True,
)
@click.option(
    "-o",
    "--directory-out",
    help="Output directory for measurement plug-in files.",
    required=True,
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

        directory_out_path = Path(directory_out)

        _validate_measurement_file(Path(measurement_file_path))
        _validate_function(function, Path(measurement_file_path))
        _validate_output_directory(directory_out_path)

        remove_handlers(logger)

        log_directory = directory_out
        logger = initialize_logger(name=DEBUG_LOGGER, log_directory=log_directory)
        logger.debug(VERSION.format(version=__version__))

        logger.info(VALIDATE_CLI_ARGS)

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
        inputs_info = extract_inputs(function_node, plugin_metadata)

        logger.info(EXTRACT_OUTPUT_INFO)
        outputs_info = extract_outputs(function_node, plugin_metadata)

        pins_info, relays_info = process_sessions_and_update_metadata(
            migrated_file_path, function, plugin_metadata, logger
        )

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
            file_path=directory_out_path,
            measurement_name=sanitized_display_name,
            service_class=f"{sanitized_display_name}_Python",
        )
        logger.debug(MEASUI_FILE_CREATED)

        create_file(
            SERVICE_CONFIG_TEMPLATE,
            directory_out_path / f"{sanitized_display_name}{SERVICE_CONFIG_FILE_EXTENSION}",
            display_name=sanitized_display_name,
            service_class=f"{sanitized_display_name}_Python",
            version=MEASUREMENT_VERSION,
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
