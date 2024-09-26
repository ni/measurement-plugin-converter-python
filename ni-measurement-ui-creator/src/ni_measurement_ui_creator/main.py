"""Command-line tool to create measui for measurements."""

import os

import click

from ni_measurement_ui_creator.constants import (
    CLI_CONTEXT_SETTINGS,
    SUPPORTED_UI_ELEMENTS,
    UserMessage,
)
from ni_measurement_ui_creator.utils._create_measui import _create_measui
from ni_measurement_ui_creator.utils._exceptions import InvalidCliInputError
from ni_measurement_ui_creator.utils._logger import get_logger
from ni_measurement_ui_creator.utils._measui_file import get_metadata
from ni_measurement_ui_creator.utils._update_measui import update_measui


@click.command(name="create")
def create() -> None:
    """Create a new measurement UI file."""
    try:
        output_dir = os.getcwd()
        log_file_path = os.path.join(output_dir, "Logs")
        logger = get_logger(log_file_path=log_file_path)

        logger.info(UserMessage.CLI_STARTING)
        logger.info(UserMessage.SUPPORTED_ELEMENTS.format(elements=SUPPORTED_UI_ELEMENTS))

        logger.info(UserMessage.GET_ACTIVE_MEASUREMENTS)
        metadata = get_metadata()

        if not metadata:
            return

        _create_measui(metadata, output_dir)

    except InvalidCliInputError as error:
        logger.error(error)

    except Exception as error:
        logger.debug(error, exc_info=True)
        logger.info(UserMessage.ERROR_OCCURRED.format(log_file=logger.handlers[0].baseFilename))

    finally:
        logger.info(UserMessage.PROCESS_COMPLETED)


@click.command(name="update")
def update() -> None:
    """Update the measurement UI file."""
    try:
        output_dir = os.getcwd()
        log_file_path = os.path.join(output_dir, "Logs")
        logger = get_logger(log_file_path=log_file_path)

        logger.info(UserMessage.CLI_STARTING)
        logger.info(UserMessage.SUPPORTED_ELEMENTS.format(elements=SUPPORTED_UI_ELEMENTS))

        logger.info(UserMessage.GET_ACTIVE_MEASUREMENTS)
        metadata = get_metadata()

        if not metadata:
            return

        update_measui(metadata, output_dir)

    except InvalidCliInputError as error:
        logger.error(error)

    except Exception as error:
        logger.debug(error, exc_info=True)
        logger.info(UserMessage.ERROR_OCCURRED.format(log_file=logger.handlers[0].baseFilename))

    finally:
        logger.info(UserMessage.PROCESS_COMPLETED)


@click.group(context_settings=CLI_CONTEXT_SETTINGS)
def run() -> None:
    """NI Measurement UI Creator is a Command Line tool for creating/updating measui files."""
    pass


run.add_command(create)
run.add_command(update)
