"""Create special elements for building UI."""

from ni_measurement_ui_creator.constants import (
    MeasUIElement,
)
from ni_measurement_ui_creator.models import DataElement, LabelElement
from ni_measurement_ui_creator.utils._common_elements import create_label, get_unique_id


def create_pin_control(element_parameter: DataElement) -> str:
    """Create `Pin Control` MeasUI Element.

    Args:
        element_parameter (DataElement): Pin Control Element Parameters.

    Returns:
        str: MeasUI Pin Control Element.
    """
    label_id = get_unique_id()
    shared_id = get_unique_id()

    string_control = MeasUIElement.PIN_SELECTOR.format(
        client_id=element_parameter.client_id,
        name=element_parameter.name,
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
            left_alignment=element_parameter.left_alignment,
            top_alignment=element_parameter.top_alignment,
        )
    )

    return string_control + label


def create_ioresource_control(element_parameter: DataElement) -> str:
    """Create `Pin Control` MeasUI Element as IOResource.

    Args:
        element_parameter (DataElement): Pin Control Element Parameters.

    Returns:
        str: MeasUI Pin Control Element as IOResource.
    """
    label_id = get_unique_id()
    shared_id = get_unique_id()

    string_control = MeasUIElement.RESOURCE_IO.format(
        client_id=element_parameter.client_id,
        name=element_parameter.name,
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
            left_alignment=element_parameter.left_alignment,
            top_alignment=element_parameter.top_alignment,
        )
    )

    return string_control + label
