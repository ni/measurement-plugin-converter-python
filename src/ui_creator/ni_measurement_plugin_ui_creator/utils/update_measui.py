"""Implementation of update measurement plug-in UI."""

import re
import shutil
import xml.etree.ElementTree as ETree  # nosec: B405
from logging import getLogger
from pathlib import Path
from typing import List, Tuple, Union
from uuid import UUID

from ni_measurement_plugin_sdk_service._internal.stubs.ni.measurementlink.measurement.v1.measurement_service_pb2 import (
    ConfigurationParameter as V1ConfigParam,
    GetMetadataResponse as V1MetaData,
    Output as V1Output,
)
from ni_measurement_plugin_sdk_service._internal.stubs.ni.measurementlink.measurement.v2.measurement_service_pb2 import (
    ConfigurationParameter as V2ConfigParam,
    GetMetadataResponse as V2MetaData,
    Output as V2Output,
)

from ni_measurement_plugin_ui_creator.constants import (
    LOGGER,
    NUMERIC_DATA_TYPE_VALUES,
    TYPE_SPECIFICATION,
    DataType,
    ElementAttrib,
    MeasUIElementPosition,
    MeasUIFile,
    SpecializedDataType,
    UpdateUI,
)
from ni_measurement_plugin_ui_creator.models import AvailableElement
from ni_measurement_plugin_ui_creator.utils.common_elements import get_unique_id
from ni_measurement_plugin_ui_creator.utils.create_measui import create_measui
from ni_measurement_plugin_ui_creator.utils.exceptions import InvalidMeasUIError
from ni_measurement_plugin_ui_creator.utils.measui_file import (
    get_available_elements,
    get_measui_files,
    get_measui_selection,
    insert_created_elements,
    validate_measui,
    write_updated_measui,
)
from ni_measurement_plugin_ui_creator.utils.ui_elements import (
    create_input_elements_from_client,
    create_output_elements_from_client,
)

AVAILABLE_MEASUI_FILES = "Available Measurement Plug-In UI Files:"
BINDING_ELEMENTS = "Binding UI controls and indicators..."
CREATING_ELEMENTS = "Creating new controls and indicators..."
INPUTS_BOUND = "Inputs are bound successfully."
INVALID_MEASUI_FILE = "Invalid Measurement Plug-In UI file. Creating a new measui file for the selected measurement..."
NO_MEASUI_FILE = "No Measurement Plug-In UI file available. Creating a new measui file for the selected measurement..."
OUTPUTS_BOUND = "Outputs are bound successfully."
UPDATED_UI = "Measurement Plug-In UI updated successfully. Please find at {filepath}."


def update_measui(
    metadata: Union[V1MetaData, V2MetaData],
    service_class: str,
    output_dir: Path,
) -> None:
    """Update the measurment plug-in UI.

    Args:
        metadata: Metadata of the measurement plug-in.
        service_class: Service class name of the measurement plug-in.
        output_dir: Output directory where updated measurement UI is outputted.
    """
    logger = getLogger(LOGGER)

    measui_files = get_measui_files(metadata)
    if not measui_files:
        logger.warning(NO_MEASUI_FILE)
        create_measui(metadata, service_class, output_dir)
        return

    logger.info(AVAILABLE_MEASUI_FILES)
    for serial_num, measui_file_path in enumerate(measui_files):
        logger.info(f"{serial_num + 1}. {measui_file_path[1:]}")

    logger.info("")
    selected_measui = measui_files[get_measui_selection(len(measui_files)) - 1][1:]

    try:
        tree = ETree.parse(selected_measui)  # nosec: B314
        validate_measui(tree)

    except (ETree.ParseError, InvalidMeasUIError, FileNotFoundError, PermissionError):
        logger.warning(INVALID_MEASUI_FILE)
        create_measui(metadata, service_class, output_dir)
        return

    updated_measui_filepath = Path(output_dir) / (
        Path(selected_measui).stem + f"_updated{MeasUIFile.MEASUREMENT_UI_FILE_EXTENSION}"
    )

    shutil.copy(selected_measui, updated_measui_filepath)

    inputs = metadata.measurement_signature.configuration_parameters
    outputs = metadata.measurement_signature.outputs

    elements = get_available_elements(tree)
    elements_names = [element.name for element in elements]

    unbind_inputs = [input for input in inputs if input.name not in elements_names]
    unbind_outputs = [output for output in outputs if output.name not in elements_names]

    root = tree.getroot()
    screen = root.find(UpdateUI.SCREEN_TAG, UpdateUI.NAMESPACES)
    if screen is None:
        return None

    try:
        client_id = screen.attrib[ElementAttrib.CLIENT_ID]
    except KeyError:
        client_id = get_unique_id()

    logger.info(BINDING_ELEMENTS)
    updated_elements = _bind_elements(client_id, elements, unbind_inputs, unbind_outputs)

    write_updated_measui(updated_measui_filepath, updated_elements)

    updated_element_names = [element.name for element in updated_elements]
    top_alignment, left_alignment = _find_alignments(updated_elements)

    unmatched_inputs = [input for input in inputs if input.name not in updated_element_names]
    unmatched_outputs = [output for output in outputs if output.name not in updated_element_names]

    logger.info(CREATING_ELEMENTS)
    elements_representation = _create_elements(
        client_id,
        top_alignment,
        left_alignment,
        unmatched_inputs,
        unmatched_outputs,
    )

    insert_created_elements(updated_measui_filepath, elements_representation)
    logger.info(UPDATED_UI.format(filepath=Path(updated_measui_filepath).resolve()))

    return None


