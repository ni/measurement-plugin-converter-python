"""Write xml content to a `.measui` file."""

import os

from mako.template import Template

from ni_measurement_ui_creator.constants import CLIENT_ID, ENCODING, TEMPLATE_FILEPATH


def render_template(
    template_name: str,
    client_id: str,
    display_name: str,
    input_output_elements: str,
) -> bytes:
    """Render measui mako file template.

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


def create_measui(filepath: str, input_output_elements: str) -> None:
    """Create `measui` file.

    Args:
        filepath (str): MeasUI File Path.
        input_output_elements (str): Input and Output XML tags.

    Returns:
        None.
    """
    file_content = render_template(
        template_name=TEMPLATE_FILEPATH,
        client_id=CLIENT_ID,
        display_name=os.path.basename(filepath),
        input_output_elements=input_output_elements,
    )

    with open(f"{filepath}.measui", "wb") as f:
        f.write(file_content)

    return None
