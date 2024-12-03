"""Models utilized in Command Line Interface implementation."""

import ast
from pathlib import Path
from typing import Optional

from pydantic import BaseModel, model_validator

from ni_measurement_plugin_converter.constants import ENCODING, UserMessage
from ._exceptions import InvalidCliArgsError


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
            raise InvalidCliArgsError(UserMessage.INVALID_FILE_DIR)

        if not self.validate_function():
            raise InvalidCliArgsError(
                UserMessage.FUNCTION_NOT_FOUND.format(
                    function=self.function,
                    measurement_file_dir=self.measurement_file_dir,
                )
            )

        try:
            output_dir_path.mkdir(parents=True, exist_ok=True)
        except (PermissionError, OSError):
            raise InvalidCliArgsError(UserMessage.ACCESS_DENIED)

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
