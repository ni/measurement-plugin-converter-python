"""Creation of .measui file for the converted measurement."""

from pathlib import Path
from typing import List, Union

import ni_measurement_plugin_sdk_service as nims
from ni_measurement_plugin_ui_creator.constants import (
    CLIENT_ID,
    DataType,
    MeasUIElementPosition,
    SpecializedDataType,
)
from ni_measurement_plugin_ui_creator.models import DataElement
from ni_measurement_plugin_ui_creator.utils.create_measui import write_measui
from ni_measurement_plugin_ui_creator.utils.helpers import (
    create_control_elements,
    create_indicator_elements,
)

from ni_measurement_plugin_converter._models import (
    InputInfo,
    OutputInfo,
    PinInfo,
    RelayInfo,
)

_REDUCTION_IN_HEIGHT = 20
SUPPORTED_NIMS_DATATYPES = [
    nims.DataType.Int64.name,
    nims.DataType.Double.name,
    nims.DataType.String.name,
    nims.DataType.Boolean.name,
    nims.DataType.Int64Array1D.name,
    nims.DataType.DoubleArray1D.name,
    nims.DataType.StringArray1D.name,
]


def _get_input_data_elements(
    pins: List[PinInfo],
    relays: List[RelayInfo],
    inputs: List[InputInfo],
) -> List[DataElement]:
    input_data_elements = []
    left_alignment = MeasUIElementPosition.LEFT_ALIGNMENT_START_VALUE
    top_alignment: Union[float, int] = MeasUIElementPosition.TOP_ALIGNMENT_START_VALUE

    height = MeasUIElementPosition.DEFAULT_HEIGHT
    width = MeasUIElementPosition.DEFAULT_WIDTH

    for pin in pins:
        input_data_elements.append(
            DataElement(
                client_id=CLIENT_ID,
                value_type=SpecializedDataType.IORESOURCE,
                left_alignment=left_alignment,
                top_alignment=top_alignment,
                height=height,
                width=width,
                name=pin.name,
            )
        )

        top_alignment += (
            MeasUIElementPosition.TOP_ALIGNMENT_INCREMENTAL_VALUE + height - _REDUCTION_IN_HEIGHT
        )

    for relay in relays:
        input_data_elements.append(
            DataElement(
                client_id=CLIENT_ID,
                left_alignment=MeasUIElementPosition.LEFT_ALIGNMENT_START_VALUE,
                top_alignment=top_alignment,
                height=height,
                width=width,
                value_type=nims.DataType.String.name,
                name=relay.name,
            )
        )
        top_alignment += (
            MeasUIElementPosition.TOP_ALIGNMENT_INCREMENTAL_VALUE + height - _REDUCTION_IN_HEIGHT
        )

    for input_info in inputs:
        value_type = input_info.nims_type.split(".")[2]
        is_array = False

        height = MeasUIElementPosition.DEFAULT_HEIGHT
        width = MeasUIElementPosition.DEFAULT_WIDTH

        if value_type not in SUPPORTED_NIMS_DATATYPES:
            continue

        if value_type == nims.DataType.Double.name:
            value_type = DataType.Double.name

        elif value_type == nims.DataType.Boolean.name:
            height = MeasUIElementPosition.BOOLEAN_HORIZONTAL_SLIDER_HEIGHT
            width = MeasUIElementPosition.BOOLEAN_HORIZONTAL_SLIDER_WIDTH

        elif value_type == nims.DataType.Int64Array1D.name:
            value_type = DataType.Int64.name
            is_array = True

            height = MeasUIElementPosition.ARRAY_HEIGHT
            width = MeasUIElementPosition.ARRAY_WIDTH

        elif value_type == nims.DataType.DoubleArray1D.name:
            value_type = DataType.Double.name
            is_array = True

            height = MeasUIElementPosition.ARRAY_HEIGHT
            width = MeasUIElementPosition.ARRAY_WIDTH

        elif value_type == nims.DataType.StringArray1D.name:
            value_type = DataType.String.name
            is_array = True

            height = MeasUIElementPosition.ARRAY_HEIGHT
            width = MeasUIElementPosition.ARRAY_WIDTH

        input_data_elements.append(
            DataElement(
                client_id=CLIENT_ID,
                left_alignment=MeasUIElementPosition.LEFT_ALIGNMENT_START_VALUE,
                top_alignment=top_alignment,
                height=height,
                width=width,
                value_type=value_type,
                name=input_info.param_name,
                is_array=is_array,
            )
        )

        top_alignment += (
            MeasUIElementPosition.TOP_ALIGNMENT_INCREMENTAL_VALUE
            + (
                height * 3.5
                if input_info.nims_type.split(".")[2]
                in [
                    nims.DataType.Int64Array1D.name,
                    nims.DataType.DoubleArray1D.name,
                    nims.DataType.StringArray1D.name,
                ]
                else height
            )
            - _REDUCTION_IN_HEIGHT
        )

    return input_data_elements


