"""Implementation of file writing."""

from pathlib import Path
from typing import Any

from mako.template import Template

from ni_measurement_plugin_converter._constants import ENCODING

TEMPLATE_DIR = "templates"


def _render_template(template_name: str, **template_args: Any) -> bytes:
    file_dir = str(Path(__file__).parent.parent / TEMPLATE_DIR / template_name)

    template = Template(  # nosec: B702
        filename=file_dir,
        input_encoding=ENCODING,
        output_encoding=ENCODING,
    )

    return template.render(**template_args)


def create_file(template_name: str, file_path: Path, **template_args: Any) -> None:
    """Create a file by rendering a template with provided arguments.

    Args:
        template_name: The name of the template file to render.
        file_path: The path to the output file.
        **template_args: Arguments to pass to the template during rendering.
    """
    output = _render_template(template_name, **template_args)

    with open(file_path, "wb") as f:
        f.write(output)
