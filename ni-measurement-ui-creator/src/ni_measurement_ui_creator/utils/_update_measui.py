"""Implementation of update meas UI."""

import os
import shutil
import xml.etree.ElementTree as ETree
from logging import getLogger
from pathlib import Path
from typing import List, Union

from ni_measurement_plugin_sdk_service._internal.stubs.ni.measurementlink.measurement.v1.measurement_service_pb2 import (
    GetMetadataResponse as V1MetaData,
    ConfigurationParameter as V1ConfigParam,
    Output as V1Output,
)
from ni_measurement_plugin_sdk_service._internal.stubs.ni.measurementlink.measurement.v2.measurement_service_pb2 import (
    GetMetadataResponse as V2MetaData,
    ConfigurationParameter as V2ConfigParam,
    Output as V2Output,
)


from ni_measurement_ui_creator.constants import (
    BOOLEAN_ELEMENTS,
    LOGGER,
    NAMESPACES,
    NUMERIC_DATA_TYPE_VALUES,
    NUMERIC_ELEMENTS,
    DataType,
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

    root = tree.getroot()
    screen = root.find(f".//sf:Screen", NAMESPACES)
    client_id = screen.attrib["ClientId"]
    updated_elements = bind_elements(client_id, elements, unbind_inputs, unbind_outputs)

    write_updated_measui(
        os.path.join(
            output_dir,
            str(Path(Path(selected_measui).name).stem) + "_updated.measui",
        ),
        updated_elements,
    )

    # Call bind elements - done.
    # Call update labels - done.
    # Call create elements.
    # Call write_updated_measui.

    return


def bind_elements(
    client_id: str,
    elements: List[AvlbleElement],
    unbind_inputs: List[Union[V1ConfigParam, V2ConfigParam]],
    unbind_outputs: List[Union[V1Output, V2Output]],
) -> List[AvlbleElement]:
    """Bind elements to its possible input/output.

    Args:
        client_id (str):
        elements (List[AvlbleElement]):
        unbind_inputs (List[Union[V1ConfigParam, V2ConfigParam]]):
        unbind_outputs (List[Union[V1Output, V2Output]]):

    Returns:
        List[AvlbleElement]:
    """
    updated_elements = bind_inputs(client_id, elements, unbind_inputs)
    updated_elements = bind_outputs(client_id, updated_elements, unbind_outputs)
    updated_elements = update_label(updated_elements)
    return updated_elements


def bind_inputs(
    client_id: str,
    elements: List[AvlbleElement],
    unbind_inputs: List[Union[V1ConfigParam, V2ConfigParam]],
) -> List[AvlbleElement]:
    """_summary_

    Args:
        client_id (str): _description_
        elements (List[AvlbleElement]): _description_
        unbind_inputs (List[Union[V1ConfigParam, V2ConfigParam]]): _description_

    Returns:
        List[AvlbleElement]: _description_
    """
    for unbind_input in unbind_inputs:
        for element in elements:
            if (
                element.bind is False
                and element.output is False
                and check_feasibility(unbind_input, element)
            ):
                element = add_input_channel(client_id, element, unbind_input)
                break

    return elements


def bind_outputs(
    client_id: str,
    elements: List[AvlbleElement],
    unbind_outputs: List[Union[V1Output, V2Output]],
) -> List[AvlbleElement]:
    """_summary_

    Args:
        client_id (str): _description_
        elements (List[AvlbleElement]): _description_
        unbind_outputs (List[Union[V1Output, V2Output]]): _description_

    Returns:
        List[AvlbleElement]: _description_
    """
    for unbind_output in unbind_outputs:
        for element in elements:
            if (
                element.bind is False
                and element.output is True
                and check_feasibility(unbind_output, element)
            ):
                element = add_output_channel(client_id, element, unbind_output)
                break

    return elements


def check_feasibility(
    unbind_input: Union[V1ConfigParam, V2ConfigParam],
    element: AvlbleElement,
) -> bool:
    """_summary_

    Args:
        unbind_input (Union[V1ConfigParam, V2ConfigParam]): _description_
        element (AvlbleElement): _description_

    Returns:
        bool: _description_
    """
    if (
        unbind_input.type in NUMERIC_DATA_TYPE_VALUES
        and not (hasattr(unbind_input, "repeated") and unbind_input.repeated)
        and element.tag in NUMERIC_ELEMENTS
    ):
        return True

    if (
        unbind_input.type == DataType.Boolean.value
        and not (hasattr(unbind_input, "repeated") and unbind_input.repeated)
        and element.tag in BOOLEAN_ELEMENTS
    ):
        return True

    if (
        unbind_input.type == DataType.String.value
        and not (
            hasattr(unbind_input, "repeated") or unbind_input.repeated or unbind_input.annotations
        )
        and element.tag == "ChannelStringControl"
    ):
        return True

    if (
        unbind_input.type in NUMERIC_DATA_TYPE_VALUES
        and hasattr(unbind_input, "repeated")
        and unbind_input.repeated
        and element.tag == "ChannelArrayViewer"
    ):
        return True

    return False


def add_input_channel(
    client_id: str,
    element: AvlbleElement,
    unbind_input: Union[V1ConfigParam, V2ConfigParam],
) -> AvlbleElement:
    """_summary_

    Args:
        client_id (str): _description_
        element (AvlbleElement): _description_
        unbind_input (Union[V1ConfigParam, V2ConfigParam]): _description_

    Returns:
        AvlbleElement: _description_
    """
    channel = f"[string]{client_id}/Configuration/{unbind_input.name}"
    element.element.attrib["Channel"] = channel
    element.bind = True
    return element


def add_output_channel(
    client_id: str,
    element: AvlbleElement,
    unbind_output: Union[V1Output, V2Output],
) -> AvlbleElement:
    """_summary_

    Args:
        client_id (str): _description_
        element (AvlbleElement): _description_
        unbind_output (Union[V1Output, V2Output]): _description_

    Returns:
        AvlbleElement: _description_
    """
    channel = f"[string]{client_id}/Output/{unbind_output.name}"
    element.element.attrib["Channel"] = channel
    element.bind = True
    return element


def update_label(elements: List[AvlbleElement]) -> List[AvlbleElement]:
    """_summary_

    Args:
        elements (List[AvlbleElement]): _description_

    Returns:
        List[AvlbleElement]: _description_
    """
    for index in range(len(elements)):
        if (
            elements[index].tag == "Label"
            and elements[index - 1].element.attrib["Id"] in elements[index].attrib["LabelOwner"]
            and elements[index].attrib["Id"] in elements[index - 1].element.attrib["Label"]
            and "Channel" in elements[index - 1].element.attrib.keys()
        ):
            elements[index].element.attrib[
                "Text"
            ] = f"[string]{elements[index-1].element.attrib['Channel'].split('/')[-1]}"

    return elements


def write_updated_measui(filepath: str, updated_ui: List[AvlbleElement]) -> None:
    """_summary_

    Args:
        filepath (str): _description_
        updated_ui (List[AvlbleElement]): _description_
    """
    tree = ETree.parse(filepath)
    root = tree.getroot()
    screen = root.find(f".//sf:Screen", NAMESPACES)
    screen_surface = screen.find(f"cf:ScreenSurface", NAMESPACES)

    screen.remove(screen_surface)

    # Apply unique id filtration here to avoid duplicates.

    for element in updated_ui:
        screen.append(element.element)

    tree.write(filepath, encoding="utf-8", xml_declaration=True)
