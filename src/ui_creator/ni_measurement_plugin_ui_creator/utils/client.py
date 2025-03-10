"""Measurement Plug-In Client."""

from logging import getLogger
from typing import List, Optional, Sequence, Tuple, Union

import grpc
from grpc import Channel
from grpc._channel import _InactiveRpcError
from ni_measurement_plugin_sdk_service._internal.stubs.ni.measurementlink.measurement.v1.measurement_service_pb2_grpc import (
    MeasurementServiceStub as V1MeasurementServiceStub,
)
from ni_measurement_plugin_sdk_service._internal.stubs.ni.measurementlink.measurement.v2.measurement_service_pb2_grpc import (
    MeasurementServiceStub as V2MeasurementServiceStub,
)
from ni_measurement_plugin_sdk_service.discovery import DiscoveryClient
from ni_measurement_plugin_sdk_service.measurement.info import ServiceInfo

from ni_measurement_plugin_ui_creator.constants import LOGGER
from ni_measurement_plugin_ui_creator.utils.exceptions import InvalidCliInputError

AVAILABLE_MEASUREMENTS = "Registered measurements:"
INACTIVE_MEASUREMENNT = "Selected measurement service is not running."
INVALID_MEASUREMENT_CHOICE = "Invalid measurement plug-in selected."
MEASUREMENT_SERVICE_INTERFACE_V1 = "ni.measurementlink.measurement.v1.MeasurementService"
MEASUREMENT_SERVICE_INTERFACE_V2 = "ni.measurementlink.measurement.v2.MeasurementService"
NO_MEASUREMENTS_RUNNING = "No measurement services are running."
SELECT_MEASUREMENT = (
    "Select a measurement service index ({start}-{end}) to create/update measui file: "
)


def get_measurement_service_stub_and_class(
    discovery_client: DiscoveryClient,
) -> Optional[Tuple[Union[V1MeasurementServiceStub, V2MeasurementServiceStub], str]]:
    """Get measurement service stub and measurement service class.

    Args:
        discovery_client: Client for accessing NI Discovery service.

    Returns:
        if available measurement service stub and service class. None in case of
        no active measurement services.
    """
    logger = getLogger(LOGGER)
    available_services = _get_active_measurement_services(discovery_client)

    if not available_services:
        logger.warning(NO_MEASUREMENTS_RUNNING)
        return None

    measurements = list(set([services.display_name for services in available_services]))

    logger.info("")
    logger.info(AVAILABLE_MEASUREMENTS)
    for serial_num, services in enumerate(measurements):
        logger.info(f"{serial_num + 1}. {services}")

    logger.info("")
    selected_measurement = _get_measurement_selection(total_measurements=len(measurements))

    measurement_service_class = _get_measurement_service_class(
        available_services,
        measurements[selected_measurement - 1],
    )
    if not measurement_service_class:
        return None

    channel_and_interface = _get_channel_and_interface(
        discovery_client,
        measurement_service_class,
    )

    if not channel_and_interface:
        return None

    channel, measurement_service_interface = channel_and_interface[0], channel_and_interface[1]

    if measurement_service_interface == MEASUREMENT_SERVICE_INTERFACE_V2:
        return V2MeasurementServiceStub(channel), measurement_service_class

    return V1MeasurementServiceStub(channel), measurement_service_class


def _get_active_measurement_services(discovery_client: DiscoveryClient) -> List[ServiceInfo]:
    v1_measurement_services = discovery_client.enumerate_services(MEASUREMENT_SERVICE_INTERFACE_V1)
    v2_measurement_services = discovery_client.enumerate_services(MEASUREMENT_SERVICE_INTERFACE_V2)

    available_services = list(v1_measurement_services) + list(v2_measurement_services)
    return available_services


def _get_measurement_selection(total_measurements: int) -> int:
    logger = getLogger(LOGGER)
    try:
        user_input = int(
            input(
                SELECT_MEASUREMENT.format(
                    start=1,
                    end=total_measurements,
                )
            )
        )

        logger.info("")

        if user_input not in list(range(1, total_measurements + 1)):
            raise InvalidCliInputError(INVALID_MEASUREMENT_CHOICE)

        return user_input

    except ValueError:
        logger.info("")
        raise InvalidCliInputError(INVALID_MEASUREMENT_CHOICE)


def _get_measurement_service_class(
    measurement_services: Sequence[ServiceInfo],
    measurement_name: str,
) -> Optional[str]:
    for service in measurement_services:
        if service.display_name == measurement_name:
            return service.service_class

    return None


def _get_channel_and_interface(
    discovery_client: DiscoveryClient,
    service_class: str,
) -> Optional[Tuple[Channel, str]]:
    logger = getLogger(LOGGER)
    resolved_service = None
    measurement_service_interface = None

    try:
        resolved_service = discovery_client.resolve_service(
            MEASUREMENT_SERVICE_INTERFACE_V2,
            service_class,
        )
        measurement_service_interface = MEASUREMENT_SERVICE_INTERFACE_V2

    except _InactiveRpcError:
        try:
            resolved_service = discovery_client.resolve_service(
                MEASUREMENT_SERVICE_INTERFACE_V1,
                service_class,
            )
            measurement_service_interface = MEASUREMENT_SERVICE_INTERFACE_V1
        except _InactiveRpcError as exp:
            logger.debug(exp)
            logger.info(INACTIVE_MEASUREMENNT)

    if resolved_service and measurement_service_interface:
        return (
            grpc.insecure_channel(resolved_service.insecure_address),
            measurement_service_interface,
        )

    return None
