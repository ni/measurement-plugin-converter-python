"""Implementation of read meas UI file."""

import os
import urllib.parse

from ni_measurement_plugin_sdk_service._internal.stubs.ni.measurementlink.measurement.v2 import (
    measurement_service_pb2 as v2_measurement_service_pb2,
)
from ni_measurement_plugin_sdk_service.discovery import DiscoveryClient

from ni_measurement_ui_creator.constants import NAMESPACES
from ni_measurement_ui_creator.models import UpdateElement
from ni_measurement_ui_creator.utils._client import get_measurement_service_stub
from ni_measurement_ui_creator.utils._exceptions import InvalidMeasUIError


def get_metadata():
    os.environ["GRPC_VERBOSITY"] = "NONE"
    discovery_client = DiscoveryClient()
    measurement_service_stub = get_measurement_service_stub(discovery_client)

    if not measurement_service_stub:
        return

    metadata = measurement_service_stub.GetMetadata(v2_measurement_service_pb2.GetMetadataRequest())
    return metadata


def get_measui_files(metadata):
    file_uris = metadata.user_interface_details
    return [
        uri_to_path(uri.file_url)
        for uri in file_uris
        if uri_to_path(uri.file_url).lower().endswith(".measui")
    ]


def uri_to_path(uri):
    return urllib.parse.unquote(urllib.parse.urlparse(uri).path)


def validate_measui(root):
    screen = root.findall(f".//sf:Screen", NAMESPACES)
    screen_surface = root.findall(f".//cf:ScreenSurface", NAMESPACES)

    if not (
        (screen and screen_surface) or root.tag == "{http://www.ni.com/PlatformFramework}SourceFile"
    ):
        raise InvalidMeasUIError


def get_controls_and_indicators(measui_tree):
    controls_and_indicators = []

    screen_surface = find_screen_surface(measui_tree)

    for element in screen_surface.iter():
        tag = element.tag.split("}")[-1]

        if "Channel" in tag or "Channel" in element.attrib or "HmiGraphPlot" in tag:
            bind = False
            name = None
            output = None
            if "Channel" in element.attrib:
                bind = True
                name = element.attrib["Channel"].split("/", 2)[-1]

                if element.attrib["Channel"].split("/")[-2] == "Configuration":
                    output = False
                else:
                    output = True

            controls_and_indicators.append(
                UpdateElement(
                    tag=tag,
                    output=output,
                    bind=bind,
                    name=name,
                    attrib=element.attrib,
                )
            )

    return controls_and_indicators


def find_screen_surface(measui_tree):
    root = measui_tree.getroot()
    screen_surface = root.findall(f".//cf:ScreenSurface", NAMESPACES)
    return screen_surface[0]
