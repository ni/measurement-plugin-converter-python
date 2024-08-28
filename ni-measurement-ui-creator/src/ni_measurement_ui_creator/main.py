"""Command-line tool to create measui for measurements."""

import os
from pathlib import Path

import click
from ni_measurement_plugin_sdk_service._internal.stubs.ni.measurementlink.measurement.v2 import (
    measurement_service_pb2 as v2_measurement_service_pb2,
)
from ni_measurement_plugin_sdk_service.discovery import DiscoveryClient

from ni_measurement_ui_creator.constants import (
    CLI_CONTEXT_SETTINGS,
    SUPPORTED_UI_ELEMENTS,
    CliHelpMessage,
    UserMessage,
)
from ni_measurement_ui_creator.utils._client import get_measurement_service_stub
from ni_measurement_ui_creator.utils._create_measui import create_measui
from ni_measurement_ui_creator.utils._exceptions import InvalidCliInputError
from ni_measurement_ui_creator.utils._logger import get_logger
from ni_measurement_ui_creator.utils._ui_elements import (
    create_input_elements_from_client,
    create_output_elements_from_client,
)


@click.command(context_settings=CLI_CONTEXT_SETTINGS)
@click.option(
    "-o",
    "--output-dir",
    type=click.Path(),
    required=True,
    help=CliHelpMessage.OUTPUT_FOLDER,
)
def run(output_dir: Path) -> None:
    """NI Measurement UI Creator is a Command Line tool for creating measui files."""
    try:
        log_file_path = os.path.join(output_dir, "Logs")
        logger = get_logger(log_file_path=log_file_path)

        logger.info(UserMessage.CLI_STARTING)
        logger.info(UserMessage.SUPPORTED_ELEMENTS.format(elements=SUPPORTED_UI_ELEMENTS))
        logger.info(UserMessage.GET_ACTIVE_MEASUREMENTS)

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

            measui_path = os.path.join(output_dir, metadata.measurement_details.display_name)

            create_measui(
                filepath=measui_path,
                input_output_elements=input_elements + output_elements,
            )
            logger.info(UserMessage.CREATED_UI.format(filepath=f"{measui_path}.measui"))
            raise Exception

    except InvalidCliInputError as error:
        logger.error(error)

    except Exception as error:
        logger.debug(error, exc_info=True)
        logger.error(UserMessage.ERROR_OCCURRED.format(log_file=logger.handlers[0].baseFilename))

    finally:
        logger.info(UserMessage.PROCESS_COMPLETED)
