"""Measurement Plug-In Client."""

from logging import Logger
from typing import Optional, Sequence

import grpc
from grpc import Channel
from grpc._channel import _InactiveRpcError
from ni_measurementlink_service._internal.stubs.ni.measurementlink.measurement.v2 import (
    measurement_service_pb2_grpc as v2_measurement_service_pb2_grpc,
)
from ni_measurementlink_service.discovery import DiscoveryClient, ServiceLocation

from ni_measurement_ui_creator.constants import (
    MEASUREMENT_SERVICE_INTERFACE_V1,
    MEASUREMENT_SERVICE_INTERFACE_V2,
    UserMessage,
)
from ._exceptions import InvalidCliInputError


def get_active_measurement_services(
    discovery_client: DiscoveryClient,
) -> Optional[Sequence[ServiceLocation]]:
    """Get available measurement services.

    Args:
        discovery_client (DiscoveryClient): Client for accessing NI Discovery service.

    Returns:
        Optional[Sequence[ServiceLocation]]: Sequence of active measurement services.
    """
    v1_measurement_services = discovery_client.enumerate_services(MEASUREMENT_SERVICE_INTERFACE_V1)
    v2_measurement_services = discovery_client.enumerate_services(MEASUREMENT_SERVICE_INTERFACE_V2)

    available_services = v1_measurement_services + v2_measurement_services
    return available_services


def get_insecure_grpc_channel_for(
    discovery_client: DiscoveryClient,
    service_class: str,
    logger: Logger,
) -> Channel:
    """Get insecure GRPC channel.

    Args:
        discovery_client (DiscoveryClient): Client for accessing NI Discovery service.
        service_class (str): Measurement Service Class name.
        logger (Logger): Logger object.

    Returns:
        Channel: Channel to server.
    """
    resolved_service = None

    try:
        resolved_service = discovery_client.resolve_service(
            MEASUREMENT_SERVICE_INTERFACE_V2,
            service_class,
        )

    except _InactiveRpcError:
        try:
            resolved_service = discovery_client.resolve_service(
                MEASUREMENT_SERVICE_INTERFACE_V1,
                service_class,
            )
        except _InactiveRpcError as exp:
            logger.debug(exp)

    finally:
        return grpc.insecure_channel(resolved_service.insecure_address)


def get_measurement_selection(total_measurements: int) -> int:
    """Prompt user to select a measurement.

    Args:
        total_measurements (int): Total measurements count.

    Returns:
        int: Selected measurement.
    """
    try:
        user_input = int(
            input(UserMessage.SELECT_MEASUREMENT.format(start=1, end=total_measurements))
        )

        if user_input not in list(range(1, total_measurements + 1)):
            raise InvalidCliInputError(UserMessage.INVALID_MEASUREMENT_CHOICE)

        return user_input

    except ValueError:
        raise InvalidCliInputError(UserMessage.ABORTED)


def get_measurement_service_stub(
    discovery_client: DiscoveryClient,
    logger: Logger,
) -> Optional[v2_measurement_service_pb2_grpc.MeasurementServiceStub]:
    """Get measurement services.

    Args:
        discovery_client (DiscoveryClient): Client for accessing NI Discovery service.
        logger (Logger): Logger object.

    Returns:
        Optional[v2_measurement_service_pb2_grpc.MeasurementServiceStub]: Measurement services.
    """
    available_services = get_active_measurement_services(discovery_client)

    if not available_services:
        logger.warning(UserMessage.NO_MEASUREMENTS_RUNNING)
        return None

    logger.info(UserMessage.AVAILABLE_MEASUREMENTS)
    for serial_num, services in enumerate(available_services):
        logger.info(f"{serial_num + 1}. {services.display_name}")

    selected_measurement = get_measurement_selection(total_measurements=len(available_services))

    channel = get_insecure_grpc_channel_for(
        discovery_client,
        available_services[selected_measurement - 1].service_class,
        logger=logger,
    )

    return v2_measurement_service_pb2_grpc.MeasurementServiceStub(channel)
