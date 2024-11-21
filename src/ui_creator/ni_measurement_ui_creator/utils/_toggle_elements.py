"""Create toggle elements for building UI."""

from typing import List

from ni_measurement_ui_creator.constants import MeasUIElement, MeasUIElementPosition
from ni_measurement_ui_creator.models import DataElement, LabelElement
from ni_measurement_ui_creator.utils._common_elements import create_label, get_unique_id


def create_horizontal_slider(element_parameter: DataElement) -> str:
    """Create `Horizontal Slider` MeasUI Element.

    Args:
        element_parameter (DataElement): Horizontal Slider Element Parameters.

    Returns:
        str: MeasUI Horizontal Slider Element.
    """
    shared_id = get_unique_id()
    label_id = get_unique_id()

    boolean_horizontal_slider = MeasUIElement.BOOLEAN_HORIZONTAL_SLIDER.format(
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

    return boolean_horizontal_slider + label


def create_boolean_led(element_parameter: DataElement) -> str:
    """Create `Round LED` MeasUI Element.

    Args:
        element_parameter (DataElement): Round LED Element Parameters.

    Returns:
        str: MeasUI Round LED Element.
    """
    shared_id = get_unique_id()
    label_id = get_unique_id()

    boolean_led = MeasUIElement.BOOLEAN_LED.format(
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

    return boolean_led + label


def create_horizontal_sliders(elements_parameter: List[DataElement]) -> str:
    """Create Multiple `Hortizontal Slider` MeasUI Elements.

    Args:
        elements_parameter (List[DataElement]): List of Horizontal Slider Element Parameters.

    Returns:
        str: MeasUI Horizontal Slider Elements.
    """
    boolean_horizontal_sliders = ""
    top_alignment = MeasUIElementPosition.TOP_ALIGNMENT_START_VALUE

    for element_parameter in elements_parameter:
        element_parameter.top_alignment = top_alignment
        top_alignment += MeasUIElementPosition.TOP_ALIGNMENT_INCREMENTAL_VALUE

        boolean_horizontal_sliders += create_horizontal_slider(element_parameter=element_parameter)

    return boolean_horizontal_sliders


def create_boolean_leds(elements_parameter: List[DataElement]) -> str:
    """Create Multiple `Round LED` MeasUI Elements.

    Args:
        elements_parameter (List[DataElement]): List of Round LED Element Parameters.

    Returns:
        str: MeasUI Round LED Elements.
    """
    boolean_leds = ""
    top_alignment = MeasUIElementPosition.TOP_ALIGNMENT_START_VALUE

    for element_parameter in elements_parameter:
        element_parameter.left_alignment = (
            MeasUIElementPosition.LEFT_ALIGNMENT_START_VALUE
            + MeasUIElementPosition.LEFT_ALIGNMENT_INCREMENTAL_VALUE
        )
        element_parameter.top_alignment = top_alignment
        top_alignment += MeasUIElementPosition.TOP_ALIGNMENT_INCREMENTAL_VALUE

        boolean_leds += create_boolean_led(element_parameter=element_parameter)

    return boolean_leds
