"""Models utilized in inputs and outputs extraction."""

from typing import List, Union

from pydantic import BaseModel


class InputInfo(BaseModel):
    """Measurement function input's info."""

    param_name: str
    param_type: str
    nims_type: str
    default_value: Union[int, float, str, bool, List[int], List[float], List[str], List[bool]]


class OutputInfo(BaseModel):
    """Measurement function output's info."""

    variable_name: str
    variable_type: str
    nims_type: str


class PinInfo(BaseModel):
    """Measurement function Pin's info."""

    name: str
    instrument_type: str
    default_value: str


class RelayInfo(BaseModel):
    """Measurement function Relay's info."""

    name: str
    default_value: str
