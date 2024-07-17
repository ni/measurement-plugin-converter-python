"""CLI Arguments Model."""

import ast
import os
from typing import Union

from pydantic import BaseModel, model_validator

from ni_measurement_plugin_converter.constants import UserMessage


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
        if not os.path.exists(self.measurement_file_dir):
            raise InvalidCliArgsError(UserMessage.INVALID_FILE_DIR)

        if not self.validate_function():
            raise InvalidCliArgsError(UserMessage.FUNCTION_NOT_FOUND)

        try:
            os.makedirs(self.output_dir, exist_ok=True)
        except (PermissionError, OSError):
            raise InvalidCliArgsError(UserMessage.ACCESS_DENIED)

        return self

    def validate_function(self) -> Union[ast.FunctionDef, None]:
        """Validate the CLI inputs.

        Returns:
            Union[ast.FunctionDef, None]: Function node if function is found in measurement file. \
                Else `None` is returned.
        """
        with open(self.measurement_file_dir, "r") as file:
            code = file.read()

        code_tree = ast.parse(code)

        for node in ast.walk(code_tree):
            if isinstance(node, ast.FunctionDef) and node.name == self.function:
                function_node = node
                break

        return function_node


class InvalidCliArgsError(Exception):
    """Invalid CLI arguments error."""

    def __init__(self, message: str) -> None:
        """Initialize the exception.

        Args:
            message (str): Error message.
        """
        super().__init__(message)
