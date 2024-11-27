"""Implementation of read and write measurement plug-in UI file for update command."""

import os
import urllib.parse
import xml.etree.ElementTree as ETree # nosec: B405
from logging import getLogger
from pathlib import Path
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

from ni_measurement_plugin_ui_creator.constants import (
    LOGGER,
    ElementAttrib,
    MeasUIFile,
    UpdateUI,
)
from ni_measurement_plugin_ui_creator.models import AvailableElement
from ni_measurement_plugin_ui_creator.utils.client import get_measurement_service_stub
from ni_measurement_plugin_ui_creator.utils.exceptions import (
    InvalidCliInputError,
    InvalidMeasUIError,
)

INVALID_MEASUI_CHOICE = "Invalid .measui file selected."
SELECT_MEASUI_FILE = "Select a measurement plug-in UI file index ({start}-{end}) to update: "


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
        return None

    metadata = measurement_service_stub.GetMetadata(v2_measurement_service_pb2.GetMetadataRequest())
    return metadata


def get_measui_selection(total_uis: int) -> int:
    """Get measurment plug-in UI selection.

    Args:
        total_uis (int): Total UIs available for the measurement plug-in.

    Raises:
        InvalidCliInputError: If the entered number is invalid.

    Returns:
        int: Selected measurement plug-in UI index.
    """
    logger = getLogger(LOGGER)
    try:
        user_input = int(
            input(
                SELECT_MEASUI_FILE.format(
                    start=1,
                    end=total_uis,
                )
            )
        )
        logger.info("")
        if user_input not in list(range(1, total_uis + 1)):
            raise InvalidCliInputError(INVALID_MEASUI_CHOICE)

        return user_input

    except ValueError:
        raise InvalidCliInputError(INVALID_MEASUI_CHOICE)


def get_measui_files(metadata: Union[V1MetaData, V2MetaData]) -> List[str]:
    """Get measurement plug-in UI files.

    1. Get measurement plug-in UI file paths from metadata.
    2. Filter file paths which has `.measui` as extension.

    Args:
        metadata (Union[V1MetaData, V2MetaData]): Metadata of measurement plug-in.

    Returns:
        List[str]: Measurement plug-in UI file paths.
    """
    file_uris = metadata.user_interface_details
    return [
        uri_to_path(uri.file_url)
        for uri in file_uris
        if uri_to_path(uri.file_url).lower().endswith(MeasUIFile.MEASUREMENT_UI_FILE_EXTENSION)
    ]


def uri_to_path(uri: str) -> str:
    """Convert the URI to path.

    Args:
        uri (str): Input URI.

    Returns:
        str: Path from the URI.
    """
    return urllib.parse.unquote(urllib.parse.urlparse(uri).path)


def validate_measui(root: ETree.ElementTree) -> None:
    """Validate measurement plug-in UI file.

    1. Check for Screen tag to be present.
    2. Check for ScreenSurface to be present.

    Args:
        root (ETree.ElementTree): Element tree of measurement plug-in UI file.

    Raises:
        InvalidMeasUIError: If measurement plug-in UI file is invalid.
    """
    screen = root.findall(UpdateUI.SCREEN_TAG, UpdateUI.NAMESPACES)
    screen_surface = root.findall(UpdateUI.SCREEN_SURFACE_TAG, UpdateUI.NAMESPACES)

    if not screen or not screen_surface:
        raise InvalidMeasUIError


def get_available_elements(measui_tree: ETree.ElementTree) -> List[AvailableElement]:
    """Get available elements from the measurement plug-in UI.

    Args:
        measui_tree (ETree.ElementTree): Measurement plug-in UI file tree.

    Returns:
        List[AvailableElement]: Info of already available elements.
    """
    screen_surface = find_screen_surface(measui_tree)
    avlble_elements = parse_measui_elements(screen_surface)
    return avlble_elements


def find_screen_surface(measui_tree: ETree.ElementTree) -> ETree.Element:
    """Find screen surface tag.

    1. In measurement plug-in UI, controls and indicators will be within screen surface tag.
    2. Get root element and find screen surface tag.

    Args:
        measui_tree (ETree.ElementTree): Measurement plug-in UI file tree.

    Returns:
        ETree.Element: Screen surface element.
    """
    root = measui_tree.getroot()
    screen_surface = root.findall(UpdateUI.SCREEN_SURFACE_TAG, UpdateUI.NAMESPACES)
    return screen_surface[0]


