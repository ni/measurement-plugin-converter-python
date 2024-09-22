"""Implementation of read meas UI file."""

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

from ni_measurement_ui_creator.constants import (
    INTERACTION_MODE_BASED,
    NAMESPACES,
    ONLY_INDICATORS,
    READ_ONLY_BASED,
    SUPPORTED_CONTROLS_AND_INDICATORS,
    UserMessage,
)
from ni_measurement_ui_creator.models import AvlbleElement
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
        InvalidCliInputError: If the entered number is not within the length of the available UIs.

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
        raise InvalidCliInputError(UserMessage.ABORTED)


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
        if __uri_to_path(uri.file_url).lower().endswith(".measui")
    ]


def __uri_to_path(uri):
    return urllib.parse.unquote(urllib.parse.urlparse(uri).path)


def validate_measui(root: ETree.ElementTree) -> None:
    """Validate measurement UI file.

    1. Check for SourceFile tag to be present.
    2. Check for Screen tag to be present.
    3. Check for ScreenSurface to be present.

    Args:
        root (ETree.ElementTree): Element tree of measurement UI file.

    Raises:
        InvalidMeasUIError: If measurement UI file is invalid.
    """
    screen = root.findall(f".//sf:Screen", NAMESPACES)
    screen_surface = root.findall(f".//cf:ScreenSurface", NAMESPACES)

    if not (
        (screen and screen_surface) or root.tag == "{http://www.ni.com/PlatformFramework}SourceFile"
    ):
        raise InvalidMeasUIError


def get_avlble_elements(measui_tree: ETree.ElementTree) -> List[AvlbleElement]:
    """Get available elements from the measurement UI.

    Args:
        measui_tree (ETree.ElementTree): Measurement UI file tree.

    Returns:
        List[AvlbleElement]: Info of already available elements.
    """
    screen_surface = find_screen_surface(measui_tree)
    avlble_elements = __get_avlble_elements(screen_surface)
    return avlble_elements


def find_screen_surface(measui_tree: ETree.ElementTree) -> ETree.Element:
    """Find screen surface tag.

    1. In measurement UI, controls and indicators will be within screen surface tag.
    2. So, get root element and find screen surface tag.

    Args:
        measui_tree (ETree.ElementTree): Measurement UI file tree.

    Returns:
        ETree.Element: Screen surface element.
    """
    # Error handling required.
    root = measui_tree.getroot()
    screen_surface = root.findall(f".//cf:ScreenSurface", NAMESPACES)
    return screen_surface[0]


def __get_avlble_elements(screen_surface: ETree.Element) -> List[AvlbleElement]:
    avlble_elements = []

    for element in screen_surface.iter():
        tag = element.tag.split("}")[-1]

        if (
            tag
            in ["ChannelRingSelector", "ChannelEnumSelector", "ChannelPathSelector", "HmiGraphPlot"]
            and "Channel" in element.attrib
        ):
            bind = True
            name = element.attrib["Channel"].split("/")[-1]

            if element.attrib["Channel"].split("/")[-2] == "output":
                output = True
            elif element.attrib["Channel"].split("/")[-2] == "configuration":
                output = False

            avlble_elements.append(
                AvlbleElement(
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
                AvlbleElement(
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
                AvlbleElement(
                    tag=tag,
                    output=output,
                    bind=bind,
                    name=name,
                    attrib=element.attrib,
                    element=element,
                )
            )

        elif tag in SUPPORTED_CONTROLS_AND_INDICATORS:
            output = get_output_info(element)
            bind, name = get_bind_info(element)

            avlble_elements.append(
                AvlbleElement(
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
                AvlbleElement(
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
        if (
            (
                "ChannelArrayNumericText" in array_ele.tag
                or "ChannelArrayStringControl" in array_ele.tag
            )
            and "IsReadOnly" in array_ele.attrib.keys()
            and array_ele.attrib["IsReadOnly"] == "[bool]True"
        ):
            output = True
        elif (
            (
                "ChannelArrayNumericText" in array_ele.tag
                or "ChannelArrayStringControl" in array_ele.tag
            )
            and "IsReadOnly" in array_ele.attrib.keys()
            and array_ele.attrib["IsReadOnly"] == "[bool]False"
        ):
            output = False
        elif (
            "ChannelArrayNumericText" in array_ele.tag
            or "ChannleArrayStringControl" in array_ele.tag
        ) and "IsReadOnly" not in array_ele.attrib.keys():
            output = False

    return output


def get_output_info(element: ETree.Element) -> bool:
    """Get output info.

    Args:
        element (ETree.Element): Element available/already.

    Returns:
        bool: True if the element is an output.
    """
    tag = element.tag.split("}")[-1]

    if tag in ONLY_INDICATORS:
        output = True

    elif (
        tag in READ_ONLY_BASED
        and "IsReadOnly" in element.attrib.keys()
        and element.attrib["IsReadOnly"] == "[bool]True"
    ):
        output = True

    elif (
        tag in READ_ONLY_BASED
        and "IsReadOnly" in element.attrib.keys()
        and element.attrib["IsReadOnly"] == "[bool]False"
    ):
        output = False

    elif tag in READ_ONLY_BASED and "IsReadOnly" not in element.attrib.keys():
        output = False

    elif (
        tag in INTERACTION_MODE_BASED
        and "InteractionMode" in element.attrib.keys()
        and element.attrib["InteractionMode"] == "[NumericPointerInteractionModes]EditRange"
    ):
        output = True

    elif (
        tag in INTERACTION_MODE_BASED
        and "InteractionMode" in element.attrib.keys()
        and element.attrib["InteractionMode"] != "[NumericPointerInteractionModes]EditRange"
    ):
        output = False

    elif tag in INTERACTION_MODE_BASED and "InteractionMode" not in element.attrib.keys():
        output = False

    return output


def get_bind_info(element: ETree.Element) -> Tuple[bool, Optional[str]]:
    """Get bind info of the element. If bound, name is also taken up.

    Args:
        element (ETree.Element): Measurement UI element.

    Returns:
        Tuple[bool, Optional[str]]:
    """
    bind = False
    name = None

    if "Channel" in element.attrib.keys():
        bind = True
        name = element.attrib["Channel"].split("/")[-1]

    return bind, name
