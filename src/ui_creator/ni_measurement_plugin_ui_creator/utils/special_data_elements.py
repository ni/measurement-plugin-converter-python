"""Create special elements for building UI."""

from ni_measurement_plugin_ui_creator.models import DataElement, LabelElement
from ni_measurement_plugin_ui_creator.utils.common_elements import (
    create_label,
    get_unique_id,
)

IORESOURCE_ARRAY = (
    '<ChannelPinSelector AllowUndefinedValues="[bool]True" BaseName="[string]Pin" '
    'Channel="[string]{client_id}/Configuration/{name}" DataType="[Type]String" '
    'Enabled="[bool]True" Height="[float]{height}" Id="{shared_id}" '
    'IsLabelBoundToChannel="[bool]False" Label="[UIModel]{label_id}" Left="[float]{left_value}" '
    'MultipleSelectionMode="[MultipleSelectionModes]List" '
    'SelectedResource="[NI_Core_DataValues_TagRefnum]PinGroup1" Top="[float]{top_value}" '
    'Width="[float]{width}" xmlns="http://www.ni.com/InstrumentFramework/ScreenDocument" />'
)
PIN_SELECTOR = (
    '<ChannelPinSelector AllowUndefinedValues="[bool]True" BaseName="[string]Pin" '
    'Channel="[string]{client_id}/Configuration/{name}" DataType="[Type]String" '
    'Enabled="[bool]True" Height="[float]{height}" Id="{shared_id}" '
    'IsLabelBoundToChannel="[bool]False" Label="[UIModel]{label_id}" '
    'Left="[float]{left_value}" SelectedResource="[NI_Core_DataValues_TagRefnum]Pin1" '
    'Top="[float]{top_value}" Width="[float]{width}" '
    'xmlns="http://www.ni.com/InstrumentFramework/ScreenDocument" />'
)


def create_pin_control(element_parameter: DataElement) -> str:
    """Create `Pin Control` Measurement plug-in UI Element.

    Args:
        element_parameter (DataElement): Pin Control Element Parameters.

    Returns:
        str: Measurement plug-in UI Pin Control Element.
    """
    label_id = get_unique_id()
    shared_id = get_unique_id()

    pin_control = PIN_SELECTOR.format(
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

    return pin_control + label


def create_ioresource_array_control(element_parameter: DataElement) -> str:
    """Create `Pin Control` Measurement plug-in UI Element as IOResourceArray1D.

    Args:
        element_parameter (DataElement): Pin Control Element Parameters.

    Returns:
        str: Measurement plug-in UI Pin Control Element as IOResourceArray1D.
    """
    label_id = get_unique_id()
    shared_id = get_unique_id()

    ioresource_control = IORESOURCE_ARRAY.format(
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

    return ioresource_control + label
