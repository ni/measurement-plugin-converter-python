"""Implementation of update meas UI."""

import os
import shutil
import xml.etree.ElementTree as ET
from logging import getLogger
from pathlib import Path

from ni_measurement_ui_creator.constants import LOGGER, UserMessage
from ni_measurement_ui_creator.utils._create_measui import create_measui
from ni_measurement_ui_creator.utils._exceptions import InvalidCliInputError, InvalidMeasUIError
from ni_measurement_ui_creator.utils._measui_file import (
    get_controls_and_indicators,
    get_measui_files,
    validate_measui,
)


def update_measui(metadata, output_dir):
    logger = getLogger(LOGGER)

    measui_files = get_measui_files(metadata)
    if not measui_files:
        logger.warning(UserMessage.NO_MEASUI_FILE)
        create_measui(metadata, output_dir)
        return

    logger.info(UserMessage.AVAILABLE_MEASUI_FILES)
    for serial_num, measui_file_path in enumerate(measui_files):
        logger.info(f"{serial_num + 1}. {measui_file_path[1:]}")

    selected_measui = measui_files[get_measui_selection(len(measui_files)) - 1][1:]

    try:
        tree = ET.parse(selected_measui)
        validate_measui(tree)
    except (ET.ParseError, InvalidMeasUIError, FileNotFoundError, PermissionError):
        logger.warning(UserMessage.INVALID_MEASUI_FILE)
        create_measui(metadata, output_dir)
        return

    shutil.copy(
        selected_measui,
        os.path.join(
            output_dir,
            str(Path(Path(selected_measui).name).stem) + "_updated.measui",
        ),
    )
    controls_and_indicators = get_controls_and_indicators(tree)

    inputs = metadata.measurement_signature.configuration_parameters
    outputs = metadata.measurement_signature.outputs

    bound_inputs_outputs = [element.name for element in controls_and_indicators]

    unbound_inputs, unbound_outputs = [], []

    for input in inputs:
        if input.name not in bound_inputs_outputs:
            unbound_inputs.append(input)

    for output in outputs:
        if output.name not in bound_inputs_outputs:
            unbound_outputs.append(output)


def get_measui_selection(total_uis: int) -> int:
    try:
        user_input = int(
            input(
                UserMessage.SELECT_MEASUI_FILE.format(
                    start=1,
                    end=total_uis,
                )
            )
        )

        if user_input not in list(range(1, total_uis + 1)):
            raise InvalidCliInputError(UserMessage.INVALID_MEASUI_CHOICE)

        return user_input

    except ValueError:
        raise InvalidCliInputError(UserMessage.ABORTED)
