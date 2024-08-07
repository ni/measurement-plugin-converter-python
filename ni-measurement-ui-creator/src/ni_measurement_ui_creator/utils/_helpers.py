"""Helpers functions of Measurement UI creator."""

from typing import List

from ni_measurement_ui_creator.constants import (
    NUMERIC_DATA_TYPE_NAMES,
    DataType,
    SpecializedDataType,
)
from ni_measurement_ui_creator.models import DataElement
from ni_measurement_ui_creator.utils._numeric_elements import (
    create_numeric_array_control,
    create_numeric_array_indicator,
    create_numeric_control,
    create_numeric_indicator,
)
from ni_measurement_ui_creator.utils._special_data_elements import (
    create_ioresource_array_control,
    create_pin_control,
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

    for data_element in inputs:
        if data_element.value_type in NUMERIC_DATA_TYPE_NAMES and data_element.is_array:
            input_elements += create_numeric_array_control(data_element)

        elif data_element.value_type == DataType.Boolean.name:
            input_elements += create_toggle_image_button(data_element)

        elif data_element.value_type == DataType.String.name and not data_element.is_array:
            input_elements += create_string_control(data_element)

        elif data_element.value_type in NUMERIC_DATA_TYPE_NAMES:
            input_elements += create_numeric_control(data_element)

        elif data_element.value_type == SpecializedDataType.PIN:
            input_elements += create_pin_control(data_element)

        elif data_element.value_type == SpecializedDataType.IORESOURCE_ARR:
            input_elements += create_ioresource_array_control(data_element)

    return input_elements


def create_indicator_elements(outputs: List[DataElement]) -> str:
    """Create indicator elements for `.measui` file.

    Args:
        outputs (List[DataElement]): List of outputs elements.

    Returns:
        str: Measurement UI output elements.
    """
    output_elements = ""

    for output in outputs:
        if output.value_type in NUMERIC_DATA_TYPE_NAMES and output.is_array:
            output_elements += create_numeric_array_indicator(output)

        elif output.value_type == DataType.Boolean.name:
            output_elements += create_toggle_image_indicator(output)

        elif output.value_type == DataType.String.name and not output.is_array:
            output_elements += create_string_indicator(output)

        elif output.value_type in NUMERIC_DATA_TYPE_NAMES:
            output_elements += create_numeric_indicator(output)

    return output_elements
