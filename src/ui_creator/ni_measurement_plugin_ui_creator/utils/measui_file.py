"""Implementation of read and write measurement plug-in UI file for update command."""

import os
import urllib.parse
import xml.etree.ElementTree as ETree  # nosec: B405
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
from ni_measurement_plugin_ui_creator.utils.client import (
    get_measurement_service_stub_and_class,
)
from ni_measurement_plugin_ui_creator.utils.exceptions import (
    InvalidCliInputError,
    InvalidMeasUIError,
)

INVALID_MEASUI_CHOICE = "Invalid .measui file selected."
SELECT_MEASUI_FILE = "Select a measurement plug-in UI file index ({start}-{end}) to update: "


def get_metadata_and_service_class() -> Optional[Tuple[Union[V1MetaData, V2MetaData], str]]:
    """Get metadata and service class of the measurement plug-in.

    Returns:
        Optional[Tuple[Union[V1MetaData, V2MetaData], str]]: Metadata and service class name
        if selected measurement plug-in is valid. Else None.
    """
    os.environ["GRPC_VERBOSITY"] = "NONE"
    discovery_client = DiscoveryClient()
    service_stub_and_class = get_measurement_service_stub_and_class(discovery_client)

    if not service_stub_and_class:
        return None

    measurement_service_stub, measurement_service_class = (
        service_stub_and_class[0],
        service_stub_and_class[1],
    )
    metadata = measurement_service_stub.GetMetadata(v2_measurement_service_pb2.GetMetadataRequest())
    return metadata, measurement_service_class


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
        logger.info("")
        raise InvalidCliInputError(INVALID_MEASUI_CHOICE)


def get_measui_files(metadata: Union[V1MetaData, V2MetaData]) -> List[str]:
    """Get measurement plug-in UI files.

    Args:
        metadata (Union[V1MetaData, V2MetaData]): Metadata of measurement plug-in.

    Returns:
        List[str]: Measurement plug-in UI file paths.
    """
    file_uris = metadata.user_interface_details
    return [
        _uri_to_path(uri.file_url)
        for uri in file_uris
        if _uri_to_path(uri.file_url).lower().endswith(MeasUIFile.MEASUREMENT_UI_FILE_EXTENSION)
    ]


def _uri_to_path(uri: str) -> str:
    """Convert the URI to path.

    Args:
        uri (str): Input URI.

    Returns:
        str: Path from the URI.
    """
    return urllib.parse.unquote(urllib.parse.urlparse(uri).path)


def validate_measui(root: ETree.ElementTree) -> None:
    """Validate measurement plug-in UI file.

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
    screen_surface = _find_screen_surface(measui_tree)
    avlble_elements = _parse_measui_elements(screen_surface)
    return avlble_elements


def _find_screen_surface(measui_tree: ETree.ElementTree) -> ETree.Element:
    """Find screen surface tag.

    Args:
        measui_tree (ETree.ElementTree): Measurement plug-in UI file tree.

    Returns:
        ETree.Element: Screen surface element.
    """
    root = measui_tree.getroot()
    screen_surface = root.findall(UpdateUI.SCREEN_SURFACE_TAG, UpdateUI.NAMESPACES)
    return screen_surface[0]


def _parse_measui_elements(screen_surface: ETree.Element) -> List[AvailableElement]:
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

        elif tag == UpdateUI.ARRAY_CONTAINER_ELEMENT:
            output_info = _get_output_info_of_array_element(element)

            if output_info:
                output, is_str_array = output_info[0], output_info[1]

            bind, name = _get_bind_info(element)

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
            bind, name = _get_bind_info(element)

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
            output = _get_output_info(element)
            bind, name = _get_bind_info(element)

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


def _get_output_info_of_array_element(element: ETree.Element) -> Optional[Tuple[bool, bool]]:
    """Get output info of an array element.

    Args:
        element (ETree.Element): Element available already created.

    Returns:
        Optional[Tuple[bool, bool]]: True if the element is an output, False if not and \
        True if the element is string array, False if it is a numeric array.
    """
    for array_element in element.iter():
        tag = array_element.tag.split("}")[-1]

        if tag == UpdateUI.STRING_ARRAY:
            return _get_output_info_for_read_only_based(array_element), True

        if tag == UpdateUI.NUMERIC_ARRAY:
            return _get_output_info_for_read_only_based(array_element), False

    return None


def _get_output_info(element: ETree.Element) -> Optional[bool]:
    """Get output info. Check if the element is control or indicator or neither.

    Args:
        element (ETree.Element): Element available already.

    Returns:
        Optional[bool]: True if the element is an output. Else False.
    """
    tag = element.tag.split("}")[-1]

    if tag in UpdateUI.ONLY_INDICATORS:
        return True

    if tag in UpdateUI.READ_ONLY_BASED:
        return _get_output_info_for_read_only_based(element)

    if tag in UpdateUI.INTERACTION_MODE_BASED:
        return _get_output_info_for_interaction_mode_based(element)

    return None


def _get_output_info_for_read_only_based(element: ETree.Element) -> bool:
    """Get output information for read only elements.

    Args:
        element (ETree.Element): Output element.

    Returns:
        bool: True if the element is read only. Else False.
    """
    if (
        ElementAttrib.IS_READ_ONLY in element.attrib.keys()
        and element.attrib[ElementAttrib.IS_READ_ONLY] == "[bool]True"
    ):
        return True

    return False


def _get_output_info_for_interaction_mode_based(element: ETree.Element) -> bool:
    """Return if the element is interaction mode based.

    Args:
        element (ETree.Element): Output element.

    Returns:
        bool: True if the element is interaction mode based. Else False.
    """
    if (
        ElementAttrib.INTERACTION_MODE in element.attrib.keys()
        and element.attrib[ElementAttrib.INTERACTION_MODE]
        == "[NumericPointerInteractionModes]EditRange"
    ):
        return True

    return False


def _get_bind_info(element: ETree.Element) -> Tuple[bool, Optional[str]]:
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
