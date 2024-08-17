"""Measurement UI constants."""

import uuid
from enum import Enum

CLIENT_ID = uuid.uuid4()


class MeasUIElement:
    """Measurement UI Elements."""

    SCREEN_SURFACE = '<ScreenSurface BackgroundColor="[SMSolidColorBrush]#00ffffff" Height="[float]1000" Id="c47bc3494c0244bab74b59853ae5087f" Left="[float]0" PanelSizeMode="Fixed" Top="[float]0" Width="[float]520" xmlns="http://www.ni.com/ConfigurationBasedSoftware.Core">'
    HEADERS = (
        f'<?xml version="1.0" encoding="utf-8"?> <SourceFile Checksum="81CD3EE5B0FDFEA2478685EE480764FB6E16C8E3B5DA74AF2CF40ED16E62CA381B9754536688461BA95599295C52450BD97BFEC7B16664C415491E047647AB88" Timestamp="1DAAA818B5383B3" xmlns="http://www.ni.com/PlatformFramework"> <SourceModelFeatureSet><ParsableNamespace AssemblyFileVersion="9.12.0.49994" FeatureSetName="Configuration Based Software Core" Name="http://www.ni.com/ConfigurationBasedSoftware.Core" OldestCompatibleVersion="6.3.0.49152" Version="9.8.1.49152" /><ParsableNamespace AssemblyFileVersion="9.12.0.49994" FeatureSetName="LabVIEW Controls" Name="http://www.ni.com/Controls.LabVIEW.Design" OldestCompatibleVersion="8.1.0.49152" Version="8.1.0.49152" /><ParsableNamespace AssemblyFileVersion="24.3.0.49994" FeatureSetName="InstrumentStudio Measurement UI" Name="http://www.ni.com/InstrumentFramework/ScreenDocument" OldestCompatibleVersion="22.1.0.1" Version="22.1.0.1" /><ParsableNamespace AssemblyFileVersion="9.12.0.49994" FeatureSetName="Editor" Name="http://www.ni.com/PanelCommon" OldestCompatibleVersion="6.1.0.0" Version="6.1.0.49152" /><ParsableNamespace AssemblyFileVersion="9.12.0.49994" FeatureSetName="Editor" Name="http://www.ni.com/PlatformFramework" OldestCompatibleVersion="8.1.0.49152" Version="8.1.0.49152" /><ApplicationVersionInfo Build="24.3.0.49994" Name="MeasurementLink UI Editor" Version="24.3.0.49994" /></SourceModelFeatureSet><Screen ClientId="{CLIENT_ID}" DisplayName="Sample Measurement (Py)" Id="20c496a981bb4f73bea9d243756baab5" ServiceClass="ni.examples.SampleMeasurement_Python" xmlns="http://www.ni.com/InstrumentFramework/ScreenDocument">'
        + SCREEN_SURFACE
    )
    FOOTER = "</ScreenSurface></Screen></SourceFile>"

    NUMERIC_CONTROL = '<ChannelNumericText AdaptsToType="[bool]True" Channel="[string]{client_id}/Configuration/{name}" Height="[float]{height}" Id="{element_id}" Label="[UIModel]{shared_id}" Left="[float]{left_value}" TabIndex="[int]0" Top="[float]{top_value}" Width="[float]{width}" ValueType="[Type]{value_type}"/>'
    NUMERIC_INDICATOR = '<ChannelNumericText AdaptsToType="[bool]True" Channel="[string]{client_id}/Output/{name}" Height="[float]{height}" Id="{element_id}" IsReadOnly="[bool]True" Label="[UIModel]{shared_id}" Left="[float]{left_value}" TabIndex="[int]2" Top="[float]{top_value}" ValueType="[Type]{value_type}" Width="[float]{width}" />'

    NUMERIC_ARRAY_INPUT = '<ChannelArrayViewer AdaptsToType="[bool]True" ArrayElement="[UIModel]{array_element_id}" Channel="[string]{client_id}/Configuration/{name}" Columns="[int]1" Dimensions="[int]1" Height="[float]{height}" Id="{shared_id}" IndexVisibility="[Visibility]Collapsed" Label="[UIModel]{label_id}" Left="[float]{left_value}" Orientation="[SMOrientation]Vertical" Rows="[int]{rows}" TabIndex="[int]0" Top="[float]{top_value}" VerticalScrollBarVisibility="[ScrollBarVisibility]Visible" Width="[float]{width}"><p.DefaultElementValue>0</p.DefaultElementValue><ChannelArrayNumericText Height="[float]24" Id="{array_element_id}" ValueFormatter="[string]LV:G5" ValueType="[Type]{value_type}" Width="[float]90" /></ChannelArrayViewer>'
    NUMERIC_ARRAY_OUTPUT = '<ChannelArrayViewer AdaptsToType="[bool]True" ArrayElement="[UIModel]{array_element_id}" Channel="[string]{client_id}/Output/{name}" Columns="[int]1" Dimensions="[int]1" Height="[float]{height}" Id="{shared_id}" IndexVisibility="[Visibility]Collapsed" Label="[UIModel]{label_id}" Left="[float]{left_value}" Orientation="[SMOrientation]Vertical" Rows="[int]{rows}" TabIndex="[int]0" Top="[float]{top_value}" VerticalScrollBarVisibility="[ScrollBarVisibility]Visible" Width="[float]{width}"><p.DefaultElementValue>0</p.DefaultElementValue><ChannelArrayNumericText Height="[float]24" Id="{array_element_id}" IsReadOnly="[bool]True" ValueFormatter="[string]LV:G5" ValueType="[Type]{value_type}" Width="[float]90" /></ChannelArrayViewer>'

    TOGGLE_IMAGE_BUTTON = '<ChannelImageButton BaseName="[string]Toggle Images Button" Channel="[string]{client_id}/Configuration/{name}" FalseImage="[UIModel]{false_image_id}" Height="[float]{height}" Id="{shared_id}" IncludeInCapture="[bool]False" IsMomentary="[bool]False" Label="[UIModel]{label_id}" Left="[float]{left_value}" Top="[float]{top_value}" TrueImage="[UIModel]{true_image_id}" Width="[float]{width}"> <Image BaseName="[string]Image" Id="{true_image_id}" Left="[float]0" Source="[string]pack://application:,,,/NationalInstruments.Hmi.Core;component/Resources/ImageButtonTrue_40x40.xml" Stretch="[SMStretch]Fill" Top="[float]0" xmlns="http://www.ni.com/PlatformFramework" /> <Image BaseName="[string]Image" Id="{false_image_id}" Left="[float]0" Source="[string]pack://application:,,,/NationalInstruments.Hmi.Core;component/Resources/ImageButtonFalse_40x40.xml" Stretch="[SMStretch]Fill" Top="[float]0" xmlns="http://www.ni.com/PlatformFramework"/></ChannelImageButton>'
    TOGGLE_IMAGE_INDICATOR = '<ChannelImageButton BaseName="[string]Toggle Images Indicator" Channel="[string]{client_id}/Output/{name}" FalseImage="[UIModel]{false_image_id}" Height="[float]{height}" Id="{shared_id}" IncludeInCapture="[bool]False" IsMomentary="[bool]False" IsReadOnly="[bool]True" Label="[UIModel]{label_id}" Left="[float]{left_value}" Top="[float]{top_value}" TrueImage="[UIModel]{true_image_id}" Width="[float]{width}"><Image BaseName="[string]Image" Id="{true_image_id}" Left="[float]0" Source="[string]pack://application:,,,/NationalInstruments.Hmi.Core;component/Resources/ImageButtonTrue_40x40.xml" Stretch="[SMStretch]Fill" Top="[float]0" xmlns="http://www.ni.com/PlatformFramework" /><Image BaseName="[string]Image" Id="{false_image_id}" Left="[float]0" Source="[string]pack://application:,,,/NationalInstruments.Hmi.Core;component/Resources/ImageButtonFalse_40x40.xml" Stretch="[SMStretch]Fill" Top="[float]0" xmlns="http://www.ni.com/PlatformFramework"/></ChannelImageButton>'

    STRING_CONTROL = '<ChannelStringControl AcceptsReturn="[bool]False" BaseName="[string]String" Channel="[string]{client_id}/Configuration/{name}" Enabled="[bool]True" Height="[float]{height}" HorizontalScrollBarVisibility="[ScrollBarVisibility]Hidden" Id="{shared_id}" Label="[UIModel]{label_id}" Left="[float]{left_value}" Top="[float]{top_value}" VerticalScrollBarVisibility="[ScrollBarVisibility]Auto" Width="[float]{width}" />'
    STRING_INDICATOR = '<ChannelStringControl AcceptsReturn="[bool]False" BaseName="[string]String" Channel="[string]{client_id}/Output/{name}" Height="[float]{height}" HorizontalScrollBarVisibility="[ScrollBarVisibility]Hidden" Id="{shared_id}" IsReadOnly="[bool]True" Label="[UIModel]{label_id}" Left="[float]{left_value}" Top="[float]{top_value}" VerticalScrollBarVisibility="[ScrollBarVisibility]Auto" Width="[float]{width}" />'

    PIN_SELECTOR = '<ChannelPinSelector AllowUndefinedValues="[bool]True" BaseName="[string]Pin" Channel="[string]{client_id}/Configuration/{name}" DataType="[Type]String" Enabled="[bool]True" Height="[float]{height}" Id="{shared_id}" IsLabelBoundToChannel="[bool]False" Label="[UIModel]{label_id}" Left="[float]{left_value}" SelectedResource="[NI_Core_DataValues_TagRefnum]Pin1" Top="[float]{top_value}" Width="[float]{width}" xmlns="http://www.ni.com/InstrumentFramework/ScreenDocument" />'
    IORESOURCE_ARRAY = '<ChannelPinSelector AllowUndefinedValues="[bool]True" BaseName="[string]Pin" Channel="[string]{client_id}/Configuration/{name}" DataType="[Type]String" Enabled="[bool]True" Height="[float]{height}" Id="{shared_id}" IsLabelBoundToChannel="[bool]False" Label="[UIModel]{label_id}" Left="[float]{left_value}" MultipleSelectionMode="[MultipleSelectionModes]List" SelectedResource="[NI_Core_DataValues_TagRefnum]PinGroup1" Top="[float]{top_value}" Width="[float]{width}" xmlns="http://www.ni.com/InstrumentFramework/ScreenDocument" />'
    LABEL = '<Label Height="[float]{height}" Id="{id}" LabelOwner="[UIModel]{shared_id}" Left="[float]{left_value}" Text="[string]{input_output_name}" Top="[float]{top_value}" Width="[float]{width}" xmlns="http://www.ni.com/PanelCommon" />'


class MeasUIElementPosition:
    """Measurement UI Element's Position."""

    LEFT_ALIGNMENT_START_VALUE = 40
    LEFT_ALIGNMENT_INCREMENTAL_VALUE = 200

    TOP_ALIGNMENT_START_VALUE = 40
    TOP_ALIGNMENT_INCREMENTAL_VALUE = 50

    TOP_ALIGNMENT_ADDITIONAL_INCREMENTAL_VALUE = 30

    BOOLEAN_HEIGHT = 50
    BOOLEAN_WIDTH = 50


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


TYPE_SPECIFICATION = "ni/type_specialization"
MEASUREMENT_SERVICE_INTERFACE_V1 = "ni.measurementlink.measurement.v1.MeasurementService"
MEASUREMENT_SERVICE_INTERFACE_V2 = "ni.measurementlink.measurement.v2.MeasurementService"
SUPPORTED_UI_ELEMENTS = [
    "Numeric Indicator",
    "Numeric Control",
    "Numeric Array Input",
    "Numeric Array Output",
    "Toggle Image Button",
    "Toggle Image Indicator",
    "String Control",
    "String Indicator",
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

ENCODING = "utf-8"
