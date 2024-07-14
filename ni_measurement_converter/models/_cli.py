"""Models for NI Measurement Converter CLI Arguments."""

import os

from pydantic import BaseModel, model_validator

from ni_measurement_converter.constants import UserMessages


class CliInputs(BaseModel):
    """Represent Command Line Interface inputs."""

    display_name: str
    file_dir: str
    method_name: str

    @model_validator(mode="after")
    def validate_cli_inputs(self) -> "CliInputs":
        """Validate the CLI inputs.

        Returns:
            CliInputs: Validated CLI inputs.
        """
        if not os.path.exists(self.file_dir):
            raise FileNotFoundError(UserMessages.INVALID_FILE_DIR)

        base_path = os.path.dirname(self.file_dir)
        measurement_plugin = os.path.join(base_path, self.display_name)
        try:
            os.makedirs(measurement_plugin, exist_ok=True)
        except (PermissionError, OSError) as error:
            raise error

        return self
