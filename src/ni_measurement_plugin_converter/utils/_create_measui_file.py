"""Creation of .measui file for the converted measurement."""

import os
from typing import List

import ni_measurement_plugin_sdk_service as nims
from ni_measurement_ui_creator.constants import (
    CLIENT_ID,
    NUMERIC_DATA_TYPE_NAMES,
    DataType,
    MeasUIElementPosition,
    SpecializedDataType,
)
from ni_measurement_ui_creator.models import DataElement
from ni_measurement_ui_creator.utils._create_measui import create_measui
from ni_measurement_ui_creator.utils._helpers import (
    create_control_elements,
    create_indicator_elements,
)

from ni_measurement_plugin_converter.models import InputInfo, OutputInfo

PIN_NAMES = "pin_names"


def get_input_data_elements(inputs: List[InputInfo]) -> List[DataElement]:
    """Get input data elements for creating `measui` file.

    Args:
        inputs (List[InputInfo]): List of inputs from measurement.

    Returns:
        List[DataElement]: List of data element for input UI compenents.
    """
    input_data_elements = [
        DataElement(
            client_id=CLIENT_ID,
            value_type=SpecializedDataType.IORESOURCE_ARR,
            left_alignment=MeasUIElementPosition.LEFT_ALIGNMENT_START_VALUE,
            top_alignment=MeasUIElementPosition.TOP_ALIGNMENT_START_VALUE,
            name=PIN_NAMES,
        )
    ]
    top_alignment = (
        MeasUIElementPosition.TOP_ALIGNMENT_START_VALUE
        + MeasUIElementPosition.TOP_ALIGNMENT_INCREMENTAL_VALUE
    )

    for input in inputs:
        value_type = input.nims_type.split(".")[2]
        value_type = DataType.Single.name if value_type == nims.DataType.Float.name else value_type

        if value_type in NUMERIC_DATA_TYPE_NAMES:
            input_data_elements.append(
                DataElement(
                    client_id=CLIENT_ID,
                    left_alignment=MeasUIElementPosition.LEFT_ALIGNMENT_START_VALUE,
                    top_alignment=top_alignment,
                    value_type=value_type,
                    name=input.param_name,
                )
            )
            top_alignment += MeasUIElementPosition.TOP_ALIGNMENT_INCREMENTAL_VALUE

        elif value_type == nims.DataType.String.name:
            input_data_elements.append(
                DataElement(
                    client_id=CLIENT_ID,
                    left_alignment=MeasUIElementPosition.LEFT_ALIGNMENT_START_VALUE,
                    top_alignment=top_alignment,
                    value_type=DataType.Single.name,
                    name=input.param_name,
                )
            )
            top_alignment += MeasUIElementPosition.TOP_ALIGNMENT_INCREMENTAL_VALUE

        elif value_type == DataType.Boolean.name:
            input_data_elements.append(
                DataElement(
                    client_id=CLIENT_ID,
                    left_alignment=MeasUIElementPosition.LEFT_ALIGNMENT_START_VALUE,
                    top_alignment=top_alignment,
                    value_type=value_type,
                    name=input.param_name,
                )
            )
            top_alignment += MeasUIElementPosition.TOP_ALIGNMENT_INCREMENTAL_VALUE

        elif value_type == nims.DataType.Int64Array1D.name:
            input_data_elements.append(
                DataElement(
                    client_id=CLIENT_ID,
                    left_alignment=MeasUIElementPosition.LEFT_ALIGNMENT_START_VALUE,
                    top_alignment=top_alignment,
                    value_type=DataType.Int64.name,
                    name=input.param_name,
                    is_array=True,
                )
            )
            top_alignment += MeasUIElementPosition.TOP_ALIGNMENT_INCREMENTAL_VALUE

        elif value_type == nims.DataType.FloatArray1D.name:
            input_data_elements.append(
                DataElement(
                    client_id=CLIENT_ID,
                    left_alignment=MeasUIElementPosition.LEFT_ALIGNMENT_START_VALUE,
                    top_alignment=top_alignment,
                    value_type=DataType.Single.name,
                    name=input.param_name,
                    is_array=True,
                )
            )
            top_alignment += MeasUIElementPosition.TOP_ALIGNMENT_INCREMENTAL_VALUE

    return input_data_elements


