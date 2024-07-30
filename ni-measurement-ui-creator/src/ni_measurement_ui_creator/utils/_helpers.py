"""Helpers functions of Measurement UI creator."""

from typing import List

from ni_measurement_ui_creator.constants import (
    NUMERIC_DATA_TYPE_NAMES,
    MeasUiElementPosition,
    SupportedDataType,
)
from ni_measurement_ui_creator.models import DataElement
from ni_measurement_ui_creator.utils._numeric_elements import (
    create_numeric_array_input,
    create_numeric_array_output,
    create_numeric_control,
    create_numeric_indicator,
)
from ni_measurement_ui_creator.utils._string_elements import (
    create_string_control,
    create_string_indicator,
)
from ni_measurement_ui_creator.utils._toggle_elements import (
    create_toggle_image_button,
    create_toggle_image_indicator,
)


def create_control_elements(inputs: List[DataElement]) -> str:
    """Create control elements for `.measui` file.

    Args:
        inputs (List[DataElement]): List of input elements.

    Returns:
        str: Measurement UI input elements.
    """
    input_elements = ""
    inputs_top_value = MeasUiElementPosition.TOP_START_VALUE

    for data_element in inputs:
        if data_element.value_type in NUMERIC_DATA_TYPE_NAMES and data_element.is_array:
            input_elements += create_numeric_array_input(data_element)

        elif data_element.value_type == SupportedDataType.Boolean.name and not (
            data_element.is_array
        ):
            input_elements += create_toggle_image_button(data_element)

        elif data_element.value_type == SupportedDataType.String.name and not (
            data_element.is_array
        ):
            input_elements += create_string_control(data_element)

        elif data_element.value_type in NUMERIC_DATA_TYPE_NAMES:
            input_elements += create_numeric_control(data_element)

        inputs_top_value += MeasUiElementPosition.TOP_INCREMENTAL_VALUE

    return input_elements


def create_indicator_elements(outputs: List[DataElement]) -> str:
    """Create indicator elements for `.measui` file.

    Args:
        outputs (List[DataElement]): List of outputs elements.

    Returns:
        str: Measurement UI output elements.
    """
    output_elements = ""
    outputs_top_value = MeasUiElementPosition.TOP_START_VALUE

    for output in outputs:
        if (
            output.value_type
            in [
                SupportedDataType.Int32.name,
                SupportedDataType.Int64.name,
                SupportedDataType.UInt32.name,
                SupportedDataType.UInt64.name,
                SupportedDataType.Single.name,
                SupportedDataType.Double.name,
            ]
            and output.is_array
        ):
            output_elements += create_numeric_array_output(output)

        elif output.value_type == SupportedDataType.Boolean.name and not output.is_array:
            output_elements += create_toggle_image_indicator(output)

        elif output.value_type == SupportedDataType.String.name and not output.is_array:
            output_elements += create_string_indicator(output)

        elif output.value_type in [
            SupportedDataType.Int32.name,
            SupportedDataType.Int64.name,
            SupportedDataType.UInt32.name,
            SupportedDataType.UInt64.name,
            SupportedDataType.Single.name,
            SupportedDataType.Double.name,
        ]:
            output_elements += create_numeric_indicator(output)

        outputs_top_value += MeasUiElementPosition.TOP_INCREMENTAL_VALUE

    return output_elements
