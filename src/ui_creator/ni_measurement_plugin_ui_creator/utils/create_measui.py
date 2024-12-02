"""Create `.measui` file for the measurements."""

from logging import getLogger
from pathlib import Path
from typing import Union
from uuid import UUID

from mako.template import Template
from ni_measurement_plugin_sdk_service._internal.stubs.ni.measurementlink.measurement.v1.measurement_service_pb2 import (
    GetMetadataResponse as V1MetaData,
)
from ni_measurement_plugin_sdk_service._internal.stubs.ni.measurementlink.measurement.v2.measurement_service_pb2 import (
    GetMetadataResponse as V2MetaData,
)

from ni_measurement_plugin_ui_creator.constants import CLIENT_ID, LOGGER, MeasUIFile
from ni_measurement_plugin_ui_creator.utils.ui_elements import (
    create_input_elements_from_client,
    create_output_elements_from_client,
)

CREATING_FILE = "Creating Measurement Plug-In UI..."
CREATED_UI = "Measurement Plug-In UI created successfully at {filepath}."


def create_measui(
    metadata: Union[V1MetaData, V2MetaData],
    service_class: str,
    output_dir: Path,
) -> None:
    """Create measurement UI file.

    Args:
        metadata (Union[V1MetaData, V2MetaData]): Metadata of a measurement plug-in.
        service_class (str): Service class name of a measurement plug-in.
        output_dir (Path): Output directory.
    """
    logger = getLogger(LOGGER)
    logger.debug(CREATING_FILE)

    inputs = metadata.measurement_signature.configuration_parameters
    input_elements, _ = create_input_elements_from_client(inputs=inputs)

    outputs = metadata.measurement_signature.outputs
    output_elements = create_output_elements_from_client(outputs=outputs)

    measui_path = Path(output_dir) / metadata.measurement_details.display_name

    write_measui(
        filepath=measui_path,
        service_class=service_class,
        input_output_elements=input_elements + output_elements,
    )
    filepath = (Path(measui_path).with_suffix(MeasUIFile.MEASUREMENT_UI_FILE_EXTENSION)).resolve()
    logger.info(CREATED_UI.format(filepath=Path(filepath).resolve()))


def write_measui(filepath: Path, service_class: str, input_output_elements: str) -> None:
    """Write `measui` file.

    Args:
        filepath (Path): File path.
        service_class (str): Service class name of the measurement plug-in.
        input_output_elements (str): Input and Output XML tags.
    """
    current_dir = Path(__file__).resolve().parent
    template_file_path = current_dir.parent / "templates" / "measurement.measui.mako"

    file_content = _render_template(
        template_name=str(template_file_path),
        client_id=CLIENT_ID,
        display_name=Path(filepath).name,
        service_class=service_class,
        input_output_elements=input_output_elements,
    )

    with open(f"{filepath}{MeasUIFile.MEASUREMENT_UI_FILE_EXTENSION}", "wb") as f:
        f.write(file_content)


def _render_template(
    template_name: str,
    client_id: Union[str, UUID],
    display_name: str,
    service_class: str,
    input_output_elements: str,
) -> bytes:
    """Render `measui` mako file template.

    Args:
        template_name (str): Name of mako file.
        client_id (Union[str, UUUID]): Client ID to be assigned in the template.
        display_name (str): Display name to be assigned in the template.
        service_class (str): Service class name of the measurement plug-in.
        input_output_elements (str): Inputs and Output elements of MeasUI file.

    Returns:
        bytes: MeasUI file content.
    """
    template = Template(  # nosec: B702
        filename=template_name,
        input_encoding=MeasUIFile.ENCODING,
        output_encoding=MeasUIFile.ENCODING,
    )

    return template.render(
        client_id=client_id,
        display_name=display_name,
        service_class=service_class,
        input_output_elements=input_output_elements,
    )
