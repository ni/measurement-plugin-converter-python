"""Implementation of read and write meas UI file for update command."""

import os
import urllib.parse
import xml.etree.ElementTree as ETree
from typing import List, Optional, Tuple, Union

from ni_measurement_plugin_sdk_service._internal.stubs.ni.measurementlink.measurement.v1.measurement_service_pb2 import (
    GetMetadataResponse as V1MetaData,
)
from ni_measurement_plugin_sdk_service._internal.stubs.ni.measurementlink.measurement.v2 import (
    measurement_service_pb2 as v2_measurement_service_pb2,
)
from ni_measurement_plugin_sdk_service._internal.stubs.ni.measurementlink.measurement.v2.measurement_service_pb2 import (
    GetMetadataResponse as V2MetaData,
)
from ni_measurement_plugin_sdk_service.discovery import DiscoveryClient

from ni_measurement_ui_creator.constants import ElementAttrib, MeasUIFile, UpdateUI, UserMessage
from ni_measurement_ui_creator.models import AvailableElement
from ni_measurement_ui_creator.utils._client import get_measurement_service_stub
from ni_measurement_ui_creator.utils._exceptions import InvalidCliInputError, InvalidMeasUIError


def get_metadata() -> Union[V1MetaData, V2MetaData, None]:
    """Get metadata of the measurement plug-in.

    1. Get measurement service.
    2. Get metadata of measurement plug-in.

    Returns:
        Union[V1MetaData, V2MetaData, None]: Metadata if selected measurement plug-in is valid.
    """
    os.environ["GRPC_VERBOSITY"] = "NONE"
    discovery_client = DiscoveryClient()
    measurement_service_stub = get_measurement_service_stub(discovery_client)

    if not measurement_service_stub:
        return

    metadata = measurement_service_stub.GetMetadata(v2_measurement_service_pb2.GetMetadataRequest())
    return metadata


def get_measui_selection(total_uis: int) -> int:
    """Get measurment UI selection.

    Args:
        total_uis (int): Total UIs available for the measurement plug-in.

    Raises:
        InvalidCliInputError: If the entered number is invalid.

    Returns:
        int: Selected measurement UI index.
    """
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
        raise InvalidCliInputError(UserMessage.INVALID_MEASUI_CHOICE)


def get_measui_files(metadata: Union[V1MetaData, V2MetaData]) -> List[str]:
    """Get measurement UI files.

    1. Get UI file paths from metadata.
    2. Filter file paths which has `.measui` as extension.

    Args:
        metadata (Union[V1MetaData, V2MetaData]): Metadata of measurement plug-in.

    Returns:
        List[str]: Measurement UI file paths.
    """
    file_uris = metadata.user_interface_details
    return [
        __uri_to_path(uri.file_url)
        for uri in file_uris
        if __uri_to_path(uri.file_url).lower().endswith(MeasUIFile.MEASUREMENT_UI_FILE_EXTENSION)
    ]


def __uri_to_path(uri: str):
    return urllib.parse.unquote(urllib.parse.urlparse(uri).path)


def validate_measui(root: ETree.ElementTree) -> None:
    """Validate measurement UI file.

    1. Check for Screen tag to be present.
    2. Check for ScreenSurface to be present.

    Args:
        root (ETree.ElementTree): Element tree of measurement UI file.

    Raises:
        InvalidMeasUIError: If measurement UI file is invalid.
    """
    screen = root.findall(UpdateUI.SCREEN_TAG, UpdateUI.NAMESPACES)
    screen_surface = root.findall(UpdateUI.SCREEN_SURFACE_TAG, UpdateUI.NAMESPACES)

    if not screen or not screen_surface:
        raise InvalidMeasUIError


def get_avlble_elements(measui_tree: ETree.ElementTree) -> List[AvailableElement]:
    """Get available elements from the measurement UI.

    Args:
        measui_tree (ETree.ElementTree): Measurement UI file tree.

    Returns:
        List[AvailableElement]: Info of already available elements.
    """
    screen_surface = find_screen_surface(measui_tree)
    avlble_elements = __get_avlble_elements(screen_surface)
    return avlble_elements


def find_screen_surface(measui_tree: ETree.ElementTree) -> ETree.Element:
    """Find screen surface tag.

    1. In measurement UI, controls and indicators will be within screen surface tag.
    2. Get root element and find screen surface tag.

    Args:
        measui_tree (ETree.ElementTree): Measurement UI file tree.

    Returns:
        ETree.Element: Screen surface element.
    """
    root = measui_tree.getroot()
    screen_surface = root.findall(UpdateUI.SCREEN_SURFACE_TAG, UpdateUI.NAMESPACES)
    return screen_surface[0]


