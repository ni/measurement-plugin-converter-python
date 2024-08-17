"""UI Elements Base Model."""

from typing import Optional, Union
from uuid import UUID

from pydantic import BaseModel, Field


class DataElement(BaseModel):
    """Data Element Model."""

    client_id: UUID
    name: str
    left_alignment: Optional[Union[int, float]] = Field(default=100)
    top_alignment: Optional[Union[int, float]] = Field(default=100)
    height: Optional[Union[int, float]] = Field(default=25)
    width: Optional[Union[int, float]] = Field(default=120)
    rows: Optional[Union[int]] = Field(default=3)
    value_type: Optional[str] = Field(default=None)
    is_array: Optional[bool] = Field(default=None)


class LabelElement(BaseModel):
    """Label Element Model."""

    id: str
    shared_id: str
    name: str
    left_alignment: Optional[Union[int, float]] = Field(default=100)
    top_alignment: Optional[Union[int, float]] = Field(default=100)
    height: Optional[Union[int, float]] = Field(default=25)
    width: Optional[Union[int, float]] = Field(default=120)
