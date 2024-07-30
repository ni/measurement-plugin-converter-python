"""Create Measurement UI Elements from client."""

from ni_measurement_ui_creator.constants import (
    CLIENT_ID,
    NUMERIC_DATA_TYPE_VALUES,
    MeasUiElementPosition,
    SupportedDataType,
)
from ni_measurement_ui_creator.models import DataElement
from ni_measurement_ui_creator.utils._helpers import (
    create_control_elements,
    create_indicator_elements,
)


def create_input_elements_from_client(inputs) -> str:
    """Create Measui input elements.

    Args:
        inputs (): Input elements from metadata using client.

    Returns:
        str: MeasUI input elements.
    """
    input_elements = []
    inputs_top_value = MeasUiElementPosition.TOP_START_VALUE

    for input in inputs:
        try:
            input_datatype = SupportedDataType(input.type)

            if (
                hasattr(input, "repeated")
                and input.repeated
                and input.type in NUMERIC_DATA_TYPE_VALUES
            ):
                input_elements.append(
                    DataElement(
                        client_id=CLIENT_ID,
                        name=input.name,
                        left_value=MeasUiElementPosition.LEFT_START_VALUE,
                        top_value=inputs_top_value,
                        value_type=input_datatype.name,
                        is_array=True,
                    )
                )

            elif input.type == SupportedDataType.Boolean.value and not (
                hasattr(input, "repeated") and input.repeated
            ):
                input_elements.append(
                    DataElement(
                        client_id=CLIENT_ID,
                        name=input.name,
                        left_value=MeasUiElementPosition.LEFT_START_VALUE,
                        top_value=inputs_top_value,
                        value_type=input_datatype.name,
                    )
                )

            elif input.type == SupportedDataType.String.value and not (
                hasattr(input, "repeated") and input.repeated
            ):
                input_elements.append(
                    DataElement(
                        client_id=CLIENT_ID,
                        name=input.name,
                        left_value=MeasUiElementPosition.LEFT_START_VALUE,
                        top_value=inputs_top_value,
                        value_type=input_datatype.name,
                    )
                )

            elif input.type in NUMERIC_DATA_TYPE_VALUES:
                input_elements.append(
                    DataElement(
                        client_id=CLIENT_ID,
                        name=input.name,
                        left_value=MeasUiElementPosition.LEFT_START_VALUE,
                        top_value=inputs_top_value,
                        lable_left_value=MeasUiElementPosition.LEFT_START_VALUE,
                        value_type=input_datatype.name,
                    )
                )

            inputs_top_value += MeasUiElementPosition.TOP_INCREMENTAL_VALUE

        except ValueError:
            pass

    return create_control_elements(input_elements)


def create_output_elements_from_client(outputs) -> str:
    """Create Measui output elements.

    Args:
        outputs (): Output elements from metadata using client.

    Returns:
        str: MeasUI output elements.
    """
    output_elements = []
    output_start_position = (
        MeasUiElementPosition.LEFT_START_VALUE + MeasUiElementPosition.LEFT_INCREMENTAL_VALUE
    )
    outputs_top_value = MeasUiElementPosition.TOP_START_VALUE

    for output in outputs:
        try:
            output_datatype = SupportedDataType(output.type)

            if (
                hasattr(output, "repeated")
                and output.repeated
                and (
                    output.type
                    in [
                        SupportedDataType.Int32.value,
                        SupportedDataType.Int64.value,
                        SupportedDataType.UInt32.value,
                        SupportedDataType.UInt64.value,
                        SupportedDataType.Single.value,
                        SupportedDataType.Double.value,
                    ]
                )
            ):
                output_elements.append(
                    DataElement(
                        client_id=CLIENT_ID,
                        name=output.name,
                        left_value=output_start_position,
                        top_value=outputs_top_value,
                        value_type=output_datatype.name,
                        is_array=True,
                    )
                )

            elif output.type == SupportedDataType.Boolean.value and not (
                hasattr(output, "repeated") and output.repeated
            ):
                output_elements.append(
                    DataElement(
                        client_id=CLIENT_ID,
                        name=output.name,
                        left_value=output_start_position,
                        top_value=outputs_top_value,
                        value_type=output_datatype.name,
                    )
                )

            elif output.type == SupportedDataType.String.value and not (
                hasattr(output, "repeated") and output.repeated
            ):
                output_elements.append(
                    DataElement(
                        client_id=CLIENT_ID,
                        name=output.name,
                        left_value=output_start_position,
                        top_value=outputs_top_value,
                        value_type=output_datatype.name,
                    )
                )

            elif output.type in [
                SupportedDataType.Int32.value,
                SupportedDataType.Int64.value,
                SupportedDataType.UInt32.value,
                SupportedDataType.UInt64.value,
                SupportedDataType.Single.value,
                SupportedDataType.Double.value,
            ]:
                output_elements.append(
                    DataElement(
                        client_id=CLIENT_ID,
                        name=output.name,
                        left_value=output_start_position,
                        top_value=outputs_top_value,
                        value_type=output_datatype.name,
                    )
                )

            outputs_top_value += MeasUiElementPosition.TOP_INCREMENTAL_VALUE

        except ValueError:
            pass

    return create_indicator_elements(output_elements)
