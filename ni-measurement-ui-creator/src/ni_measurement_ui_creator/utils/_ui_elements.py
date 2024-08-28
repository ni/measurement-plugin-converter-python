"""Create Measurement UI Elements from client."""

from ni_measurement_ui_creator.constants import (
    CLIENT_ID,
    NUMERIC_DATA_TYPE_VALUES,
    TYPE_SPECIFICATION,
    DataType,
    MeasUIElementPosition,
    SpecializedDataType,
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
    input_top_alignment = MeasUIElementPosition.TOP_ALIGNMENT_START_VALUE

    for input in inputs:
        try:
            input_datatype = DataType(input.type)

            if (
                hasattr(input, "repeated")
                and input.repeated
                and input.type in NUMERIC_DATA_TYPE_VALUES
            ):
                input_elements.append(
                    DataElement(
                        client_id=CLIENT_ID,
                        name=input.name,
                        left_alignment=MeasUIElementPosition.LEFT_ALIGNMENT_START_VALUE,
                        top_alignment=input_top_alignment,
                        height=MeasUIElementPosition.ARRAY_HEIGHT,
                        width=MeasUIElementPosition.ARRAY_WIDTH,
                        value_type=input_datatype.name,
                        is_array=True,
                    )
                )
                input_top_alignment += MeasUIElementPosition.TOP_ALIGNMENT_INCREMENTAL_VALUE + (
                    MeasUIElementPosition.TOP_ALIGNMENT_ADDITIONAL_INCREMENTAL_VALUE * 3.5
                )

            elif input.type == DataType.Boolean.value and not (
                hasattr(input, "repeated") and input.repeated
            ):
                input_elements.append(
                    DataElement(
                        client_id=CLIENT_ID,
                        name=input.name,
                        left_alignment=MeasUIElementPosition.LEFT_ALIGNMENT_START_VALUE,
                        top_alignment=input_top_alignment,
                        height=MeasUIElementPosition.BOOLEAN_HORIZONTAL_SLIDER_HEIGHT,
                        width=MeasUIElementPosition.BOOLEAN_HORIZONTAL_SLIDER_WIDTH,
                        value_type=input_datatype.name,
                    )
                )
                input_top_alignment += (
                    MeasUIElementPosition.TOP_ALIGNMENT_INCREMENTAL_VALUE
                    + MeasUIElementPosition.TOP_ALIGNMENT_ADDITIONAL_INCREMENTAL_VALUE * 0.5
                )

            elif (
                input.type == DataType.String.value
                and not (hasattr(input, "repeated") and input.repeated)
                and not input.annotations
            ):
                input_elements.append(
                    DataElement(
                        client_id=CLIENT_ID,
                        name=input.name,
                        left_alignment=MeasUIElementPosition.LEFT_ALIGNMENT_START_VALUE,
                        top_alignment=input_top_alignment,
                        value_type=input_datatype.name,
                    )
                )
                input_top_alignment += MeasUIElementPosition.TOP_ALIGNMENT_INCREMENTAL_VALUE

            elif input.type in NUMERIC_DATA_TYPE_VALUES:
                input_elements.append(
                    DataElement(
                        client_id=CLIENT_ID,
                        name=input.name,
                        left_alignment=MeasUIElementPosition.LEFT_ALIGNMENT_START_VALUE,
                        top_alignment=input_top_alignment,
                        value_type=input_datatype.name,
                    )
                )
                input_top_alignment += MeasUIElementPosition.TOP_ALIGNMENT_INCREMENTAL_VALUE

            elif (
                input.annotations
                and input.annotations[TYPE_SPECIFICATION] == SpecializedDataType.IORESOURCE.lower()
                and hasattr(input, "repeated")
                and input.repeated
            ):
                input_elements.append(
                    DataElement(
                        client_id=CLIENT_ID,
                        name=input.name,
                        left_alignment=MeasUIElementPosition.LEFT_ALIGNMENT_START_VALUE,
                        top_alignment=input_top_alignment,
                        value_type=SpecializedDataType.IORESOURCE_ARR,
                    )
                )
                input_top_alignment += MeasUIElementPosition.TOP_ALIGNMENT_INCREMENTAL_VALUE

            elif (
                input.annotations
                and input.annotations[TYPE_SPECIFICATION] == SpecializedDataType.PIN.lower()
                and not (hasattr(input, "repeated") and input.repeated)
            ):
                input_elements.append(
                    DataElement(
                        client_id=CLIENT_ID,
                        name=input.name,
                        left_alignment=MeasUIElementPosition.LEFT_ALIGNMENT_START_VALUE,
                        top_alignment=input_top_alignment,
                        value_type=SpecializedDataType.PIN,
                    )
                )
                input_top_alignment += MeasUIElementPosition.TOP_ALIGNMENT_INCREMENTAL_VALUE

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
    output_left_alignment = (
        MeasUIElementPosition.LEFT_ALIGNMENT_START_VALUE
        + MeasUIElementPosition.LEFT_ALIGNMENT_INCREMENTAL_VALUE
    )
    output_top_alignment = MeasUIElementPosition.TOP_ALIGNMENT_START_VALUE

    for output in outputs:
        try:
            output_datatype = DataType(output.type)

            if (
                hasattr(output, "repeated")
                and output.repeated
                and output.type in NUMERIC_DATA_TYPE_VALUES
            ):
                output_elements.append(
                    DataElement(
                        client_id=CLIENT_ID,
                        name=output.name,
                        left_alignment=output_left_alignment,
                        top_alignment=output_top_alignment,
                        value_type=output_datatype.name,
                        height=MeasUIElementPosition.ARRAY_HEIGHT,
                        width=MeasUIElementPosition.ARRAY_WIDTH,
                        is_array=True,
                    )
                )
                output_top_alignment += MeasUIElementPosition.TOP_ALIGNMENT_INCREMENTAL_VALUE + (
                    MeasUIElementPosition.TOP_ALIGNMENT_ADDITIONAL_INCREMENTAL_VALUE * 3.5
                )

            elif output.type == DataType.Boolean.value and not (
                hasattr(output, "repeated") and output.repeated
            ):
                output_elements.append(
                    DataElement(
                        client_id=CLIENT_ID,
                        name=output.name,
                        left_alignment=output_left_alignment,
                        top_alignment=output_top_alignment,
                        value_type=output_datatype.name,
                        height=MeasUIElementPosition.BOOLEAN_LED_HEIGHT,
                        width=MeasUIElementPosition.BOOLEAN_LED_WIDTH,
                    )
                )
                output_top_alignment += (
                    MeasUIElementPosition.TOP_ALIGNMENT_INCREMENTAL_VALUE
                    + MeasUIElementPosition.TOP_ALIGNMENT_ADDITIONAL_INCREMENTAL_VALUE * 0.5
                )

            elif output.type == DataType.String.value and not (
                hasattr(output, "repeated") and output.repeated
            ):
                output_elements.append(
                    DataElement(
                        client_id=CLIENT_ID,
                        name=output.name,
                        left_alignment=output_left_alignment,
                        top_alignment=output_top_alignment,
                        value_type=output_datatype.name,
                    )
                )
                output_top_alignment += MeasUIElementPosition.TOP_ALIGNMENT_INCREMENTAL_VALUE

            elif output.type in NUMERIC_DATA_TYPE_VALUES:
                output_elements.append(
                    DataElement(
                        client_id=CLIENT_ID,
                        name=output.name,
                        left_alignment=output_left_alignment,
                        top_alignment=output_top_alignment,
                        value_type=output_datatype.name,
                    )
                )
                output_top_alignment += MeasUIElementPosition.TOP_ALIGNMENT_INCREMENTAL_VALUE

        except ValueError:
            pass

    return create_indicator_elements(output_elements)
