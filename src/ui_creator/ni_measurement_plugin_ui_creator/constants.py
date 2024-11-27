"""Measurement plug-in UI constants."""

import uuid
from enum import Enum

CLIENT_ID = uuid.uuid4()


class MeasUIElementPosition:
    """Measurement plug-in UI's element position."""

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

    INCREASE_FACTOR = 3.5
    REDUCE_FACTOR = 0.5


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

    ARRAY_ELEMENT = "ChannelArrayViewer"
    PIN_ELEMENT = "ChannelPinSelector"
    RING_AND_DEFAULT_ELEMENT = ["p.DefaultElementValue", "RingSelectorInfo"]
    STRING_ARRAY = "ChannelArrayStringControl"
    NUMERIC_ARRAY = "ChannelArrayNumericText"

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
NUMERIC_DATA_TYPE_VALUES = [
    DataType.Int32.value,
    DataType.Int64.value,
    DataType.UInt32.value,
    DataType.UInt64.value,
    DataType.Single.value,
    DataType.Double.value,
]
