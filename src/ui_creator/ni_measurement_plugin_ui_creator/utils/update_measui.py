"""Implementation of update meas UI."""

import re
import shutil
import xml.etree.ElementTree as ETree
from logging import getLogger
from pathlib import Path
from typing import List, Tuple, Union

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

AVAILABLE_MEASUI_FILES = "Available Measurement UI Files:"
NO_MEASUI_FILE = (
    "No Measurement UI file available. "
    "Creating a new measui file for the selected measurement..."
)
INVALID_MEASUI_FILE = (
    "Invalid Measurement UI file. Creating a new measui file for the selected measurement..."
)
BINDING_ELEMENTS = "Binding UI controls and indicators..."
INPUTS_BOUND = "Inputs are bound successfully."
OUTPUTS_BOUND = "Outputs are bound successfully."
CREATING_ELEMENTS = "Creating new controls and indicators..."
UPDATED_UI = "Measurement UI updated successfully. Please find at {filepath}"


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
        logger.warning(NO_MEASUI_FILE)
        create_measui(metadata, output_dir)
        return

    logger.info(AVAILABLE_MEASUI_FILES)
    for serial_num, measui_file_path in enumerate(measui_files):
        logger.info(f"{serial_num + 1}. {measui_file_path[1:]}")

    logger.info("")
    selected_measui = measui_files[get_measui_selection(len(measui_files)) - 1][1:]

    try:
        tree = ETree.parse(selected_measui)
        validate_measui(tree)

    except (ETree.ParseError, InvalidMeasUIError, FileNotFoundError, PermissionError):
        logger.warning(INVALID_MEASUI_FILE)
        create_measui(metadata, output_dir)
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
    client_id = screen.attrib[ElementAttrib.CLIENT_ID]

    logger.info(BINDING_ELEMENTS)
    updated_elements = bind_elements(client_id, elements, unbind_inputs, unbind_outputs)

    write_updated_measui(updated_measui_filepath, updated_elements)

    updated_element_names = [element.name for element in updated_elements]
    top_alignment, left_alignment = find_alignments(updated_elements)

    unmatched_inputs = [input for input in inputs if input.name not in updated_element_names]
    unmatched_outputs = [output for output in outputs if output.name not in updated_element_names]

    logger.info(CREATING_ELEMENTS)
    elements_representation = create_elements(
        client_id,
        top_alignment,
        left_alignment,
        unmatched_inputs,
        unmatched_outputs,
    )

    insert_created_elements(updated_measui_filepath, elements_representation)
    logger.info(UPDATED_UI.format(filepath=Path(updated_measui_filepath).resolve()))

    return None


def bind_elements(
    client_id: str,
    elements: List[AvailableElement],
    unbind_inputs: List[Union[V1ConfigParam, V2ConfigParam]],
    unbind_outputs: List[Union[V1Output, V2Output]],
) -> List[AvailableElement]:
    """Bind elements to its possible input/output.

    Args:
        client_id (str): Client ID.
        elements (List[AvailableElement]): Available elements.
        unbind_inputs (List[Union[V1ConfigParam, V2ConfigParam]]): Unbind inputs.
        unbind_outputs (List[Union[V1Output, V2Output]]): Unbind outputs

    Returns:
        List[AvailableElement]: Updated elements.
    """
    updated_elements = bind_inputs(client_id, elements, unbind_inputs)
    updated_elements = bind_outputs(client_id, updated_elements, unbind_outputs)
    return updated_elements


def bind_inputs(
    client_id: str,
    elements: List[AvailableElement],
    unbind_inputs: List[Union[V1ConfigParam, V2ConfigParam]],
) -> List[AvailableElement]:
    """Bind inputs to controls if feasible.

    Args:
        client_id (str): Client ID.
        elements (List[AvailableElement]): List of available elements.
        unbind_inputs (List[Union[V1ConfigParam, V2ConfigParam]]): Unbind inputs.

    Returns:
        List[AvailableElement]: Updated elements that are being bound.
    """
    logger = getLogger(LOGGER)

    for unbind_input in unbind_inputs:
        for index, element in enumerate(elements):
            if (
                element.bind is False
                and element.output is False
                and check_feasibility(unbind_input, element)
            ):
                element = add_channel(client_id, element, unbind_input)
                element.name = unbind_input.name
                element.bind = True
                elements = update_label(index, elements)
                break

    logger.debug(INPUTS_BOUND)
    return elements


