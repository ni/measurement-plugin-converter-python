"""Models utilized in Command Line Interface implementation."""

import ast
from pathlib import Path
from typing import Optional

from pydantic import BaseModel, model_validator

from ni_measurement_plugin_converter.models._exceptions import InvalidCliArgsError

INVALID_FILE_DIR = (
    "Invalid measurement file directory. Please provide valid measurement file directory."
)
FUNCTION_NOT_FOUND = "Measurement function {function} not found in the file {measurement_file_dir}"
ACCESS_DENIED = (
    "Access is denied. "
    "Please run the tool with Admin privileges or provide a different file directory."
)
ENCODING = "utf-8"


class CliInputs(BaseModel):
    """Command Line Interface inputs."""

    display_name: str
    measurement_file_dir: str
    function: str
    output_dir: str

    @model_validator(mode="after")
    def validate_cli_inputs(self) -> "CliInputs":
        """Validate the CLI inputs.

        Returns:
            CliInputs: Validated CLI inputs.
        """
        measurement_file_path = Path(self.measurement_file_dir)
        output_dir_path = Path(self.output_dir)

        if not measurement_file_path.exists():
            raise InvalidCliArgsError(INVALID_FILE_DIR)

        if not self.validate_function():
            raise InvalidCliArgsError(
                FUNCTION_NOT_FOUND.format(
                    function=self.function,
                    measurement_file_dir=self.measurement_file_dir,
                )
            )

        try:
            output_dir_path.mkdir(parents=True, exist_ok=True)
        except (PermissionError, OSError):
            raise InvalidCliArgsError(ACCESS_DENIED)

        return self

    def validate_function(self) -> Optional[ast.FunctionDef]:
        """Validate the CLI inputs.

        Returns:
            Optional[ast.FunctionDef]: Function node if function is found in measurement file. \
                Else `None` is returned.
        """
        function_node = None
        measurement_file_path = Path(self.measurement_file_dir)

        with measurement_file_path.open("r", encoding=ENCODING) as file:
            code = file.read()

        code_tree = ast.parse(code)

        for node in ast.walk(code_tree):
            if isinstance(node, ast.FunctionDef) and node.name == self.function:
                function_node = node
                break

        return function_node
