"""Create string elements for building UI."""

from ni_measurement_plugin_ui_creator.models import DataElement, LabelElement
from ni_measurement_plugin_ui_creator.utils.common_elements import create_label, get_unique_id

STRING_ARRAY_INPUT = (
    '<ChannelArrayViewer ArrayElement="[UIModel]{array_element_id}" '
    'BaseName="[string]String Array Input" Channel="[string]{client_id}/Configuration/{name}" '
    'Columns="[int]1" Dimensions="[int]1" Height="[float]{height}" Id="{shared_id}" '
    'IndexVisibility="[Visibility]Collapsed" IsFixedSize="[bool]False" '
    'Label="[UIModel]{label_id}" Left="[float]{left_value}" Orientation="[SMOrientation]Vertical" '
    'Rows="[int]{rows}" Top="[float]{top_value}" '
    'VerticalScrollBarVisibility="[ScrollBarVisibility]Visible" Width="[float]105">'
    '<p.DefaultElementValue>""</p.DefaultElementValue>'
    '<ChannelArrayStringControl AcceptsReturn="[bool]False" BaseName="[string]String" '
    'Height="[float]{height}" HorizontalScrollBarVisibility="[ScrollBarVisibility]Hidden" '
    'Id="{array_element_id}" VerticalScrollBarVisibility="[ScrollBarVisibility]Auto" '
    'Width="[float]{width}" /></ChannelArrayViewer>'
)
STRING_ARRAY_OUTPUT = (
    '<ChannelArrayViewer ArrayElement="[UIModel]{array_element_id}" '
    'BaseName="[string]String Array Output" Channel="[string]{client_id}/Output/{name}" '
    'Columns="[int]1" Dimensions="[int]1" Height="[float]{height}" Id="{shared_id}" '
    'IndexVisibility="[Visibility]Collapsed" IsFixedSize="[bool]False" Label="[UIModel]{label_id}" '
    'Left="[float]{left_value}" Orientation="[SMOrientation]Vertical" Rows="[int]{rows}" '
    'Top="[float]{top_value}" VerticalScrollBarVisibility="[ScrollBarVisibility]Visible" '
    'Width="[float]105"><p.DefaultElementValue>""</p.DefaultElementValue>'
    '<ChannelArrayStringControl AcceptsReturn="[bool]False" BaseName="[string]String" '
    'Height="[float]{height}" HorizontalScrollBarVisibility="[ScrollBarVisibility]Hidden" '
    'Id="{array_element_id}" IsReadOnly="[bool]True" '
    'VerticalScrollBarVisibility="[ScrollBarVisibility]Auto" '
    'Width="[float]{width}" /></ChannelArrayViewer>'
)
STRING_CONTROL = (
    '<ChannelStringControl AcceptsReturn="[bool]False" BaseName="[string]String" '
    'Channel="[string]{client_id}/Configuration/{name}" Enabled="[bool]True" '
    'Height="[float]{height}" HorizontalScrollBarVisibility="[ScrollBarVisibility]Hidden" '
    'Id="{shared_id}" Label="[UIModel]{label_id}" Left="[float]{left_value}" '
    'Top="[float]{top_value}" VerticalScrollBarVisibility="[ScrollBarVisibility]Auto" '
    'Width="[float]{width}" />'
)
STRING_INDICATOR = (
    '<ChannelStringControl AcceptsReturn="[bool]False" BaseName="[string]String" '
    'Channel="[string]{client_id}/Output/{name}" Height="[float]{height}" '
    'HorizontalScrollBarVisibility="[ScrollBarVisibility]Hidden" Id="{shared_id}" '
    'IsReadOnly="[bool]True" Label="[UIModel]{label_id}" Left="[float]{left_value}" '
    'Top="[float]{top_value}" VerticalScrollBarVisibility="[ScrollBarVisibility]Auto" '
    'Width="[float]{width}" />'
)


def create_string_control(element_parameter: DataElement) -> str:
    """Create `String Control` Measurement plug-in UI Element.

    Args:
        element_parameter: String Control Element Parameters.

    Returns:
        String Control Element.
    """
    label_id = get_unique_id()
    shared_id = get_unique_id()

    string_control = STRING_CONTROL.format(
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
    """Create `String Indicator` Measurement plug-in UI Element.

    Args:
        element_parameter: String Indicator Element Parameters.

    Returns:
        String Indicator Element.
    """
    label_id = get_unique_id()
    shared_id = get_unique_id()

    string_indicator = STRING_INDICATOR.format(
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


def create_string_array_control(element_parameter: DataElement) -> str:
    """Create `String Array Input` Measurement plug-in UI Element.

    Args:
        element_parameter: String Array Input Element Parameters.

    Returns:
        String Array Input Element.
    """
    array_element_id = get_unique_id()
    shared_id = get_unique_id()
    label_id = get_unique_id()

    string_array = STRING_ARRAY_INPUT.format(
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
    """Create `String Array Output` Measurement plug-in UI Element.

    Args:
        element_parameter: String Array Output Element Parameters.

    Returns:
        Sting Array Output Element.
    """
    array_element_id = get_unique_id()
    shared_id = get_unique_id()
    label_id = get_unique_id()

    string_array = STRING_ARRAY_OUTPUT.format(
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
