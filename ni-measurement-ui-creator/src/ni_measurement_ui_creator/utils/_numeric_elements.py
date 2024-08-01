"""Create numeric elements for building UI."""

from typing import List

from ni_measurement_ui_creator.constants import (
    MeasUIElementPosition,
    MeasUIElement,
)
from ni_measurement_ui_creator.models import DataElement, LabelElement
from ni_measurement_ui_creator.utils._common_elements import create_label, get_unique_id


def create_numeric_control(element_parameter: DataElement) -> str:
    """Create `Numeric Control` MeasUI Element .

    Args:
        element_parameter (DataElement): Numeric Control Element Parameters.

    Returns:
        str: MeasUI Numeric Control Element.
    """
    element_id = get_unique_id()
    shared_id = get_unique_id()

    numeric_control = MeasUIElement.NUMERIC_CONTROL.format(
        client_id=element_parameter.client_id,
        element_id=element_id,
        shared_id=shared_id,
        name=element_parameter.name,
        left_value=element_parameter.left_alignment,
        top_value=element_parameter.top_alignment,
        value_type=element_parameter.value_type,
    )

    label = create_label(
        element_parameter=LabelElement(
            id=shared_id,
            shared_id=shared_id,
            name=element_parameter.name,
            left_value=element_parameter.left_alignment,
            top_value=element_parameter.top_alignment,
        )
    )

    return numeric_control + label


def create_numeric_indicator(element_parameter: DataElement) -> str:
    """Create `Numeric Indicator` measui element.

    Args:
        element_parameter (DataElement): Numeric Indicator Element Parameters.

    Returns:
        str: MeasUI Numeric Indicator Element.
    """
    element_id = get_unique_id()
    shared_id = get_unique_id()

    numeric_indicator = MeasUIElement.NUMERIC_INDICATOR.format(
        client_id=element_parameter.client_id,
        element_id=element_id,
        shared_id=shared_id,
        name=element_parameter.name,
        left_value=element_parameter.left_alignment,
        top_value=element_parameter.top_alignment,
        value_type=element_parameter.value_type,
    )

    label = create_label(
        element_parameter=LabelElement(
            id=shared_id,
            shared_id=shared_id,
            name=element_parameter.name,
            left_value=element_parameter.left_alignment,
            top_value=element_parameter.top_alignment,
        )
    )

    return numeric_indicator + label


def create_numeric_array_input(element_parameter: DataElement) -> str:
    """Create `Numeric Array Input` MeasUI Element.

    Args:
        element_parameter (DataElement): Numeric Array Input Element Parameters.

    Returns:
        str: MeasUI Numeric Array Input Element.
    """
    array_element_id = get_unique_id()
    shared_id = get_unique_id()
    label_id = get_unique_id()

    numeric_array = MeasUIElement.NUMERIC_ARRAY_INPUT.format(
        client_id=element_parameter.client_id,
        array_element_id=array_element_id,
        shared_id=shared_id,
        label_id=label_id,
        name=element_parameter.name,
        left_value=element_parameter.left_alignment,
        value_type=element_parameter.value_type,
        top_value=element_parameter.top_alignment,
    )

    label = create_label(
        element_parameter=LabelElement(
            id=label_id,
            shared_id=shared_id,
            name=element_parameter.name,
            left_value=element_parameter.left_alignment,
            top_value=element_parameter.top_alignment,
        )
    )

    return numeric_array + label


def create_numeric_array_control(element_parameter: DataElement) -> str:
    """Create `Numeric Array Output` MeasUI Element.

    Args:
        element_parameter (DataElement): Numeric Array Output Element Parameters.

    Returns:
        str: MeasUI Array Output Element.
    """
    array_element_id = get_unique_id()
    shared_id = get_unique_id()
    label_id = get_unique_id()

    numeric_array = MeasUIElement.NUMERIC_ARRAY_OUTPUT.format(
        client_id=element_parameter.client_id,
        array_element_id=array_element_id,
        shared_id=shared_id,
        label_id=label_id,
        name=element_parameter.name,
        left_value=element_parameter.left_alignment,
        value_type=element_parameter.value_type,
        top_value=element_parameter.top_alignment,
    )

    label = create_label(
        element_parameter=LabelElement(
            id=label_id,
            shared_id=shared_id,
            name=element_parameter.name,
            left_value=element_parameter.left_alignment,
            top_value=element_parameter.top_alignment,
        )
    )

    return numeric_array + label


def create_numeric_indicators(elements_parameter: List[DataElement]) -> str:
    """Create Multiple `Numeric Indicator` MeasUI Elements.

    Args:
        elements_parameter (List[DataElement]): List of Numeric Indicator Element parameters.

    Returns:
        str: MeasUI Numeric Indicator Elements.
    """
    numeric_indicators = ""
    top_value = MeasUIElementPosition.TOP_START_VALUE

    for element_parameter in elements_parameter:
        element_parameter.left_alignment = (
            MeasUIElementPosition.LEFT_START_VALUE + MeasUIElementPosition.LEFT_INCREMENTAL_VALUE
        )
        element_parameter.top_alignment = top_value
        top_value += MeasUIElementPosition.TOP_INCREMENTAL_VALUE

        numeric_indicators += create_numeric_indicator(element_parameter=element_parameter)

    return numeric_indicators


def create_numeric_array_inputs(elements_parameter: List[DataElement]) -> str:
    """Create Multiple `Numeric Array Input` MeasUI Elements.

    Args:
        element_parameter (List[DataElement]): Numeric Array Input Element Parameters.

    Returns:
        str: MeasUI Numeric Array Input Elements.
    """
    numeric_array_inputs = ""
    top_value = MeasUIElementPosition.TOP_START_VALUE

    for element_parameter in elements_parameter:
        element_parameter.top_alignment = top_value
        top_value += MeasUIElementPosition.TOP_INCREMENTAL_VALUE

        numeric_array_inputs += create_numeric_array_input(element_parameter=element_parameter)

    return numeric_array_inputs


def create_numeric_array_outputs(elements_parameter: List[DataElement]) -> str:
    """Create Multiple `Numeric Array Output` MeasUI Elements.

    Args:
        element_parameter (List[DataElement]): List of Numeric Array Output Element \
            parameters.

    Returns:
        str: MeasUI Array Output Elements.
    """
    numeric_array_outputs = ""
    top_value = MeasUIElementPosition.TOP_START_VALUE

    for element_parameter in elements_parameter:
        element_parameter.left_alignment = (
            MeasUIElementPosition.LEFT_START_VALUE + MeasUIElementPosition.LEFT_INCREMENTAL_VALUE
        )
        element_parameter.top_alignment = top_value
        top_value += MeasUIElementPosition.TOP_INCREMENTAL_VALUE

        numeric_array_outputs += create_numeric_array_control(element_parameter=element_parameter)

    return numeric_array_outputs


def create_numeric_controls(elements_parameter: List[DataElement]) -> str:
    """Create Multiple `Numeric Control` MeasUI Elements.

    Args:
        elements_parameter (List[DataElement]): List of Numeric Control Element Parameters.

    Returns:
        str: MeasUI Numeric control Elements.
    """
    numeric_controls = ""
    top_value = MeasUIElementPosition.TOP_START_VALUE

    for element_parameter in elements_parameter:
        element_parameter.top_alignment = top_value
        top_value += MeasUIElementPosition.TOP_INCREMENTAL_VALUE

        numeric_controls += create_numeric_control(element_parameter=element_parameter)

    return numeric_controls
