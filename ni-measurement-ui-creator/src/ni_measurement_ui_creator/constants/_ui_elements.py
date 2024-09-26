"""Measurement UI constants."""

import uuid
from enum import Enum

CLIENT_ID = uuid.uuid4()


class MeasUIElement:
    """Measurement UI Elements."""

    NUMERIC_CONTROL = '<ChannelNumericText AdaptsToType="[bool]True" Channel="[string]{client_id}/Configuration/{name}" Height="[float]{height}" Id="{shared_id}" Label="[UIModel]{element_id}" Left="[float]{left_value}" TabIndex="[int]0" Top="[float]{top_value}" Width="[float]{width}" ValueType="[Type]{value_type}"/>'
    NUMERIC_INDICATOR = '<ChannelNumericText AdaptsToType="[bool]True" Channel="[string]{client_id}/Output/{name}" Height="[float]{height}" Id="{shared_id}" IsReadOnly="[bool]True" Label="[UIModel]{element_id}" Left="[float]{left_value}" TabIndex="[int]2" Top="[float]{top_value}" ValueType="[Type]{value_type}" Width="[float]{width}" />'

    NUMERIC_ARRAY_INPUT = '<ChannelArrayViewer AdaptsToType="[bool]True" ArrayElement="[UIModel]{array_element_id}" Channel="[string]{client_id}/Configuration/{name}" Columns="[int]1" Dimensions="[int]1" Height="[float]120" Id="{shared_id}" IndexVisibility="[Visibility]Collapsed" Label="[UIModel]{label_id}" Left="[float]{left_value}" Orientation="[SMOrientation]Vertical" Rows="[int]{rows}" TabIndex="[int]0" Top="[float]{top_value}" VerticalScrollBarVisibility="[ScrollBarVisibility]Visible" Width="[float]104"><p.DefaultElementValue>0</p.DefaultElementValue><ChannelArrayNumericText Height="[float]{height}" Id="{array_element_id}" ValueFormatter="[string]LV:G5" ValueType="[Type]{value_type}" Width="[float]{width}" /></ChannelArrayViewer>'
    NUMERIC_ARRAY_OUTPUT = '<ChannelArrayViewer AdaptsToType="[bool]True" ArrayElement="[UIModel]{array_element_id}" Channel="[string]{client_id}/Output/{name}" Columns="[int]1" Dimensions="[int]1" Height="[float]120" Id="{shared_id}" IndexVisibility="[Visibility]Collapsed" Label="[UIModel]{label_id}" Left="[float]{left_value}" Orientation="[SMOrientation]Vertical" Rows="[int]{rows}" TabIndex="[int]0" Top="[float]{top_value}" VerticalScrollBarVisibility="[ScrollBarVisibility]Visible" Width="[float]104"><p.DefaultElementValue>0</p.DefaultElementValue><ChannelArrayNumericText Height="[float]{height}" Id="{array_element_id}" IsReadOnly="[bool]True" ValueFormatter="[string]LV:G5" ValueType="[Type]{value_type}" Width="[float]{width}" /></ChannelArrayViewer>'

    BOOLEAN_HORIZONTAL_SLIDER = '<ChannelSwitch BaseName="[string]Switch" Channel="[string]{client_id}/Configuration/{name}" Enabled="[bool]True" FalseContent="[string]Off" Height="[float]{height}" Id="{shared_id}" IsReadOnly="[bool]False" Label="[UIModel]{label_id}" Left="[float]{left_value}" MinHeight="[float]5" MinWidth="[float]5" Orientation="[SMOrientation]Horizontal" Shape="[SwitchShape]Slider" Top="[float]{top_value}" TrueContent="[string]On" Width="[float]{width}" />'
    BOOLEAN_LED = '<ChannelLED BaseName="[string]Round LED" Channel="[string]{client_id}/Output/{name}" ContentVisibility="[Visibility]Collapsed" FalseContent="[string]Off" Height="[float]{height}" Id="{shared_id}" IsReadOnly="[bool]True" Label="[UIModel]{label_id}" Left="[float]{left_value}" MinHeight="[float]5" MinWidth="[float]5" Shape="[LEDShape]Round" Top="[float]{top_value}" TrueContent="[string]On" Width="[float]{width}" />'

    STRING_CONTROL = '<ChannelStringControl AcceptsReturn="[bool]False" BaseName="[string]String" Channel="[string]{client_id}/Configuration/{name}" Enabled="[bool]True" Height="[float]{height}" HorizontalScrollBarVisibility="[ScrollBarVisibility]Hidden" Id="{shared_id}" Label="[UIModel]{label_id}" Left="[float]{left_value}" Top="[float]{top_value}" VerticalScrollBarVisibility="[ScrollBarVisibility]Auto" Width="[float]{width}" />'
    STRING_INDICATOR = '<ChannelStringControl AcceptsReturn="[bool]False" BaseName="[string]String" Channel="[string]{client_id}/Output/{name}" Height="[float]{height}" HorizontalScrollBarVisibility="[ScrollBarVisibility]Hidden" Id="{shared_id}" IsReadOnly="[bool]True" Label="[UIModel]{label_id}" Left="[float]{left_value}" Top="[float]{top_value}" VerticalScrollBarVisibility="[ScrollBarVisibility]Auto" Width="[float]{width}" />'

    STRING_ARRAY_INPUT = '<ChannelArrayViewer ArrayElement="[UIModel]{array_element_id}" BaseName="[string]String Array Input" Channel="[string]{client_id}/Configuration/{name}" Columns="[int]1" Dimensions="[int]1" Height="[float]{height}" Id="{shared_id}" IndexVisibility="[Visibility]Collapsed" IsFixedSize="[bool]False" Label="[UIModel]{label_id}" Left="[float]{left_value}" Orientation="[SMOrientation]Vertical" Rows="[int]{rows}" Top="[float]{top_value}" VerticalScrollBarVisibility="[ScrollBarVisibility]Visible" Width="[float]105"><p.DefaultElementValue>""</p.DefaultElementValue><ChannelArrayStringControl AcceptsReturn="[bool]False" BaseName="[string]String" Height="[float]{height}" HorizontalScrollBarVisibility="[ScrollBarVisibility]Hidden" Id="{array_element_id}" VerticalScrollBarVisibility="[ScrollBarVisibility]Auto" Width="[float]{width}" /></ChannelArrayViewer>'
    STRING_ARRAY_OUTPUT = '<ChannelArrayViewer ArrayElement="[UIModel]{array_element_id}" BaseName="[string]String Array Output" Channel="[string]{client_id}/Output/{name}" Columns="[int]1" Dimensions="[int]1" Height="[float]{height}" Id="{shared_id}" IndexVisibility="[Visibility]Collapsed" IsFixedSize="[bool]False" Label="[UIModel]{label_id}" Left="[float]{left_value}" Orientation="[SMOrientation]Vertical" Rows="[int]{rows}" Top="[float]{top_value}" VerticalScrollBarVisibility="[ScrollBarVisibility]Visible" Width="[float]105"><p.DefaultElementValue>""</p.DefaultElementValue><ChannelArrayStringControl AcceptsReturn="[bool]False" BaseName="[string]String" Height="[float]{height}" HorizontalScrollBarVisibility="[ScrollBarVisibility]Hidden" Id="{array_element_id}" IsReadOnly="[bool]True" VerticalScrollBarVisibility="[ScrollBarVisibility]Auto" Width="[float]{width}" /></ChannelArrayViewer>'

    PIN_SELECTOR = '<ChannelPinSelector AllowUndefinedValues="[bool]True" BaseName="[string]Pin" Channel="[string]{client_id}/Configuration/{name}" DataType="[Type]String" Enabled="[bool]True" Height="[float]{height}" Id="{shared_id}" IsLabelBoundToChannel="[bool]False" Label="[UIModel]{label_id}" Left="[float]{left_value}" SelectedResource="[NI_Core_DataValues_TagRefnum]Pin1" Top="[float]{top_value}" Width="[float]{width}" xmlns="http://www.ni.com/InstrumentFramework/ScreenDocument" />'
    IORESOURCE_ARRAY = '<ChannelPinSelector AllowUndefinedValues="[bool]True" BaseName="[string]Pin" Channel="[string]{client_id}/Configuration/{name}" DataType="[Type]String" Enabled="[bool]True" Height="[float]{height}" Id="{shared_id}" IsLabelBoundToChannel="[bool]False" Label="[UIModel]{label_id}" Left="[float]{left_value}" MultipleSelectionMode="[MultipleSelectionModes]List" SelectedResource="[NI_Core_DataValues_TagRefnum]PinGroup1" Top="[float]{top_value}" Width="[float]{width}" xmlns="http://www.ni.com/InstrumentFramework/ScreenDocument" />'

    LABEL = '<Label Height="[float]16" Id="{id}" LabelOwner="[UIModel]{shared_id}" Left="[float]{left_value}" Text="[string]{input_output_name}" Top="[float]{top_value}" Width="[float]100" xmlns="http://www.ni.com/PanelCommon" />'


