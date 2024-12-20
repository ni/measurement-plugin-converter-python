"""Implementation of command line interface of Measurement Plug-in UI Creator."""

from pathlib import Path
from typing import Callable

import click

from ni_measurement_plugin_ui_creator.utils.create_measui import create_measui
from ni_measurement_plugin_ui_creator.utils.exceptions import InvalidCliInputError
from ni_measurement_plugin_ui_creator.utils.logger import get_logger
from ni_measurement_plugin_ui_creator.utils.measui_file import get_metadata_and_service_class
from ni_measurement_plugin_ui_creator.utils.update_measui import update_measui

CLI_CONTEXT_SETTINGS = {"help_option_names": ["-h", "--help"]}
ERROR_OCCURRED = "Error occurred. Please find the log file at {log_file}."
GET_ACTIVE_MEASUREMENTS = "Getting the active measurements..."
PROCESS_COMPLETED = "Process completed."
START_CLI = "Starting the NI Measurement Plug-In UI Creator..."
SUPPORTED_ELEMENTS = "Supported UI Elements: {elements}"
SUPPORTED_UI_ELEMENTS = [
    "Boolean Horizontal Slider",
    "Boolean Round LED",
    "Numeric Array Input",
    "Numeric Array Output",
    "Numeric Control",
    "Numeric Indicator",
    "Pin",
    "String Array Input",
    "String Array Output",
    "String Control",
    "String Indicator",
]


def _create_or_update_ui(process_func: Callable) -> None:
    """Create or update `measui` file."""
    try:
        output_dir = Path.cwd()
        log_file_path = Path(output_dir) / "ui_creator_logs"
        logger = get_logger(log_file_path=log_file_path)

        logger.info(START_CLI)
        logger.info(SUPPORTED_ELEMENTS.format(elements=SUPPORTED_UI_ELEMENTS))

        logger.info(GET_ACTIVE_MEASUREMENTS)
        metadata_and_service_class = get_metadata_and_service_class()

        if not metadata_and_service_class:
            return

        process_func(metadata_and_service_class[0], metadata_and_service_class[1], output_dir)

    except InvalidCliInputError as error:
        logger.error(error)

    except Exception as error:
        logger.debug(error, exc_info=True)
        logger.info(ERROR_OCCURRED.format(log_file=log_file_path / "log.txt"))

    finally:
        logger.info(PROCESS_COMPLETED)


@click.command(name="create")
def _create() -> None:
    """Create a new measurement UI file."""
    _create_or_update_ui(create_measui)


@click.command(name="update")
def _update() -> None:
    """Update the measurement UI file."""
    _create_or_update_ui(update_measui)


@click.group(context_settings=CLI_CONTEXT_SETTINGS)
def start() -> None:
    """Creates or updates .measui file for Python Measurement plug-ins."""
    pass


start.add_command(_create)
start.add_command(_update)