def _bind_elements(
    client_id: Union[str, UUID],
    elements: List[AvailableElement],
    unbind_inputs: List[Union[V1ConfigParam, V2ConfigParam]],
    unbind_outputs: List[Union[V1Output, V2Output]],
) -> List[AvailableElement]:
    updated_elements = _bind_inputs(client_id, elements, unbind_inputs)
    updated_elements = _bind_outputs(client_id, updated_elements, unbind_outputs)
    return updated_elements


def _bind_inputs(
    client_id: Union[str, UUID],
    elements: List[AvailableElement],
    unbind_inputs: List[Union[V1ConfigParam, V2ConfigParam]],
) -> List[AvailableElement]:
    logger = getLogger(LOGGER)

    for unbind_input in unbind_inputs:
        for index, element in enumerate(elements):
            if (
                element.bind is False
                and element.output is False
                and _check_feasibility(unbind_input, element)
            ):
                element = _add_channel(client_id, element, unbind_input)
                element.name = unbind_input.name
                element.bind = True
                elements = _update_lable(index, elements)
                break

    logger.debug(INPUTS_BOUND)
    return elements


def _bind_outputs(
    client_id: Union[str, UUID],
    elements: List[AvailableElement],
    unbind_outputs: List[Union[V1Output, V2Output]],
) -> List[AvailableElement]:
    logger = getLogger(LOGGER)

    for unbind_output in unbind_outputs:
        for index, element in enumerate(elements):
            if (
                element.bind is False
                and element.output is True
                and _check_feasibility(unbind_output, element)
            ):
                element = _add_channel(client_id, element, unbind_output)
                element.name = unbind_output.name
                element.bind = True
                elements = _update_lable(index, elements)
                break

    logger.debug(OUTPUTS_BOUND)
    return elements


def _check_feasibility(
    unbind_param: Union[V1ConfigParam, V2ConfigParam, V1Output, V2Output],
    element: AvailableElement,
) -> bool:
    if (
        unbind_param.type in NUMERIC_DATA_TYPE_VALUES
        and not unbind_param.repeated
        and element.tag in UpdateUI.NUMERIC_ELEMENTS
    ):
        return True

    if (
        unbind_param.type == DataType.Boolean.value
        and not unbind_param.repeated
        and element.tag in UpdateUI.BOOLEAN_ELEMENTS
    ):
        return True

    if (
        unbind_param.type == DataType.String.value
        and not unbind_param.repeated
        and not unbind_param.annotations
        and element.tag == "ChannelStringControl"
    ):
        return True

    if (
        unbind_param.type in NUMERIC_DATA_TYPE_VALUES
        and unbind_param.repeated
        and element.tag == UpdateUI.ARRAY_CONTAINER_ELEMENT
        and element.is_str_array is False
    ):
        return True

    if (
        unbind_param.annotations
        and (
            unbind_param.annotations[TYPE_SPECIFICATION] == SpecializedDataType.PIN.lower()
            or unbind_param.annotations[TYPE_SPECIFICATION]
            == SpecializedDataType.IORESOURCE.lower()
        )
        and element.tag == UpdateUI.PIN_ELEMENT
    ):
        return True

    if (
        unbind_param.type == DataType.String.value
        and unbind_param.repeated
        and not unbind_param.annotations
        and element.tag == UpdateUI.ARRAY_CONTAINER_ELEMENT
        and element.is_str_array
    ):
        return True

    return False


