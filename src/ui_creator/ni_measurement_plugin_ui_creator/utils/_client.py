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

from ._exceptions import InvalidCliInputError

NO_MEASUREMENTS_RUNNING = "No measurement services are running."
AVAILABLE_MEASUREMENTS = "Available/Registered measurements:"
SELECT_MEASUREMENT = (
    "Select a measurement service index ({start}-{end}) to update/generate measui file: "
)
INVALID_MEASUREMENT_CHOICE = "Invalid measurement plug-in selected."
MEASUREMENT_SERVICE_INTERFACE_V1 = "ni.measurementlink.measurement.v1.MeasurementService"
MEASUREMENT_SERVICE_INTERFACE_V2 = "ni.measurementlink.measurement.v2.MeasurementService"


def get_active_measurement_services(discovery_client: DiscoveryClient) -> List[ServiceInfo]:
    """Get available measurement services.

    Args:
        discovery_client (DiscoveryClient): Client for accessing NI Discovery service.

    Returns:
        Optional[List[ServiceLocation]]: Sequence of active measurement services.
    """
    v1_measurement_services = discovery_client.enumerate_services(MEASUREMENT_SERVICE_INTERFACE_V1)
    v2_measurement_services = discovery_client.enumerate_services(MEASUREMENT_SERVICE_INTERFACE_V2)

    available_services = list(v1_measurement_services) + list(v2_measurement_services)
    return available_services


def get_insecure_grpc_channel_for(
    discovery_client: DiscoveryClient,
    service_class: str,
) -> Optional[Tuple[Channel, str]]:
    """Get insecure GRPC channel.

    Args:
        discovery_client (DiscoveryClient): Client for accessing NI Discovery service.
        service_class (str): Measurement Service Class name.

    Returns:
        Tuple[Channel, str]: Channel to server and measurement service interface name.
    """
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

    if resolved_service and measurement_service_interface:
        return (
            grpc.insecure_channel(resolved_service.insecure_address),
            measurement_service_interface,
        )
    return None


def get_measurement_selection(total_measurements: int) -> int:
    """Prompt user to select a measurement.

    Args:
        total_measurements (int): Total measurements count.

    Returns:
        int: Selected measurement.
    """
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
        raise InvalidCliInputError(INVALID_MEASUREMENT_CHOICE)


def get_measurement_service_class(
    measurement_services: Sequence[ServiceInfo],
    measurement_name: str,
) -> Optional[str]:
    """Get measurement service class information.

    Args:
        measurement_services Sequence[ServiceLocation]]: List of measurement services.
        measurement_name (str): Measurement name.

    Returns:
        Optional[str]: Measurement service class information or None.
    """
    for service in measurement_services:
        if service.display_name == measurement_name:
            return service.service_class
    return None


def get_measurement_service_stub(
    discovery_client: DiscoveryClient,
) -> Union[V1MeasurementServiceStub, V2MeasurementServiceStub, None]:
    """Get measurement services.

    Args:
        discovery_client (DiscoveryClient): Client for accessing NI Discovery service.

    Returns:
        Union[V1MeasurementServiceStub, V2MeasurementServiceStub, None]: Measurement services or \
            None in case of no active measurement services.
    """
    logger = getLogger(LOGGER)
    available_services = get_active_measurement_services(discovery_client)

    if not available_services:
        logger.warning(NO_MEASUREMENTS_RUNNING)
        return None

    measurements = list(set([services.display_name for services in available_services]))

    logger.info("")
    logger.info(AVAILABLE_MEASUREMENTS)
    for serial_num, services in enumerate(measurements):
        logger.info(f"{serial_num + 1}. {services}")

    logger.info("")
    selected_measurement = get_measurement_selection(total_measurements=len(measurements))

    measurement_service_class = get_measurement_service_class(
        available_services,
        measurements[selected_measurement - 1],
    )
    channel, measurement_service_interface = get_insecure_grpc_channel_for(
        discovery_client,
        measurement_service_class,
    )

    if measurement_service_interface == MEASUREMENT_SERVICE_INTERFACE_V2:
        return V2MeasurementServiceStub(channel)

    return V1MeasurementServiceStub(channel)
