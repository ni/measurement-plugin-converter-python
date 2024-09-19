"""Create `.measui` file for the measurements."""

import os
from logging import getLogger
from typing import Union

from mako.template import Template
from ni_measurement_plugin_sdk_service._internal.stubs.ni.measurementlink.measurement.v1.measurement_service_pb2 import (
    GetMetadataResponse as V1MetaData,
)
from ni_measurement_plugin_sdk_service._internal.stubs.ni.measurementlink.measurement.v2.measurement_service_pb2 import (
    GetMetadataResponse as V2MetaData,
)

from ni_measurement_ui_creator.constants import CLIENT_ID, ENCODING, LOGGER, UserMessage
from ni_measurement_ui_creator.utils._ui_elements import (
    create_input_elements_from_client,
    create_output_elements_from_client,
)


def create_measui(metadata: Union[V1MetaData, V2MetaData], output_dir: str) -> None:
    """Create measurement UI file.

    1. Get inputs and outputs from the metadata.
    2. Create input elements.
    3. Create output elements.

    Args:
        metadata (Union[V1MetaData, V2MetaData]): Metadata of a measurement plug-in.
        output_dir (str): Output directory.
    """
    logger = getLogger(LOGGER)
    inputs = metadata.measurement_signature.configuration_parameters
    input_elements = create_input_elements_from_client(inputs=inputs)

    outputs = metadata.measurement_signature.outputs
    output_elements = create_output_elements_from_client(outputs=outputs)

    measui_path = os.path.join(output_dir, metadata.measurement_details.display_name)

    __create_measui(
        filepath=measui_path,
        input_output_elements=input_elements + output_elements,
    )
    logger.info(UserMessage.CREATED_UI.format(filepath=f"{measui_path}.measui"))


def __create_measui(filepath: str, input_output_elements: str) -> None:
    """Create `measui` file.

    Args:
        filepath (str): MeasUI File Path.
        input_output_elements (str): Input and Output XML tags.
    """
    current_dir = os.path.dirname(os.path.abspath(__file__))
    template_file_path = os.path.join(
        os.path.dirname(current_dir), "templates", "measurement.measui.mako"
    )

    file_content = __render_template(
        template_name=template_file_path,
        client_id=CLIENT_ID,
        display_name=os.path.basename(filepath),
        input_output_elements=input_output_elements,
    )

    with open(f"{filepath}.measui", "wb") as f:
        f.write(file_content)


def __render_template(
    template_name: str,
    client_id: str,
    display_name: str,
    input_output_elements: str,
) -> bytes:
    """Render `measui` mako file template.

    Args:
        template_name (str): Name of mako file.
        client_id (str): Client ID to be assigned in the template.
        display_name (str): Display name to be assigned in the template.
        input_output_elements (str): Inputs and Output elements of MeasUI file.

    Returns:
        bytes: MeasUI file content.
    """
    template = Template(filename=template_name, input_encoding=ENCODING, output_encoding=ENCODING)

    return template.render(
        client_id=client_id,
        display_name=display_name,
        input_output_elements=input_output_elements,
    )
