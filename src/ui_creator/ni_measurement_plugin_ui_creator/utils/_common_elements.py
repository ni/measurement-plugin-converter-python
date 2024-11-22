"""Create common UI elements for building UI."""

import uuid

from ni_measurement_plugin_ui_creator.models import LabelElement


LABEL = '<Label Height="[float]16" Id="{id}" LabelOwner="[UIModel]{shared_id}" Left="[float]{left_value}" Text="[string]{input_output_name}" Top="[float]{top_value}" Width="[float]100" xmlns="http://www.ni.com/PanelCommon" />'


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
    label = LABEL.format(
        id=element_parameter.id,
        shared_id=element_parameter.shared_id,
        input_output_name=element_parameter.name,
        left_value=element_parameter.left_alignment,
        top_value=element_parameter.top_alignment,
    )

    return label
