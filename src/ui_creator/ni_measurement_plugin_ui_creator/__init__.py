"""Command-line tool to create measui for measurements."""

from pathlib import Path
from typing import Callable

import click

from ni_measurement_plugin_ui_creator.utils.create_measui import create_measui
from ni_measurement_plugin_ui_creator.utils.exceptions import InvalidCliInputError
from ni_measurement_plugin_ui_creator.utils.logger import get_logger
from ni_measurement_plugin_ui_creator.utils.measui_file import get_metadata
from ni_measurement_plugin_ui_creator.utils.update_measui import update_measui

START_CLI = "Starting the NI Measurement UI Creator..."
SUPPORTED_ELEMENTS = "Supported UI Elements: {elements}"
SUPPORTED_UI_ELEMENTS = [
    "Numeric Indicator",
    "Numeric Control",
    "Numeric Array Input",
    "Numeric Array Output",
    "Boolean Horizontal Slider",
    "Boolean Round LED",
    "String Control",
    "String Indicator",
    "String Array Input",
    "String Array Output",
    "Pin",
]
CLI_CONTEXT_SETTINGS = {"help_option_names": ["-h", "--help"]}
GET_ACTIVE_MEASUREMENTS = "Getting the active measurements..."
ERROR_OCCURRED = "Error occurred. Please find the log file at {log_file}"
PROCESS_COMPLETED = "Process completed."


def perform_ui_action(process_func: Callable) -> None:
    """Create or update `measui` file.

    Args:
        process_func (Callable): Create or update function.
    """
    try:
        output_dir = Path.cwd()
        log_file_path = Path(output_dir) / "ui_creator_logs"
        logger = get_logger(log_file_path=log_file_path)

        logger.info(START_CLI)
        logger.info(SUPPORTED_ELEMENTS.format(elements=SUPPORTED_UI_ELEMENTS))

        logger.info(GET_ACTIVE_MEASUREMENTS)
        metadata = get_metadata()

        if not metadata:
            return

        process_func(metadata, output_dir)

    except InvalidCliInputError as error:
        logger.error(error)

    except Exception as error:
        logger.debug(error, exc_info=True)
        logger.info(ERROR_OCCURRED.format(log_file=log_file_path / "log.txt"))

    finally:
        logger.info(PROCESS_COMPLETED)


@click.command(name="create")
def create() -> None:
    """Create a new measurement UI file."""
    perform_ui_action(create_measui)


@click.command(name="update")
def update() -> None:
    """Update the measurement UI file."""
    perform_ui_action(update_measui)


@click.group(context_settings=CLI_CONTEXT_SETTINGS)
def execute_cli() -> None:
    """NI Measurement UI Creator is a Command Line tool for creating/updating measui files."""
    pass


execute_cli.add_command(create)
execute_cli.add_command(update)
