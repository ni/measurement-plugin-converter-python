"""Create toggle elements for building UI."""

from typing import List

from ni_measurement_ui_creator.constants import (
    MeasUIElementPosition,
    MeasUIElement,
)
from ni_measurement_ui_creator.models import DataElement, LabelElement
from ni_measurement_ui_creator.utils._common_elements import create_label, get_unique_id


def create_toggle_image_button(element_parameter: DataElement) -> str:
    """Create `Toggle Image Button` MeasUI Element.

    Args:
        element_parameter (DataElement): Toggle Image Button Element Parameters.

    Returns:
        str: MeasUI Toggle Image Button Element.
    """
    true_image_id = get_unique_id()
    false_image_id = get_unique_id()

    shared_id = get_unique_id()
    label_id = get_unique_id()

    toggle_image_button = MeasUIElement.TOGGLE_IMAGE_BUTTON.format(
        client_id=element_parameter.client_id,
        name=element_parameter.name,
        false_image_id=false_image_id,
        true_image_id=true_image_id,
        label_id=label_id,
        shared_id=shared_id,
        left_value=element_parameter.left_alignment,
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

    return toggle_image_button + label


def create_toggle_image_indicator(element_parameter: DataElement) -> str:
    """Create `Toggle Image Indicator` MeasUI Element.

    Args:
        element_parameter (DataElement): Toggle Image Indicator Element Parameters.

    Returns:
        str: MeasUI Toggle Image Indicator Element.
    """
    true_image_id = get_unique_id()
    false_image_id = get_unique_id()

    shared_id = get_unique_id()
    label_id = get_unique_id()

    toggle_image_button = MeasUIElement.TOGGLE_IMAGE_INDICATOR.format(
        client_id=element_parameter.client_id,
        name=element_parameter.name,
        false_image_id=false_image_id,
        true_image_id=true_image_id,
        label_id=label_id,
        shared_id=shared_id,
        left_value=element_parameter.left_alignment,
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

    return toggle_image_button + label


def create_toggle_image_buttons(elements_parameter: List[DataElement]) -> str:
    """Create Multiple `Toggle Image Button` MeasUI Elements.

    Args:
        elements_parameter (List[DataElement]): List of Toggle Image Button Element \
            Parameters.

    Returns:
        str: MeasUI Toggle Image Button Elements.
    """
    toggle_image_buttons = ""
    top_value = MeasUIElementPosition.TOP_START_VALUE

    for element_parameter in elements_parameter:
        element_parameter.top_alignment = top_value
        top_value += MeasUIElementPosition.TOP_INCREMENTAL_VALUE

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
    top_value = MeasUIElementPosition.TOP_START_VALUE

    for element_parameter in elements_parameter:
        element_parameter.left_alignment = (
            MeasUIElementPosition.LEFT_START_VALUE + MeasUIElementPosition.LEFT_INCREMENTAL_VALUE
        )
        element_parameter.top_alignment = top_value
        top_value += MeasUIElementPosition.TOP_INCREMENTAL_VALUE

        toggle_image_indicators += create_toggle_image_indicator(
            element_parameter=element_parameter
        )

    return toggle_image_indicators
