"""UI Elements Base Model."""

from typing import Optional, Union, Dict
from uuid import UUID

from pydantic import BaseModel, Field

from ni_measurement_ui_creator.constants import MeasUIElementPosition


class DataElement(BaseModel):
    """Data Element Model."""

    client_id: UUID
    name: str
    left_alignment: Optional[Union[int, float]] = Field(
        default=MeasUIElementPosition.DEFAULT_LEFT_ALIGNMENT
    )
    top_alignment: Optional[Union[int, float]] = Field(
        default=MeasUIElementPosition.DEFAULT_TOP_ALIGNMENT
    )

    height: Optional[Union[int, float]] = Field(default=MeasUIElementPosition.DEFAULT_HEIGHT)
    width: Optional[Union[int, float]] = Field(default=MeasUIElementPosition.DEFAULT_WIDTH)
    rows: Optional[Union[int]] = Field(default=MeasUIElementPosition.DEFAULT_ARRAY_ROWS)

    value_type: Optional[str] = Field(default=None)
    is_array: Optional[bool] = Field(default=None)


class LabelElement(BaseModel):
    """Label Element Model."""

    id: str
    shared_id: str
    name: str
    left_alignment: Optional[Union[int, float]] = Field(
        default=MeasUIElementPosition.DEFAULT_LEFT_ALIGNMENT
    )
    top_alignment: Optional[Union[int, float]] = Field(
        default=MeasUIElementPosition.DEFAULT_TOP_ALIGNMENT
    )


class UpdateElement(BaseModel):
    """Elements available in measui file to be updated."""

    tag: str
    bind: bool
    name: Optional[str]
    output: Optional[bool]
    attrib: Dict[str, str]