def _get_output_data_elements(outputs: List[OutputInfo]) -> List[DataElement]:
    output_data_elements = []
    top_alignment: Union[float, int] = MeasUIElementPosition.TOP_ALIGNMENT_START_VALUE

    left_alignment = (
        MeasUIElementPosition.LEFT_ALIGNMENT_START_VALUE
        + MeasUIElementPosition.LEFT_ALIGNMENT_INCREMENTAL_VALUE
    )

    for output in outputs:
        value_type = output.nims_type.split(".")[2]
        is_array = False

        height = MeasUIElementPosition.DEFAULT_HEIGHT
        width = MeasUIElementPosition.DEFAULT_WIDTH

        if value_type not in SUPPORTED_NIMS_DATATYPES:
            continue

        if value_type == nims.DataType.Double.name:
            value_type = DataType.Double.name

        elif value_type == nims.DataType.Boolean.name:
            height = MeasUIElementPosition.BOOLEAN_LED_HEIGHT
            width = MeasUIElementPosition.BOOLEAN_LED_WIDTH

        elif value_type == nims.DataType.Int64Array1D.name:
            value_type = DataType.Int64.name
            is_array = True

            height = MeasUIElementPosition.ARRAY_HEIGHT
            width = MeasUIElementPosition.ARRAY_WIDTH

        elif value_type == nims.DataType.DoubleArray1D.name:
            value_type = DataType.Double.name
            is_array = True

            height = MeasUIElementPosition.ARRAY_HEIGHT
            width = MeasUIElementPosition.ARRAY_WIDTH

        elif value_type == nims.DataType.StringArray1D.name:
            value_type = DataType.String.name
            is_array = True

            height = MeasUIElementPosition.ARRAY_HEIGHT
            width = MeasUIElementPosition.ARRAY_WIDTH

        output_data_elements.append(
            DataElement(
                client_id=CLIENT_ID,
                left_alignment=left_alignment,
                top_alignment=top_alignment,
                height=height,
                width=width,
                value_type=value_type,
                name=output.variable_name,
                is_array=is_array,
            )
        )
        top_alignment += (
            MeasUIElementPosition.TOP_ALIGNMENT_INCREMENTAL_VALUE
            + (
                height * 3.5
                if output.nims_type.split(".")[2]
                in [
                    nims.DataType.Int64Array1D.name,
                    nims.DataType.DoubleArray1D.name,
                    nims.DataType.StringArray1D.name,
                ]
                else height
            )
            - _REDUCTION_IN_HEIGHT
        )

    return output_data_elements


def create_measui_file(
    pins: List[PinInfo],
    relays: List[RelayInfo],
    inputs: List[InputInfo],
    outputs: List[OutputInfo],
    file_path: Path,
    measurement_name: str,
    service_class: str,
) -> None:
    """Generate a `.measui` file for the converted measurement.

    Args:
        pins: List of pins.
        relays: List of relays.
        inputs: List of inputs from measurement.
        outputs: List of outputs from measurement.
        file_path: File path of the measurement.
        measurement_name: Measurement name.
        service_class: Service class name.
    """
    input_data_elements = _get_input_data_elements(pins, relays, inputs)
    output_data_elements = _get_output_data_elements(outputs)

    input_ui_elements = create_control_elements(input_data_elements)
    output_ui_elements = create_indicator_elements(output_data_elements)

    measui_path = file_path / measurement_name
    write_measui(
        filepath=measui_path,
        service_class=service_class,
        input_output_elements=input_ui_elements + output_ui_elements,
    )
