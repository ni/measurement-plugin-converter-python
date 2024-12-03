"""Implementation of file writing."""

import pathlib
from typing import Any

from mako.template import Template

from ni_measurement_plugin_converter._constants import ENCODING

TEMPLATE_DIR = "templates"


def create_file(template_name: str, file_name: str, **template_args: Any) -> None:
    """Create file.

    Args:
        template_name (str): Template file name.
        file_name (str): Output file name.
    """
    output = _render_template(template_name, **template_args)

    with open(file_name, "wb") as f:
        f.write(output)


def _render_template(template_name: str, **template_args: Any) -> bytes:
    file_dir = str(pathlib.Path(__file__).parent.parent / TEMPLATE_DIR / template_name)

    template = Template(
        filename=file_dir,
        input_encoding=ENCODING,
        output_encoding=ENCODING,
    )

    return template.render(**template_args)
