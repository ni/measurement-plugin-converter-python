"""CLI Arguments Model."""

import os

from pydantic import BaseModel, model_validator

from ni_measurement_plugin_converter.constants import UserMessage
from ni_measurement_plugin_converter.helpers import get_measurement_function


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
        
        if not get_measurement_function(self.measurement_file_dir, self.function):
            raise InvalidCliArgsError(UserMessage.FUNCTION_NOT_FOUND)

        try:
            os.makedirs(self.output_dir, exist_ok=True)
        except (PermissionError, OSError):
            raise InvalidCliArgsError(UserMessage.ACCESS_DENIED)

        return self



class InvalidCliArgsError(Exception):
    def __init__(self, message: str) -> None:
        super().__init__(message)