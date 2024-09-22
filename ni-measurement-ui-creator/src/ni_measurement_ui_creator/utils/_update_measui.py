"""Implementation of update meas UI."""

import os
import shutil
import xml.etree.ElementTree as ETree
from logging import getLogger
from pathlib import Path
from typing import List, Union

from ni_measurement_plugin_sdk_service._internal.stubs.ni.measurementlink.measurement.v1.measurement_service_pb2 import (
    GetMetadataResponse as V1MetaData,
)
from ni_measurement_plugin_sdk_service._internal.stubs.ni.measurementlink.measurement.v2.measurement_service_pb2 import (
    GetMetadataResponse as V2MetaData,
)

from ni_measurement_ui_creator.constants import (
    LOGGER,
    NAMESPACES,
    NUMERIC_DATA_TYPE_VALUES,
    UserMessage,
)
from ni_measurement_ui_creator.models import AvlbleElement
from ni_measurement_ui_creator.utils._create_measui import create_measui
from ni_measurement_ui_creator.utils._exceptions import InvalidMeasUIError
from ni_measurement_ui_creator.utils._measui_file import (
    get_avlble_elements,
    get_measui_files,
    get_measui_selection,
    validate_measui,
)


def update_measui(metadata: Union[V1MetaData, V2MetaData], output_dir: Path) -> None:
    """Update measurment UI.

    1. Get measurement files of the selected measurement plug-in.
    2. Get the measurement UI to be updated.
    3. Create a copy.
    4. Bind elements.
    5. Create elements.

    Args:
        metadata (Union[V1MetaData, V2MetaData]): Metadata of the measurement plug-in.
        output_dir (Path): Output directory where updated measurement UI is outputted.
    """
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
        tree = ETree.parse(selected_measui)
        validate_measui(tree)

    except (ETree.ParseError, InvalidMeasUIError, FileNotFoundError, PermissionError):
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

    inputs = metadata.measurement_signature.configuration_parameters
    outputs = metadata.measurement_signature.outputs

    elements = get_avlble_elements(tree)
    elements_names = [element.name for element in elements]

    unbind_inputs = [input for input in inputs if input.name not in elements_names]
    unbind_outputs = [output for output in outputs if output.name not in elements_names]

    # Call bind elements.
    # Call create elements.
    # Call write_updated_measui

    return


accepted_datatypes = {}


def bind_elements(elements: List[AvlbleElement], unbind_inputs, unbind_output):
    for unbind_input in unbind_inputs:
        if unbind_input.data in NUMERIC_DATA_TYPE_VALUES:
            ...


def bind_inputs(): ...


def write_updated_measui(filepath, updated_ui):
    tree = ETree.parse(filepath)
    root = tree.getroot()
    screen = root.find(f".//sf:Screen", NAMESPACES)
    screen_surface = screen.find(f"cf:ScreenSurface", NAMESPACES)
    screen.remove(screen_surface)
    screen.append(updated_ui)

    tree.write(filepath, encoding="utf-8", xml_declaration=True)