def get_output_data_elements(outputs: List[OutputInfo]) -> List[DataElement]:
    """Get output data elements for creating `measui` file.

    Args:
        outputs (List[OutputInfo]): List of outputs from measurement.

    Returns:
        List[DataElement]: List of data element for output UI compenents.
    """
    output_data_elements = []
    top_alignment = MeasUIElementPosition.TOP_ALIGNMENT_START_VALUE
    left_alignment = (
        MeasUIElementPosition.LEFT_ALIGNMENT_START_VALUE
        + MeasUIElementPosition.LEFT_ALIGNMENT_INCREMENTAL_VALUE
    )

    for output in outputs:
        value_type = output.nims_type.split(".")[2]
        value_type = DataType.Single.name if value_type == nims.DataType.Float.name else value_type

        if value_type in NUMERIC_DATA_TYPE_NAMES:
            output_data_elements.append(
                DataElement(
                    client_id=CLIENT_ID,
                    left_alignment=left_alignment,
                    top_alignment=top_alignment,
                    value_type=value_type,
                    name=output.variable_name,
                )
            )
            top_alignment += MeasUIElementPosition.TOP_ALIGNMENT_INCREMENTAL_VALUE

        elif value_type == nims.DataType.String.name:
            output_data_elements.append(
                DataElement(
                    client_id=CLIENT_ID,
                    left_alignment=MeasUIElementPosition.LEFT_ALIGNMENT_START_VALUE,
                    top_alignment=top_alignment,
                    value_type=DataType.Single.name,
                    name=output.variable_name,
                )
            )
            top_alignment += MeasUIElementPosition.TOP_ALIGNMENT_INCREMENTAL_VALUE

        elif value_type == DataType.Boolean.name:
            output_data_elements.append(
                DataElement(
                    client_id=CLIENT_ID,
                    left_alignment=MeasUIElementPosition.LEFT_ALIGNMENT_START_VALUE,
                    top_alignment=top_alignment,
                    value_type=value_type,
                    name=output.variable_name,
                )
            )
            top_alignment += MeasUIElementPosition.TOP_ALIGNMENT_INCREMENTAL_VALUE

        elif value_type == nims.DataType.Int64Array1D.name:
            output_data_elements.append(
                DataElement(
                    client_id=CLIENT_ID,
                    left_alignment=MeasUIElementPosition.LEFT_ALIGNMENT_START_VALUE,
                    top_alignment=top_alignment,
                    value_type=value_type,
                    name=output.variable_name,
                    is_array=True,
                )
            )
            top_alignment += MeasUIElementPosition.TOP_ALIGNMENT_INCREMENTAL_VALUE

        elif value_type == nims.DataType.FloatArray1D.name:
            output_data_elements.append(
                DataElement(
                    client_id=CLIENT_ID,
                    left_alignment=MeasUIElementPosition.LEFT_ALIGNMENT_START_VALUE,
                    top_alignment=top_alignment,
                    value_type=DataType.Single.name,
                    name=output.variable_name,
                    is_array=True,
                )
            )
            top_alignment += MeasUIElementPosition.TOP_ALIGNMENT_INCREMENTAL_VALUE

    return output_data_elements


def create_measui_file(
    inputs: List[InputInfo],
    outputs: List[OutputInfo],
    file_path: str,
    measurement_name: str,
) -> None:
    """Create `.measui` file for the converted measurement.

    Args:
        inputs (List[InputInfo]): List of inputs from measurement.
        outputs (List[OutputInfo]): List of  outputs from measurement.
        file_path (str): File path of the measurement.
        measurement_name (str): Measurement name.

    Returns:
        None.
    """
    input_data_elements = get_input_data_elements(inputs)
    output_data_elements = get_output_data_elements(outputs)

    input_ui_elements = create_control_elements(input_data_elements)
    output_ui_elements = create_indicator_elements(output_data_elements)

    measui_path = os.path.join(file_path, measurement_name)
    create_measui(
        filepath=measui_path,
        input_output_elements=input_ui_elements + output_ui_elements,
    )
