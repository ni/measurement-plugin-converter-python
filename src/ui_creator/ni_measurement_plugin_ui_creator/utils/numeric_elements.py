"""Create numeric elements for building UI."""

from ni_measurement_plugin_ui_creator.models import DataElement, LabelElement
from ni_measurement_plugin_ui_creator.utils.common_elements import create_label, get_unique_id

NUMERIC_ARRAY_INPUT = (
    '<ChannelArrayViewer AdaptsToType="[bool]True" '
    'ArrayElement="[UIModel]{array_element_id}" Channel="[string]{client_id}/Configuration/{name}" '
    'Columns="[int]1" Dimensions="[int]1" Height="[float]120" Id="{shared_id}" '
    'IndexVisibility="[Visibility]Collapsed" Label="[UIModel]{label_id}" Left="[float]{left_value}" '
    'Orientation="[SMOrientation]Vertical" Rows="[int]{rows}" TabIndex="[int]0" '
    'Top="[float]{top_value}" VerticalScrollBarVisibility="[ScrollBarVisibility]Visible" '
    'Width="[float]104"><p.DefaultElementValue>0</p.DefaultElementValue>'
    '<ChannelArrayNumericText Height="[float]{height}" Id="{array_element_id}" '
    'ValueFormatter="[string]LV:G5" ValueType="[Type]{value_type}" '
    'Width="[float]{width}" /></ChannelArrayViewer>'
)
NUMERIC_ARRAY_OUTPUT = (
    '<ChannelArrayViewer AdaptsToType="[bool]True" '
    'ArrayElement="[UIModel]{array_element_id}" Channel="[string]{client_id}/Output/{name}" '
    'Columns="[int]1" Dimensions="[int]1" Height="[float]120" Id="{shared_id}" '
    'IndexVisibility="[Visibility]Collapsed" Label="[UIModel]{label_id}" '
    'Left="[float]{left_value}" Orientation="[SMOrientation]Vertical" Rows="[int]{rows}" '
    'TabIndex="[int]0" Top="[float]{top_value}" '
    'VerticalScrollBarVisibility="[ScrollBarVisibility]Visible" '
    'Width="[float]104"><p.DefaultElementValue>0</p.DefaultElementValue>'
    '<ChannelArrayNumericText Height="[float]{height}" Id="{array_element_id}" '
    'IsReadOnly="[bool]True" ValueFormatter="[string]LV:G5" ValueType="[Type]{value_type}" '
    'Width="[float]{width}" /></ChannelArrayViewer>'
)
NUMERIC_CONTROL = (
    '<ChannelNumericText AdaptsToType="[bool]True" '
    'Channel="[string]{client_id}/Configuration/{name}" Height="[float]{height}" '
    'Id="{shared_id}" Label="[UIModel]{element_id}" Left="[float]{left_value}" '
    'TabIndex="[int]0" Top="[float]{top_value}" Width="[float]{width}" '
    'ValueType="[Type]{value_type}"/>'
)
NUMERIC_INDICATOR = (
    '<ChannelNumericText AdaptsToType="[bool]True" '
    'Channel="[string]{client_id}/Output/{name}" Height="[float]{height}" '
    'Id="{shared_id}" IsReadOnly="[bool]True" Label="[UIModel]{element_id}" '
    'Left="[float]{left_value}" TabIndex="[int]2" Top="[float]{top_value}" '
    'ValueType="[Type]{value_type}" Width="[float]{width}" />'
)


def create_numeric_control(element_parameter: DataElement) -> str:
    """Create `Numeric Control` Measurement plug-in UI Element .

    Args:
        element_parameter (DataElement): Numeric Control Element Parameters.

    Returns:
        str: Numeric Control Element.
    """
    element_id = get_unique_id()
    shared_id = get_unique_id()

    numeric_control = NUMERIC_CONTROL.format(
        client_id=element_parameter.client_id,
        element_id=element_id,
        shared_id=shared_id,
        name=element_parameter.name,
        left_value=element_parameter.left_alignment,
        top_value=element_parameter.top_alignment,
        height=element_parameter.height,
        width=element_parameter.width,
        value_type=element_parameter.value_type,
    )

    label = create_label(
        element_parameter=LabelElement(
            id=element_id,
            shared_id=shared_id,
            name=element_parameter.name,
            left_alignment=element_parameter.left_alignment,
            top_alignment=element_parameter.top_alignment,
        )
    )

    return numeric_control + label


def create_numeric_indicator(element_parameter: DataElement) -> str:
    """Create `Numeric Indicator` measurement plug-in UI element.

    Args:
        element_parameter (DataElement): Numeric Indicator Element Parameters.

    Returns:
        str: Numeric Indicator Element.
    """
    element_id = get_unique_id()
    shared_id = get_unique_id()

    numeric_indicator = NUMERIC_INDICATOR.format(
        client_id=element_parameter.client_id,
        element_id=element_id,
        shared_id=shared_id,
        name=element_parameter.name,
        left_value=element_parameter.left_alignment,
        top_value=element_parameter.top_alignment,
        height=element_parameter.height,
        width=element_parameter.width,
        value_type=element_parameter.value_type,
    )

    label = create_label(
        element_parameter=LabelElement(
            id=element_id,
            shared_id=shared_id,
            name=element_parameter.name,
            left_alignment=element_parameter.left_alignment,
            top_alignment=element_parameter.top_alignment,
        )
    )

    return numeric_indicator + label


def create_numeric_array_control(element_parameter: DataElement) -> str:
    """Create `Numeric Array Input` Measurement plug-in UI Element.

    Args:
        element_parameter (DataElement): Numeric Array Input Element Parameters.

    Returns:
        str: Numeric Array Input Element.
    """
    array_element_id = get_unique_id()
    shared_id = get_unique_id()
    label_id = get_unique_id()

    numeric_array = NUMERIC_ARRAY_INPUT.format(
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

    return numeric_array + label


def create_numeric_array_indicator(element_parameter: DataElement) -> str:
    """Create `Numeric Array Output` Measurement plug-in UI Element.

    Args:
        element_parameter (DataElement): Numeric Array Output Element Parameters.

    Returns:
        str: Numeric Array Output Element.
    """
    array_element_id = get_unique_id()
    shared_id = get_unique_id()
    label_id = get_unique_id()

    numeric_array = NUMERIC_ARRAY_OUTPUT.format(
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

    return numeric_array + label
