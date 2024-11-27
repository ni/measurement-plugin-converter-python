"""Measurement plug-in UI constants."""

import uuid
from enum import Enum

CLIENT_ID = uuid.uuid4()


class DataType(Enum):
    """Supported data types and its corresponding values from ni_measurement_plugin_sdk_service."""

    Boolean = 8
    Double = 1
    Int32 = 5
    Int64 = 3
    Single = 2
    String = 9
    UInt32 = 13
    UInt64 = 4


class ElementAttrib:
    """Attributes in UI Elements."""

    CHANNEL = "Channel"
    CLIENT_ID = "ClientId"
    HEIGHT = "Height"
    ID = "Id"
    INTERACTION_MODE = "InteractionMode"
    IS_READ_ONLY = "IsReadOnly"
    LABEL = "Label"
    LABEL_OWNER = "LabelOwner"
    LEFT = "Left"
    MIN_HEIGHT = "MinHeight"
    TOP = "Top"


class MeasUIElementPosition:
    """Measurement plug-in UI's element position."""

    ARRAY_HEIGHT = 25
    ARRAY_WIDTH = 90
    BOOLEAN_HORIZONTAL_SLIDER_HEIGHT = 35
    BOOLEAN_HORIZONTAL_SLIDER_WIDTH = 70
    BOOLEAN_LED_HEIGHT = 35
    BOOLEAN_LED_WIDTH = 35
    DEFAULT_ARRAY_ROWS = 3
    DEFAULT_HEIGHT = 25
    DEFAULT_LEFT_ALIGNMENT = 100
    DEFAULT_TOP_ALIGNMENT = 100
    DEFAULT_WIDTH = 120
    INCREASE_FACTOR = 3.5
    LEFT_ALIGNMENT_INCREMENTAL_VALUE = 200
    LEFT_ALIGNMENT_START_VALUE = 40
    MIN_HEIGHT = "MinHeight"
    REDUCE_FACTOR = 0.5
    TOP_ALIGNMENT_ADDITIONAL_INCREMENTAL_VALUE = 20
    TOP_ALIGNMENT_INCREMENTAL_VALUE = 50
    TOP_ALIGNMENT_START_VALUE = 40


class MeasUIFile:
    """Measurement UI file."""

    ENCODING = "utf-8"
    MEASUREMENT_UI_FILE_EXTENSION = ".measui"


class SpecializedDataType:
    """Special data types supported."""

    IORESOURCE = "IOResource"
    IORESOURCE_ARR = "IOResourceArray1D"
    PIN = "Pin"


class SupportedDataType:
    """Supported data types in UI creator."""

    BOOL = "Boolean"
    DOUBLE = "Double"
    INT32 = "Int32"
    INT64 = "Int64"
    IORESOURCE = "IOResource"
    IORESOURCE_ARR = "IOResourceArray1D"
    PIN = "Pin"
    SINGLE = "Single"
    STR = "String"
    UINT32 = "UInt32"
    UINT64 = "UInt64"


class UpdateUI:
    """Update UI file."""

    ARRAY_CONTAINER_ELEMENT = "ChannelArrayViewer"
    BOOLEAN_ELEMENTS = [
        "ChannelLED",
        "ChannelImageButton",
        "ChannelButton",
        "ChannelCheckBox",
        "ChannelSwitch",
    ]
    BOOLEAN_HORIZONTAL_SLIDER = "ChannelSlider"
    CLIENT_ID = "ClientId"
    INCREASE_FACTOR = 3.5
    INTERACTION_MODE_BASED = [
        "ChannelSlider",
        "ChannelKnob",
        "ChannelButton",
        "ChannelSwitch",
        "ChannelGauge",
        "ChannelMeter",
        "ChannelTank",
    ]
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
    PIN_ELEMENT = "ChannelPinSelector"
    RING_AND_DEFAULT_ELEMENT = ["p.DefaultElementValue", "RingSelectorInfo"]
    SCREEN_SURFACE_TAG = ".//cf:ScreenSurface"
    SCREEN_TAG = ".//sf:Screen"
    STRING_ARRAY = "ChannelArrayStringControl"
    SPECIAL_ELEMENTS = ["ChannelPinSelector", "ChannelArrayViewer"]
    SUPPORTED_CONTROLS_AND_INDICATORS = (
        BOOLEAN_ELEMENTS + NUMERIC_ELEMENTS + INTERACTION_MODE_BASED + SPECIAL_ELEMENTS
    )
    UNSUPPORTED_ELEMENTS = [
        "ChannelRingSelector",
        "ChannelEnumSelector",
        "ChannelPathSelector",
        "HmiGraphPlot",
    ]


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
