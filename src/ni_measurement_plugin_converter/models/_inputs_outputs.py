"""Inputs and Outputs Models."""

from typing import List, Union

from pydantic import BaseModel


class InputConfigurations(BaseModel):
    """Measurement inputs configurations."""

    param_name: str
    param_type: str
    nims_type: str
    default_value: Union[int, float, str, bool, List[int], List[float], List[str], List[bool]]


class OutputConfigurations(BaseModel):
    """Measurement outputs configurations."""

    variable_name: str
    variable_type: str
    nims_type: str
