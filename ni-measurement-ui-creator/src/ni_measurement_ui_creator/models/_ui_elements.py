"""UI Elements Base Model."""

import xml.etree.ElementTree as ETree
from typing import Dict, Optional, Union
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


class AvlbleElement(BaseModel):
    """Elements available in measui file to be updated."""

    tag: str
    element: ETree.Element
    attrib: Dict[str, str]
    output: Optional[bool]
    bind: Optional[bool]
    name: Optional[str]

    class Config:
        """To allow non pydantic types."""

        arbitrary_types_allowed = True