class MeasUIElementPosition:
    """Measurement UI Element's Position."""

    LEFT_ALIGNMENT_START_VALUE = 40
    LEFT_ALIGNMENT_INCREMENTAL_VALUE = 200

    TOP_ALIGNMENT_START_VALUE = 40
    TOP_ALIGNMENT_INCREMENTAL_VALUE = 50

    TOP_ALIGNMENT_ADDITIONAL_INCREMENTAL_VALUE = 20

    DEFAULT_LEFT_ALIGNMENT = 100
    DEFAULT_TOP_ALIGNMENT = 100

    DEFAULT_HEIGHT = 25
    DEFAULT_WIDTH = 120

    DEFAULT_ARRAY_ROWS = 3

    BOOLEAN_HORIZONTAL_SLIDER_HEIGHT = 35
    BOOLEAN_HORIZONTAL_SLIDER_WIDTH = 70

    BOOLEAN_LED_HEIGHT = 35
    BOOLEAN_LED_WIDTH = 35

    ARRAY_HEIGHT = 25
    ARRAY_WIDTH = 90


class SupportedDataType:
    """Supported data types in UI creator."""

    DOUBLE = "Double"
    SINGLE = "Single"
    INT32 = "Int32"
    INT64 = "Int64"
    UINT32 = "UInt32"
    UINT64 = "UInt64"
    BOOL = "Boolean"
    STR = "String"
    PIN = "Pin"
    IORESOURCE = "IOResource"
    IORESOURCE_ARR = "IOResourceArray1D"