def __get_avlble_elements(screen_surface: ETree.Element) -> List[AvailableElement]:
    avlble_elements = []

    for element in screen_surface.iter():
        tag = element.tag.split("}")[-1]

        if tag in UpdateUI.UNSUPPORTED_ELEMENTS and ElementAttrib.CHANNEL in element.attrib.keys():
            bind = True
            name = element.attrib[ElementAttrib.CHANNEL].split("/")[-1]

            if element.attrib[ElementAttrib.CHANNEL].split("/")[-2] == "output":
                output = True
            elif element.attrib[ElementAttrib.CHANNEL].split("/")[-2] == "configuration":
                output = False

            avlble_elements.append(
                AvailableElement(
                    tag=tag,
                    output=output,
                    bind=bind,
                    name=name,
                    attrib=element.attrib,
                    element=element,
                )
            )

        elif tag == "ChannelArrayViewer":
            output = get_output_info_of_array_element(element)
            bind, name = get_bind_info(element)

            avlble_elements.append(
                AvailableElement(
                    tag=tag,
                    output=output,
                    bind=bind,
                    name=name,
                    attrib=element.attrib,
                    element=element,
                )
            )

        elif tag == "ChannelPinSelector":
            output = False
            bind, name = get_bind_info(element)

            avlble_elements.append(
                AvailableElement(
                    tag=tag,
                    output=output,
                    bind=bind,
                    name=name,
                    attrib=element.attrib,
                    element=element,
                )
            )

        elif tag in UpdateUI.SUPPORTED_CONTROLS_AND_INDICATORS:
            output = get_output_info(element)
            bind, name = get_bind_info(element)

            avlble_elements.append(
                AvailableElement(
                    tag=tag,
                    output=output,
                    bind=bind,
                    name=name,
                    attrib=element.attrib,
                    element=element,
                )
            )

        elif element.tag not in ["p.DefaultElementValue", "RingSelectorInfo"]:
            avlble_elements.append(
                AvailableElement(
                    tag=tag,
                    output=None,
                    bind=None,
                    name=None,
                    attrib=element.attrib,
                    element=element,
                )
            )

    return avlble_elements


def get_output_info_of_array_element(element: ETree.Element) -> bool:
    """Check whether array element is input or output.

    Args:
        element (ETree.Element): Element available/already created.

    Returns:
        bool: True if the element is an output.
    """
    for array_ele in element.iter():
        tag = array_ele.tag.split("}")[-1]
        if (
            tag in UpdateUI.NUMERIC_AND_STRING_ARRAY
            and ElementAttrib.IS_READ_ONLY in array_ele.attrib.keys()
            and array_ele.attrib[ElementAttrib.IS_READ_ONLY] == "[bool]True"
        ):
            return True

        elif (
            tag in UpdateUI.NUMERIC_AND_STRING_ARRAY
            and ElementAttrib.IS_READ_ONLY in array_ele.attrib.keys()
            and array_ele.attrib[ElementAttrib.IS_READ_ONLY] == "[bool]False"
        ):
            return False

        elif (
            tag in UpdateUI.NUMERIC_AND_STRING_ARRAY
            and ElementAttrib.IS_READ_ONLY not in array_ele.attrib.keys()
        ):
            return False


def get_output_info(element: ETree.Element) -> bool:
    """Get output info.

    Args:
        element (ETree.Element): Element available/already.

    Returns:
        bool: True if the element is an output.
    """
    tag = element.tag.split("}")[-1]

    if tag in UpdateUI.ONLY_INDICATORS:
        return True

    if tag in UpdateUI.READ_ONLY_BASED:
        return __get_output_info_for_read_only_based(element)

    if tag in UpdateUI.INTERACTION_MODE_BASED:
        return __get_output_info_for_interaction_mode_based(element)


def __get_output_info_for_read_only_based(element: AvailableElement) -> bool:
    if (
        ElementAttrib.IS_READ_ONLY in element.attrib.keys()
        and element.attrib[ElementAttrib.IS_READ_ONLY] == "[bool]True"
    ):
        return True

    return False


def __get_output_info_for_interaction_mode_based(element: AvailableElement) -> bool:
    if (
        ElementAttrib.INTERACTION_MODE in element.attrib.keys()
        and element.attrib[ElementAttrib.INTERACTION_MODE]
        == "[NumericPointerInteractionModes]EditRange"
    ):
        return True

    return False


def get_bind_info(element: ETree.Element) -> Tuple[bool, Optional[str]]:
    """Get bind info of the element. If bound, name is also taken up.

    Args:
        element (ETree.Element): Measurement UI element.

    Returns:
        Tuple[bool, Optional[str]]: Bind and name of the element being bound. None if not bound.
    """
    bind = False
    name = None

    if ElementAttrib.CHANNEL in element.attrib.keys():
        bind = True
        name = element.attrib[ElementAttrib.CHANNEL].split("/")[-1]

    return bind, name


def write_updated_measui(filepath: str, updated_ui: List[AvailableElement]) -> None:
    """Write updated meas UI elements.

    1. Find the Screen tag.
    2. Replace the screen surface tag with updated counterpart.

    Args:
        filepath (str): Filepath of the updated meas UI.
        updated_ui (List[AvailableElement]): Updated UI elements.
    """
    tree = ETree.parse(filepath)
    root = tree.getroot()

    screen = root.find(UpdateUI.SCREEN_TAG, UpdateUI.NAMESPACES)
    screen_surface = screen.find(UpdateUI.SCREEN_SURFACE_TAG, UpdateUI.NAMESPACES)

    screen.remove(screen_surface)
    screen.append(updated_ui[0].element)

    tree.write(filepath, encoding=MeasUIFile.ENCODING, xml_declaration=True)


def insert_created_elements(filepath: str, elements_str: str) -> None:
    """Insert created elements.

    Args:
        filepath (str): Measurement UI file path.
        elements_str (str): Created elements.
    """
    with open(filepath, "r", encoding=MeasUIFile.ENCODING) as file:
        xml_content = file.read()

    closing_tag = "</ns2:ScreenSurface>"
    insert_position = xml_content.find(closing_tag)

    new_content = (
        xml_content[:insert_position] + elements_str + "\n" + xml_content[insert_position:]
    )

    with open(filepath, "w", encoding=MeasUIFile.ENCODING) as file:
        file.write(new_content)
