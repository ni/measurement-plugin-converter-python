"""CLI tool to create measui from Measurement Plug-Ins."""

import os
from pathlib import Path

import click
from ni_measurementlink_service._internal.stubs.ni.measurementlink.measurement.v2 import (
    measurement_service_pb2 as v2_measurement_service_pb2,
)
from ni_measurementlink_service.discovery import DiscoveryClient

from ni_measurement_ui_creator.constants import (
    CLI_CONTEXT_SETTINGS,
    SUPPORTED_UI_ELEMENTS,
    CliHelpMessage,
    UserMessage,
)
from ni_measurement_ui_creator.utils._client import get_measurement_service_stub
from ni_measurement_ui_creator.utils._exceptions import InvalidCliInputError
from ni_measurement_ui_creator.utils._logger import get_logger
from ni_measurement_ui_creator.utils._ui_elements import (
    create_input_elements_from_client,
    create_output_elements_from_client,
)
from ni_measurement_ui_creator.utils._write_xml import write_to_xml


@click.command(context_settings=CLI_CONTEXT_SETTINGS)
@click.option(
    "-o",
    "--output-dir",
    type=click.Path(),
    required=True,
    help=CliHelpMessage.OUTPUT_FOLDER,
)
def run(output_dir: Path):
    """NI Measurement UI Creator is a CLI tool to create measui file from running \
measurement services."""
    try:
        log_file_path = os.path.join(output_dir, "Logs")
        logger = get_logger(log_file_path=log_file_path)

        logger.info(UserMessage.STARTING)
        logger.info(UserMessage.SUPPORTED_ELEMENTS.format(elements=SUPPORTED_UI_ELEMENTS))
        logger.info(UserMessage.GET_MEASUREMENTS_RUNNING)

        os.environ["GRPC_VERBOSITY"] = "NONE"
        discovery_client = DiscoveryClient()
        measurement_service_stub = get_measurement_service_stub(discovery_client, logger=logger)

        if measurement_service_stub:
            metadata = measurement_service_stub.GetMetadata(
                v2_measurement_service_pb2.GetMetadataRequest()
            )
            inputs = metadata.measurement_signature.configuration_parameters
            input_elements = create_input_elements_from_client(inputs=inputs)

            outputs = metadata.measurement_signature.outputs
            output_elements = create_output_elements_from_client(outputs=outputs)

            filepath = os.path.join(output_dir, metadata.measurement_details.display_name)

            write_to_xml(
                filepath=filepath,
                input_output_elements=input_elements + output_elements,
            )
            logger.info(UserMessage.CREATED_UI.format(filepath=f"{filepath}.measui"))

    except InvalidCliInputError as error:
        logger.warning(error)

    except Exception as error:
        logger.debug(error, exc_info=True)
        logger.warning(UserMessage.ERROR_OCCURRED)

    finally:
        logger.info(UserMessage.PROCESS_COMPLETED)
