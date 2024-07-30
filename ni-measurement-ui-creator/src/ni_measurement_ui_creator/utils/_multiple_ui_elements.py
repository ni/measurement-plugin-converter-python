"""Helpers to create multiple numeric control, numeric indicator, numeric array input and \
numeric array output."""

from typing import List

from ni_measurement_ui_creator.constants import MeasUiElementPosition
from ni_measurement_ui_creator.models import DataElement
from ni_measurement_ui_creator.utils._helpers import (
    create_numeric_array_input,
    create_numeric_array_output,
    create_numeric_control,
    create_numeric_indicator,
    create_string_control,
    create_string_indicator,
    create_toggle_image_button,
    create_toggle_image_indicator,
)


def create_numeric_controls(elements_parameter: List[DataElement]) -> str:
    """Create Multiple `Numeric Control` MeasUI Elements.

    Args:
        elements_parameter (List[DataElement]): List of Numeric Control Element Parameters.

    Returns:
        str: MeasUI Numeric control Elements.
    """
    numeric_controls = ""
    top_value = MeasUiElementPosition.TOP_START_VALUE

    for element_parameter in elements_parameter:
        element_parameter.top_value = top_value
        top_value += MeasUiElementPosition.TOP_INCREMENTAL_VALUE

        numeric_controls += create_numeric_control(element_parameter=element_parameter)

    return numeric_controls


def create_numeric_indicators(elements_parameter: List[DataElement]) -> str:
    """Create Multiple `Numeric Indicator` MeasUI Elements.

    Args:
        elements_parameter (List[DataElement]): List of Numeric Indicator Element parameters.

    Returns:
        str: MeasUI Numeric Indicator Elements.
    """
    numeric_indicators = ""
    top_value = MeasUiElementPosition.TOP_START_VALUE

    for element_parameter in elements_parameter:
        element_parameter.left_value = (
            MeasUiElementPosition.LEFT_START_VALUE + MeasUiElementPosition.LEFT_INCREMENTAL_VALUE
        )
        element_parameter.top_value = top_value
        top_value += MeasUiElementPosition.TOP_INCREMENTAL_VALUE

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
    top_value = MeasUiElementPosition.TOP_START_VALUE

    for element_parameter in elements_parameter:
        element_parameter.top_value = top_value
        top_value += MeasUiElementPosition.TOP_INCREMENTAL_VALUE

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
    top_value = MeasUiElementPosition.TOP_START_VALUE

    for element_parameter in elements_parameter:
        element_parameter.left_value = (
            MeasUiElementPosition.LEFT_START_VALUE + MeasUiElementPosition.LEFT_INCREMENTAL_VALUE
        )
        element_parameter.top_value = top_value
        top_value += MeasUiElementPosition.TOP_INCREMENTAL_VALUE

        numeric_array_outputs += create_numeric_array_output(element_parameter=element_parameter)

    return numeric_array_outputs


def create_string_controls(elements_parameter: List[DataElement]) -> str:
    """Create Multiple `String Control` MeasUI Elements.

    Args:
        elements_parameter (List[DataElement]): List of String Control Element Parameters.

    Returns:
        str: MeasUI String Control Elements.
    """
    string_controls = ""
    top_value = MeasUiElementPosition.TOP_START_VALUE

    for element_parameter in elements_parameter:
        element_parameter.top_value = top_value
        top_value += MeasUiElementPosition.TOP_INCREMENTAL_VALUE

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
    top_value = MeasUiElementPosition.TOP_START_VALUE

    for element_parameter in elements_parameter:
        element_parameter.left_value = (
            MeasUiElementPosition.LEFT_START_VALUE + MeasUiElementPosition.LEFT_INCREMENTAL_VALUE
        )
        element_parameter.top_value = top_value
        top_value += MeasUiElementPosition.TOP_INCREMENTAL_VALUE

        string_indicators += create_string_indicator(element_parameter=element_parameter)

    return string_indicators


def create_toggle_image_buttons(elements_parameter: List[DataElement]) -> str:
    """Create Multiple `Toggle Image Button` MeasUI Elements.

    Args:
        elements_parameter (List[DataElement]): List of Toggle Image Button Element \
            Parameters.

    Returns:
        str: MeasUI Toggle Image Button Elements.
    """
    toggle_image_buttons = ""
    top_value = MeasUiElementPosition.TOP_START_VALUE

    for element_parameter in elements_parameter:
        element_parameter.top_value = top_value
        top_value += MeasUiElementPosition.TOP_INCREMENTAL_VALUE

        toggle_image_buttons += create_toggle_image_button(element_parameter=element_parameter)

    return toggle_image_buttons


def create_toggle_image_indicators(elements_parameter: List[DataElement]) -> str:
    """Create Multiple `Toggle Image Indicator` MeasUI Elements.

    Args:
        elements_parameter (List[DataElement]): List of Toggle Image Indicator Element \
            Parameters.

    Returns:
        str: MeasUI Toggle Image Indicator Elements.
    """
    toggle_image_indicators = ""
    top_value = MeasUiElementPosition.TOP_START_VALUE

    for element_parameter in elements_parameter:
        element_parameter.left_value = (
            MeasUiElementPosition.LEFT_START_VALUE + MeasUiElementPosition.LEFT_INCREMENTAL_VALUE
        )
        element_parameter.top_value = top_value
        top_value += MeasUiElementPosition.TOP_INCREMENTAL_VALUE

        toggle_image_indicators += create_toggle_image_indicator(
            element_parameter=element_parameter
        )

    return toggle_image_indicators