def parse_measui_elements(screen_surface: ETree.Element) -> List[AvailableElement]:
    """Parse the `measui` elements.

    Args:
        screen_surface (ETree.Element): Elements of measurement plug-in UI.

    Returns:
        List[AvailableElement]: Parsed elements.
    """
    avlble_elements = []

    for element in screen_surface.iter():
        tag = element.tag.split("}")[-1]

        if tag in UpdateUI.UNSUPPORTED_ELEMENTS and ElementAttrib.CHANNEL in element.attrib.keys():
            bind: bool = True
            name: Optional[str] = element.attrib[ElementAttrib.CHANNEL].split("/")[-1]
            output: Optional[bool]

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

        elif tag == UpdateUI.ARRAY_ELEMENT:
            output_info = get_output_info_of_array_element(element)

            if output_info:
                output, is_str_array = output_info[0], output_info[1]

            bind, name = get_bind_info(element)

            avlble_elements.append(
                AvailableElement(
                    tag=tag,
                    output=output,
                    bind=bind,
                    name=name,
                    is_str_array=is_str_array,
                    attrib=element.attrib,
                    element=element,
                )
            )

        elif tag == UpdateUI.PIN_ELEMENT:
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

        elif element.tag not in UpdateUI.RING_AND_DEFAULT_ELEMENT:
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


def get_output_info_of_array_element(element: ETree.Element) -> Optional[Tuple[bool, bool]]:
    """Get output info of an array element.

    1. Check if the array element is control or indicator.
    2. Check type of array element i.e., String array or numeric array.

    Args:
        element (ETree.Element): Element available already created.

    Returns:
        Optional[Tuple[bool, bool]]: True if the element is an output, False if not and \
        True if the element is string array, False if it is a numeric array.
    """
    for array_element in element.iter():
        tag = array_element.tag.split("}")[-1]

        if tag == UpdateUI.STRING_ARRAY:
            return get_output_info_for_read_only_based(array_element), True

        if tag == UpdateUI.NUMERIC_ARRAY:
            return get_output_info_for_read_only_based(array_element), False

    return None


def get_output_info(element: ETree.Element) -> Optional[bool]:
    """Get output info.

    Check if the element is control or indicator.

    Args:
        element (ETree.Element): Element available already.

    Returns:
        Optional[bool]: True if the element is an output.
    """
    tag = element.tag.split("}")[-1]

    if tag in UpdateUI.ONLY_INDICATORS:
        return True

    if tag in UpdateUI.READ_ONLY_BASED:
        return get_output_info_for_read_only_based(element)

    if tag in UpdateUI.INTERACTION_MODE_BASED:
        return get_output_info_for_interaction_mode_based(element)

    return None


def get_output_info_for_read_only_based(element: ETree.Element) -> bool:
    """Get output information for read only elements.

    Args:
        element (ETree.Element): Output element.

    Returns:
        bool: True if the element is read only.
    """
    if (
        ElementAttrib.IS_READ_ONLY in element.attrib.keys()
        and element.attrib[ElementAttrib.IS_READ_ONLY] == "[bool]True"
    ):
        return True

    return False


def get_output_info_for_interaction_mode_based(element: ETree.Element) -> bool:
    """Return if the element is interaction mode based.

    Args:
        element (ETree.Element): Output element.

    Returns:
        bool: True if the element is interaction mode based.
    """
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
        element (ETree.Element): Measurement plug-in UI element.

    Returns:
        Tuple[bool, Optional[str]]: Bind and name of the element being bound. None if not bound.
    """
    bind = False
    name = None

    if ElementAttrib.CHANNEL in element.attrib.keys():
        bind = True
        name = element.attrib[ElementAttrib.CHANNEL].split("/")[-1]

    return bind, name


def write_updated_measui(filepath: Path, updated_ui: List[AvailableElement]) -> None:
    """Write updated measurement plug-in UI elements.

    1. Find the Screen tag.
    2. Replace the screen surface tag with updated counterpart.

    Args:
        filepath (Path): Filepath of the updated measurement plug-in UI.
        updated_ui (List[AvailableElement]): Updated UI elements.
    """
    tree = ETree.parse(filepath)  # nosec: B314
    root = tree.getroot()

    screen = root.find(UpdateUI.SCREEN_TAG, UpdateUI.NAMESPACES)

    if screen:
        screen_surface = screen.find(UpdateUI.SCREEN_SURFACE_TAG, UpdateUI.NAMESPACES)
        if screen_surface:
            screen.remove(screen_surface)

        screen.append(updated_ui[0].element)
        tree.write(filepath, encoding=MeasUIFile.ENCODING, xml_declaration=True)


def insert_created_elements(filepath: Path, elements_str: str) -> None:
    """Insert created elements.

    Args:
        filepath (Path): Measurement plug-in UI file path.
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