def _add_channel(
    client_id: Union[str, UUID],
    element: AvailableElement,
    unbind_param: Union[V1ConfigParam, V2ConfigParam, V1Output, V2Output],
) -> AvailableElement:
    if isinstance(unbind_param, V1ConfigParam) or isinstance(unbind_param, V2ConfigParam):
        channel = f"[string]{client_id}/Configuration/{unbind_param.name}"
    else:
        channel = f"[string]{client_id}/Output/{unbind_param.name}"

    element.element.attrib[ElementAttrib.CHANNEL] = channel
    return element


def _update_lable(index: int, elements: List[AvailableElement]) -> List[AvailableElement]:
    for label_index in range(index + 1, len(elements)):
        if (
            elements[label_index].tag == ElementAttrib.LABEL
            and elements[index].element.attrib[ElementAttrib.ID]
            in elements[label_index].attrib[ElementAttrib.LABEL_OWNER]
            and elements[label_index].attrib[ElementAttrib.ID]
            in elements[index].element.attrib[ElementAttrib.LABEL]
            and ElementAttrib.CHANNEL in elements[index].element.attrib.keys()
        ):
            elements[label_index].element.attrib[
                "Text"
            ] = f"[string]{elements[index].element.attrib[ElementAttrib.CHANNEL].split('/')[-1]}"
            break

    return elements


def _find_alignments(updated_elements: List[AvailableElement]) -> Tuple[float, float]:
    def extract_top_value(element: AvailableElement):
        try:
            return float(element.element.attrib[ElementAttrib.TOP].split("]")[-1])
        except (AttributeError, ValueError, KeyError):
            return -1.0

    elements = updated_elements[1:]
    lowest_element = max(elements, key=extract_top_value, default=None)

    if not lowest_element:
        return 50.0, 50.0

    top_start_value = (
        float(lowest_element.attrib[ElementAttrib.TOP].split("]")[-1])
        + (
            float(lowest_element.attrib[ElementAttrib.HEIGHT].split("]")[-1])
            if ElementAttrib.HEIGHT in lowest_element.attrib
            else float(lowest_element.attrib[ElementAttrib.MIN_HEIGHT].split("]")[-1])
        )
        + MeasUIElementPosition.TOP_ALIGNMENT_INCREMENTAL_VALUE
    )

    left_start_value = float(lowest_element.attrib[ElementAttrib.LEFT].split("]")[-1])
    return top_start_value, left_start_value


def _create_elements(
    client_id: str,
    top_alignment: float,
    left_alignment: float,
    unmatched_inputs: List[Union[V1ConfigParam, V2ConfigParam]],
    unmatched_outputs: List[Union[V1Output, V2Output]],
) -> str:
    inputs, top_alignment = create_input_elements_from_client(
        inputs=unmatched_inputs,
        client_id=client_id,
        input_top_alignment=top_alignment,
        input_left_alignment=left_alignment,
    )
    outputs = create_output_elements_from_client(
        outputs=unmatched_outputs,
        client_id=client_id,
        output_top_alignment=top_alignment,
        output_left_alignment=left_alignment,
    )
    ui_elements = _add_namespace(inputs + outputs)

    return ui_elements


def _add_namespace(ui_elements: str) -> str:
    ui_elements = re.sub(r"<ChannelPinSelector", "<ns1:ChannelPinSelector", ui_elements)
    ui_elements = re.sub(r"<ChannelArrayViewer", "<ns2:ChannelArrayViewer", ui_elements)
    ui_elements = re.sub(r"</ChannelArrayViewer", "</ns2:ChannelArrayViewer", ui_elements)
    ui_elements = re.sub(r"<Channel(?!PinSelector|ArrayViewer)", "<ns2:Channel", ui_elements)
    ui_elements = re.sub(r"<p", "<ns2:p", ui_elements)
    ui_elements = re.sub(r"</p", "</ns2:p", ui_elements)
    ui_elements = re.sub(r"<Label", "<ns3:Label", ui_elements)
    return ui_elements
