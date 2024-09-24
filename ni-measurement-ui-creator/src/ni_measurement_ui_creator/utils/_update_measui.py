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
from ni_measurement_ui_creator.utils._ui_elements import (
    create_input_elements_from_client,
    create_output_elements_from_client,
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

    updated_element_names = [element.name for element in updated_elements]
    unbind_inputs = [input for input in inputs if input.name not in updated_element_names]
    unbind_outputs = [output for output in outputs if output.name not in updated_element_names]

    elements = create_elements(client_id, unbind_inputs, unbind_outputs)
    # Call bind elements - done.
    # Call update labels - done.
    # Call create elements - done.
    # Call write_updated_measui - done.
    # Handle graph.
    # Update labels of array elements.
    # Find max top, left values for element creation.
    insert_multiple_elements_directly(
        os.path.join(
            output_dir,
            str(Path(Path(selected_measui).name).stem) + "_updated.measui",
        ),
        "ScreenSurface",
        elements,
    )

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
                element.name = unbind_input.name
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
                element.name = unbind_output.name
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


def create_elements(client_id, unbind_inputs, unbind_outputs):
    """_summary_

    Args:
        client_id (_type_): _description_
        unbind_inputs (_type_): _description_
        unbind_outputs (_type_): _description_

    Returns:
        _type_: _description_
    """
    inputs = create_input_elements_from_client(
        inputs=unbind_inputs,
        input_top_alignment=350,
        client_id=client_id,
    )
    outputs = create_output_elements_from_client(
        outputs=unbind_outputs,
        output_left_alignment=300,
        client_id=client_id,
    )
    ui_elements = add_namespace(inputs + outputs)

    return ui_elements


def add_namespace(ui_elements: str):
    """_summary_

    Args:
        ui_elements (str): _description_

    Returns:
        _type_: _description_
    """
    ui_elements = ui_elements.replace("<Channel", "<ns2:Channel")
    ui_elements = ui_elements.replace("<p", "<ns2:p")
    ui_elements = ui_elements.replace("<Label", "<ns3:Label")
    return ui_elements


def write_updated_measui(filepath: str, updated_ui: List[AvlbleElement]) -> None:
    """_summary_

    Args:
        filepath (str): _description_
        updated_ui (List[AvlbleElement]): _description_
    """
    tree = ETree.parse(filepath)
    root = tree.getroot()
    screen = root.find("{http://www.ni.com/InstrumentFramework/ScreenDocument}Screen")
    screen_surface = screen.find("{http://www.ni.com/ConfigurationBasedSoftware.Core}ScreenSurface")

    screen.remove(screen_surface)
    screen.append(updated_ui[0].element)

    tree.write(filepath, encoding="utf-8", xml_declaration=True)


def insert_multiple_elements_directly(xml_file, parent_tag, elements_str):
    """_summary_

    Args:
        xml_file (_type_): _description_
        parent_tag (_type_): _description_
        elements_str (_type_): _description_
    """
    # Read the existing XML content
    with open(xml_file, "r", encoding="utf-8") as file:
        xml_content = file.read()

    # Find the position of the closing tag of the parent element
    closing_tag = f"</ns2:{parent_tag}>"
    insert_position = xml_content.find(closing_tag)

    if insert_position == -1:
        print(f"Tag '{parent_tag}' not found.")
        return

    # Insert the new elements before the closing tag
    new_content = (
        xml_content[:insert_position] + elements_str + "\n" + xml_content[insert_position:]
    )

    # Write the modified content back to the XML file
    with open(xml_file, "w", encoding="utf-8") as file:
        file.write(new_content)
