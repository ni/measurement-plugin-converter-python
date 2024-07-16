"""Models for NI Measurement Converter CLI Arguments."""

import os

from pydantic import BaseModel, model_validator

from ni_measurement_plugin_converter.constants import UserMessages


class CliInputs(BaseModel):
    """Represent Command Line Interface inputs."""

    service_name: str
    measurement_file_dir: str
    function: str

    @model_validator(mode="after")
    def validate_cli_inputs(self) -> "CliInputs":
        """Validate the CLI inputs.

        Returns:
            CliInputs: Validated CLI inputs.
        """
        if not os.path.exists(self.measurement_file_dir):
            raise FileNotFoundError(UserMessages.INVALID_FILE_DIR)

        base_path = os.path.dirname(self.measurement_file_dir)
        measurement_plugin = os.path.join(base_path, self.service_name)
        try:
            os.makedirs(measurement_plugin, exist_ok=True)
        except (PermissionError, OSError) as error:
            raise error

        return self
