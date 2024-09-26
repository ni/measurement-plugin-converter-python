"""Create string elements for building UI."""

from typing import List

from ni_measurement_ui_creator.constants import (
    MeasUIElementPosition,
    MeasUIElement,
)
from ni_measurement_ui_creator.models import DataElement, LabelElement
from ni_measurement_ui_creator.utils._common_elements import create_label, get_unique_id


def create_string_control(element_parameter: DataElement) -> str:
    """Create `String Control` MeasUI Element.

    Args:
        element_parameter (DataElement): String Control Element Parameters.

    Returns:
        str: MeasUI String Control Element.
    """
    label_id = get_unique_id()
    shared_id = get_unique_id()

    string_control = MeasUIElement.STRING_CONTROL.format(
        client_id=element_parameter.client_id,
        name=element_parameter.name,
        label_id=label_id,
        shared_id=shared_id,
        left_value=element_parameter.left_alignment,
        top_value=element_parameter.top_alignment,
        height=element_parameter.height,
        width=element_parameter.width,
    )

    label = create_label(
        element_parameter=LabelElement(
            id=label_id,
            shared_id=shared_id,
            name=element_parameter.name,
            left_alignment=element_parameter.left_alignment,
            top_alignment=element_parameter.top_alignment,
        )
    )

    return string_control + label


def create_string_indicator(element_parameter: DataElement) -> str:
    """Create `String Indicator` MeasUI Element.

    Args:
        element_parameter (DataElement): String Indicator Element Parameters.

    Returns:
        str: MeasUI String Indicator Element.
    """
    label_id = get_unique_id()
    shared_id = get_unique_id()

    string_indicator = MeasUIElement.STRING_INDICATOR.format(
        client_id=element_parameter.client_id,
        name=element_parameter.name,
        label_id=label_id,
        shared_id=shared_id,
        left_value=element_parameter.left_alignment,
        top_value=element_parameter.top_alignment,
        height=element_parameter.height,
        width=element_parameter.width,
    )

    label = create_label(
        element_parameter=LabelElement(
            id=label_id,
            shared_id=shared_id,
            name=element_parameter.name,
            left_alignment=element_parameter.left_alignment,
            top_alignment=element_parameter.top_alignment,
        )
    )

    return string_indicator + label


def create_string_controls(elements_parameter: List[DataElement]) -> str:
    """Create Multiple `String Control` MeasUI Elements.

    Args:
        elements_parameter (List[DataElement]): List of String Control Element Parameters.

    Returns:
        str: MeasUI String Control Elements.
    """
    string_controls = ""
    top_alignment = MeasUIElementPosition.TOP_ALIGNMENT_START_VALUE

    for element_parameter in elements_parameter:
        element_parameter.top_alignment = top_alignment
        top_alignment += MeasUIElementPosition.TOP_ALIGNMENT_INCREMENTAL_VALUE

        string_controls += create_string_control(element_parameter=element_parameter)

    return string_controls


def create_string_indicators(elements_parameter: List[DataElement]) -> str:
    """Create Multiple `String Indicators` MeasUI Elements.

    Args:
        elements_parameter (List[DataElement]): List of String Indicator Element Parameters.

    Returns:
        str: MeasUI String Indicator Elements.
    """
    string_indicators = ""
    top_alignment = MeasUIElementPosition.TOP_ALIGNMENT_START_VALUE

    for element_parameter in elements_parameter:
        element_parameter.left_alignment = (
            MeasUIElementPosition.LEFT_ALIGNMENT_START_VALUE
            + MeasUIElementPosition.LEFT_ALIGNMENT_INCREMENTAL_VALUE
        )
        element_parameter.top_alignment = top_alignment
        top_alignment += MeasUIElementPosition.TOP_ALIGNMENT_INCREMENTAL_VALUE

        string_indicators += create_string_indicator(element_parameter=element_parameter)

    return string_indicators


def create_string_array_control(element_parameter: DataElement) -> str:
    """Create `String Array Input` MeasUI Element.

    Args:
        element_parameter (DataElement): String Array Input Element Parameters.

    Returns:
        str: MeasUI String Array Input Element.
    """
    array_element_id = get_unique_id()
    shared_id = get_unique_id()
    label_id = get_unique_id()

    string_array = MeasUIElement.STRING_ARRAY_INPUT.format(
        client_id=element_parameter.client_id,
        array_element_id=array_element_id,
        shared_id=shared_id,
        label_id=label_id,
        name=element_parameter.name,
        left_value=element_parameter.left_alignment,
        value_type=element_parameter.value_type,
        top_value=element_parameter.top_alignment,
        height=element_parameter.height,
        width=element_parameter.width,
        rows=element_parameter.rows,
    )

    label = create_label(
        element_parameter=LabelElement(
            id=label_id,
            shared_id=shared_id,
            name=element_parameter.name,
            left_alignment=element_parameter.left_alignment,
            top_alignment=element_parameter.top_alignment,
        )
    )

    return string_array + label


def create_string_array_indicator(element_parameter: DataElement) -> str:
    """Create `String Array Output` MeasUI Element.

    Args:
        element_parameter (DataElement): String Array Output Element Parameters.

    Returns:
        str: MeasUI Sting Array Output Element.
    """
    array_element_id = get_unique_id()
    shared_id = get_unique_id()
    label_id = get_unique_id()

    string_array = MeasUIElement.STRING_ARRAY_OUTPUT.format(
        client_id=element_parameter.client_id,
        array_element_id=array_element_id,
        shared_id=shared_id,
        label_id=label_id,
        name=element_parameter.name,
        left_value=element_parameter.left_alignment,
        value_type=element_parameter.value_type,
        top_value=element_parameter.top_alignment,
        height=element_parameter.height,
        width=element_parameter.width,
        rows=element_parameter.rows,
    )

    label = create_label(
        element_parameter=LabelElement(
            id=label_id,
            shared_id=shared_id,
            name=element_parameter.name,
            left_alignment=element_parameter.left_alignment,
            top_alignment=element_parameter.top_alignment,
        )
    )

    return string_array + label
