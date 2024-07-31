"""Create common UI elements for building UI."""

import uuid

from ni_measurement_ui_creator.constants._ui_elements import MeasUIElement
from ni_measurement_ui_creator.models._ui_elements import LabelElement


def get_unique_id() -> str:
    """Return unique alphanumeric id after removing hyphens.

    Returns:
        str: Alphanumeric ID.
    """
    id = str(uuid.uuid4()).replace("-", "")
    return id


def create_label(element_parameter: LabelElement) -> str:
    """Create `Label` MeasUI Element.

    Args:
        element_parameter (LabelElement): Label Element Parameters.

    Returns:
        str: MeasUI Label Element.
    """
    label = MeasUIElement.LABEL.format(
        id=element_parameter.id,
        shared_id=element_parameter.shared_id,
        input_output_name=element_parameter.name,
        left_value=element_parameter.left_value,
        top_value=element_parameter.top_value,
    )

    return label