def bind_outputs(
    client_id: str,
    elements: List[AvailableElement],
    unbind_outputs: List[Union[V1Output, V2Output]],
) -> List[AvailableElement]:
    """Bind outputs to indicators if feasible.

    Args:
        client_id (str): Client ID.
        elements (List[AvailableElement]): List of available elements.
        unbind_outputs (List[Union[V1Output, V2Output]]): Unbind outputs.

    Returns:
        List[AvailableElement]: Updated elements that are being bound.
    """
    logger = getLogger(LOGGER)
    for unbind_output in unbind_outputs:
        for index, element in enumerate(elements):
            if (
                element.bind is False
                and element.output is True
                and check_feasibility(unbind_output, element)
            ):
                element = add_channel(client_id, element, unbind_output)
                element.name = unbind_output.name
                element.bind = True
                elements = update_label(index, elements)
                break

    logger.debug(OUTPUTS_BOUND)
    return elements


def check_feasibility(
    unbind_param: Union[V1ConfigParam, V2ConfigParam, V1Output, V2Output],
    element: AvailableElement,
) -> bool:
    """Check if unbind input/output can be bound to the element.

    Args:
        unbind_param (Union[V1ConfigParam, V2ConfigParam]): Unbind input/output.
        element (AvailableElement): Unbind element.

    Returns:
        bool: True if unbind input/output is possible to bound to the element.
    """
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
        and element.tag == UpdateUI.ARRAY_ELEMENT
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
        and element.tag == UpdateUI.ARRAY_ELEMENT
        and element.is_str_array
    ):
        return True

    return False


def add_channel(
    client_id: str,
    element: AvailableElement,
    unbind_param: Union[V1ConfigParam, V2ConfigParam, V1Output, V2Output],
) -> AvailableElement:
    """Add channel attribute to bind the lement.

    Args:
        client_id (str): Client ID.
        element (AvailableElement): Unbind element.
        unbind_input (Union[V1ConfigParam, V2ConfigParam, V1Output, V2Output]): Unbind input/output.

    Returns:
        AvailableElement: Bound element.
    """
    if isinstance(unbind_param, V1ConfigParam) or isinstance(unbind_param, V2ConfigParam):
        channel = f"[string]{client_id}/Configuration/{unbind_param.name}"
    else:
        channel = f"[string]{client_id}/Output/{unbind_param.name}"

    element.element.attrib[ElementAttrib.CHANNEL] = channel
    return element


def update_label(index: int, elements: List[AvailableElement]) -> List[AvailableElement]:
    """Update label element.

    1. Find the bound label element of the element.
    2. Update the label element with the name.

    Args:
        index (int): Index of bound element.
        elements (List[AvailableElement]): Available elements.

    Returns:
        List[AvailableElement]: Elements with updated label.
    """
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


def find_alignments(updated_elements: List[AvailableElement]) -> Tuple[float, float]:
    """Find bottom most element to get the top and left values.

    Args:
        updated_elements (List[AvailableElement]): Updated UI elements.

    Returns:
        Tuple[float, float]: Top and left values.
    """

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


def create_elements(
    client_id: str,
    top_alignment: float,
    left_alignment: float,
    unmatched_inputs: List[Union[V1ConfigParam, V2ConfigParam]],
    unmatched_outputs: List[Union[V1Output, V2Output]],
) -> str:
    """Create controls and indicators for the unmatched inputs and outputs.

    Args:
        client_id (str): Client ID of the file.
        top_alignment (float): Top alignment value.
        left_alignment (float): Left alignment value.
        unmatched_inputs (List[Union[V1ConfigParam, V2ConfigParam]]): Inputs that \
        doesn't have a corresponding element.
        unmatched_outputs (List[Union[V1Output, V2Output]]): Outputs that \
        doesn't have a corresponding element.

    Returns:
        str: UI elements for supported unmatched inputs and unmatched outputs.
    """
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
    ui_elements = add_namespace(inputs + outputs)

    return ui_elements


def add_namespace(ui_elements: str) -> str:
    """Add namespace to UI elements created.

    Args:
        ui_elements (str): UI elements.

    Returns:
        str: Namespaces added UI elements.
    """
    ui_elements = re.sub(r"<ChannelPinSelector", "<ns1:ChannelPinSelector", ui_elements)
    ui_elements = re.sub(r"<ChannelArrayViewer", "<ns2:ChannelArrayViewer", ui_elements)
    ui_elements = re.sub(r"</ChannelArrayViewer", "</ns2:ChannelArrayViewer", ui_elements)
    ui_elements = re.sub(r"<Channel(?!PinSelector|ArrayViewer)", "<ns2:Channel", ui_elements)
    ui_elements = re.sub(r"<p", "<ns2:p", ui_elements)
    ui_elements = re.sub(r"</p", "</ns2:p", ui_elements)
    ui_elements = re.sub(r"<Label", "<ns3:Label", ui_elements)
    return ui_elements