class DataType(Enum):
    """Supported data types and its corresponding input values."""

    Double = 1
    Single = 2
    Int32 = 5
    Int64 = 3
    UInt32 = 13
    UInt64 = 4
    Boolean = 8
    String = 9


class SpecializedDataType:
    """Special data types supported."""

    PIN = "Pin"
    IORESOURCE = "IOResource"
    IORESOURCE_ARR = "IOResourceArray1D"


class UpdateUI:
    """Update UI file."""

    NAMESPACES = {
        "pf": "http://www.ni.com/PlatformFramework",
        "sf": "http://www.ni.com/InstrumentFramework/ScreenDocument",
        "cf": "http://www.ni.com/ConfigurationBasedSoftware.Core",
        "pc": "http://www.ni.com/PanelCommon",
    }
    SCREEN_TAG = ".//sf:Screen"
    SCREEN_SURFACE_TAG = ".//cf:ScreenSurface"

    NUMERIC_ELEMENTS = [
        "ChannelNumericText",
        "ChannelSlider",
        "ChannelGauge",
        "ChannelMeter",
        "ChannelKnob",
        "ChannelLinearProgressBar",
        "ChannelRadialProgressBar",
        "ChannelTank",
    ]
    BOOLEAN_ELEMENTS = [
        "ChannelLED",
        "ChannelImageButton",
        "ChannelButton",
        "ChannelCheckBox",
        "ChannelSwitch",
    ]
    READ_ONLY_BASED = [
        "ChannelNumericText",
        "ChannelButton",
        "ChannelSwitch",
        "ChannelStringControl",
        "ChannelLED",
        "ChannelImageButton",
    ]
    INTERACTION_MODE_BASED = [
        "ChannelSlider",
        "ChannelKnob",
        "ChannelButton",
        "ChannelSwitch",
        "ChannelGauge",
        "ChannelMeter",
        "ChannelTank",
    ]
    ONLY_INDICATORS = ["ChannelLinearProgressBar", "ChannelRadialProgressBar", "ChannelCheckBox"]
    SPECIAL_ELEMENTS = ["ChannelPinSelector", "ChannelArrayViewer"]

    SUPPORTED_CONTROLS_AND_INDICATORS = (
        READ_ONLY_BASED + INTERACTION_MODE_BASED + ONLY_INDICATORS + SPECIAL_ELEMENTS
    )

    UNSUPPORTED_ELEMENTS = [
        "ChannelRingSelector",
        "ChannelEnumSelector",
        "ChannelPathSelector",
        "HmiGraphPlot",
    ]


class ElementAttrib:
    """Attributes in UI Elements."""

    CLIENT_ID = "ClientId"
    CHANNEL = "Channel"
    LABEL = "Label"
    LABEL_OWNER = "LabelOwner"
    ID = "Id"
    TOP = "Top"
    LEFT = "Left"
    HEIGHT = "Height"
    MIN_HEIGHT = "MinHeight"
    IS_READ_ONLY = "IsReadOnly"
    INTERACTION_MODE = "InteractionMode"


class MeasUIFile:
    """Measurement UI file."""

    ENCODING = "utf-8"
    MEASUREMENT_UI_FILE_EXTENSION = ".measui"


LOGGER = "logger"
TYPE_SPECIFICATION = "ni/type_specialization"
MEASUREMENT_SERVICE_INTERFACE_V1 = "ni.measurementlink.measurement.v1.MeasurementService"
MEASUREMENT_SERVICE_INTERFACE_V2 = "ni.measurementlink.measurement.v2.MeasurementService"
SUPPORTED_UI_ELEMENTS = [
    "Numeric Indicator",
    "Numeric Control",
    "Numeric Array Input",
    "Numeric Array Output",
    "Boolean Horizontal Slider",
    "Boolean Round LED",
    "String Control",
    "String Indicator",
    "String Array Input",
    "String Array Output",
    "Pin",
]
NUMERIC_DATA_TYPE_NAMES = [
    DataType.Int32.name,
    DataType.Int64.name,
    DataType.UInt32.name,
    DataType.UInt64.name,
    DataType.Single.name,
    DataType.Double.name,
]
NUMERIC_DATA_TYPE_VALUES = [
    DataType.Int32.value,
    DataType.Int64.value,
    DataType.UInt32.value,
    DataType.UInt64.value,
    DataType.Single.value,
    DataType.Double.value,
]
