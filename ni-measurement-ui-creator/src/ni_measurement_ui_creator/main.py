"""Command-line tool to create measui for measurements."""

import os
from pathlib import Path

import click

from ni_measurement_ui_creator.constants import SUPPORTED_UI_ELEMENTS, CliHelpMessage, UserMessage
from ni_measurement_ui_creator.utils._create_measui import create_measui
from ni_measurement_ui_creator.utils._exceptions import InvalidCliInputError
from ni_measurement_ui_creator.utils._logger import get_logger
from ni_measurement_ui_creator.utils._measui_file import get_metadata
from ni_measurement_ui_creator.utils._update_measui import update_measui


@click.command(name="update")
@click.option(
    "-o",
    "--output-dir",
    type=click.Path(),
    required=True,
    help=CliHelpMessage.OUTPUT_FOLDER,
)
def update(output_dir: Path) -> None:
    try:
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

    finally:
        logger.info(UserMessage.PROCESS_COMPLETED)


@click.command(name="create")
@click.option(
    "-o",
    "--output-dir",
    type=click.Path(),
    required=True,
    help=CliHelpMessage.OUTPUT_FOLDER,
)
def create(output_dir: Path) -> None:
    """NI Measurement UI Creator is a Command Line tool for creating measui files."""
    try:
        log_file_path = os.path.join(output_dir, "Logs")
        logger = get_logger(log_file_path=log_file_path)

        logger.info(UserMessage.CLI_STARTING)
        logger.info(UserMessage.SUPPORTED_ELEMENTS.format(elements=SUPPORTED_UI_ELEMENTS))
        logger.info(UserMessage.GET_ACTIVE_MEASUREMENTS)

        metadata = get_metadata()

        if not metadata:
            return

        create_measui(metadata, output_dir)

    except InvalidCliInputError as error:
        logger.error(error)

    except Exception as error:
        logger.debug(error, exc_info=True)

    finally:
        logger.info(UserMessage.PROCESS_COMPLETED)


@click.group()
def run() -> None:
    pass


run.add_command(create)
run.add_command(update)
