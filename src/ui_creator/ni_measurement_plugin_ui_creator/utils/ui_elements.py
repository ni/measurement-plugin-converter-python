"""Create Measurement UI Elements from client."""

from typing import List, Union, Tuple
from uuid import UUID

from ni_measurement_plugin_sdk_service._internal.stubs.ni.measurementlink.measurement.v1.measurement_service_pb2 import (
    ConfigurationParameter as V1ConfigParam,
)
from ni_measurement_plugin_sdk_service._internal.stubs.ni.measurementlink.measurement.v1.measurement_service_pb2 import (
    Output as V1Output,
)
from ni_measurement_plugin_sdk_service._internal.stubs.ni.measurementlink.measurement.v2.measurement_service_pb2 import (
    ConfigurationParameter as V2ConfigParam,
)
from ni_measurement_plugin_sdk_service._internal.stubs.ni.measurementlink.measurement.v2.measurement_service_pb2 import (
    Output as V2Output,
)

from ni_measurement_plugin_ui_creator.constants import (
    CLIENT_ID,
    NUMERIC_DATA_TYPE_VALUES,
    TYPE_SPECIFICATION,
    DataType,
    MeasUIElementPosition,
    SpecializedDataType,
)
from ni_measurement_plugin_ui_creator.models import DataElement
from ni_measurement_plugin_ui_creator.utils.helpers import (
    create_control_elements,
    create_indicator_elements,
)


def create_input_elements_from_client(
    inputs: List[Union[V1ConfigParam, V2ConfigParam]],
    client_id: Union[str, UUID] = CLIENT_ID,
    input_top_alignment: Union[int, float] = MeasUIElementPosition.TOP_ALIGNMENT_START_VALUE,
    input_left_alignment: Union[int, float] = MeasUIElementPosition.LEFT_ALIGNMENT_START_VALUE,
) -> Tuple[str, Union[int, float]]:
    """Create input elements.

    Args:
        inputs (List[Union[V1ConfigParam, V2ConfigParam]]): Inputs from Metadata.
        client_id (Union[str, UUID], optional): Client ID. Defaults to CLIENT_ID.
        input_top_alignment (Union[int, float], optional): Input top alignment value. \
        Defaults to MeasUIElementPosition.TOP_ALIGNMENT_START_VALUE.
        input_left_alignment (Union[int, float], optional): Input left alignment value. \
        Defaults to MeasUIElementPosition.LEFT_ALIGNMENT_START_VALUE.

    Returns:
        Tuple[str, Union[int, float]: Control elements and input elements top alignment.
    """
    input_elements = []

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
                        client_id=client_id,
                        name=input.name,
                        left_alignment=input_left_alignment,
                        top_alignment=input_top_alignment,
                        height=MeasUIElementPosition.ARRAY_HEIGHT,
                        width=MeasUIElementPosition.ARRAY_WIDTH,
                        value_type=input_datatype.name,
                        is_array=True,
                    )
                )
                input_top_alignment += MeasUIElementPosition.TOP_ALIGNMENT_INCREMENTAL_VALUE + (
                    MeasUIElementPosition.TOP_ALIGNMENT_ADDITIONAL_INCREMENTAL_VALUE
                    * MeasUIElementPosition.INCREASE_FACTOR
                )

            elif input.type == DataType.Boolean.value and not (
                hasattr(input, "repeated") and input.repeated
            ):
                input_elements.append(
                    DataElement(
                        client_id=client_id,
                        name=input.name,
                        left_alignment=input_left_alignment,
                        top_alignment=input_top_alignment,
                        height=MeasUIElementPosition.BOOLEAN_HORIZONTAL_SLIDER_HEIGHT,
                        width=MeasUIElementPosition.BOOLEAN_HORIZONTAL_SLIDER_WIDTH,
                        value_type=input_datatype.name,
                    )
                )
                input_top_alignment += (
                    MeasUIElementPosition.TOP_ALIGNMENT_INCREMENTAL_VALUE
                    + MeasUIElementPosition.TOP_ALIGNMENT_ADDITIONAL_INCREMENTAL_VALUE
                    * MeasUIElementPosition.REDUCE_FACTOR
                )

            elif (
                input.type == DataType.String.value
                and not (hasattr(input, "repeated") and input.repeated)
                and not input.annotations
            ):
                input_elements.append(
                    DataElement(
                        client_id=client_id,
                        name=input.name,
                        left_alignment=input_left_alignment,
                        top_alignment=input_top_alignment,
                        value_type=input_datatype.name,
                    )
                )
                input_top_alignment += MeasUIElementPosition.TOP_ALIGNMENT_INCREMENTAL_VALUE

            elif input.type in NUMERIC_DATA_TYPE_VALUES:
                input_elements.append(
                    DataElement(
                        client_id=client_id,
                        name=input.name,
                        left_alignment=input_left_alignment,
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
                        client_id=client_id,
                        name=input.name,
                        left_alignment=input_left_alignment,
                        top_alignment=input_top_alignment,
                        value_type=SpecializedDataType.IORESOURCE_ARR,
                    )
                )
                input_top_alignment += MeasUIElementPosition.TOP_ALIGNMENT_INCREMENTAL_VALUE

            elif (
                input.annotations
                and (
                    input.annotations[TYPE_SPECIFICATION] == SpecializedDataType.PIN.lower()
                    or input.annotations[TYPE_SPECIFICATION]
                    == SpecializedDataType.IORESOURCE.lower()
                )
                and not (hasattr(input, "repeated") and input.repeated)
            ):
                input_elements.append(
                    DataElement(
                        client_id=client_id,
                        name=input.name,
                        left_alignment=input_left_alignment,
                        top_alignment=input_top_alignment,
                        value_type=SpecializedDataType.PIN,
                    )
                )
                input_top_alignment += MeasUIElementPosition.TOP_ALIGNMENT_INCREMENTAL_VALUE

            elif input.type == DataType.String.value and input.repeated and not input.annotations:
                input_elements.append(
                    DataElement(
                        client_id=client_id,
                        name=input.name,
                        left_alignment=input_left_alignment,
                        top_alignment=input_top_alignment,
                        height=MeasUIElementPosition.ARRAY_HEIGHT,
                        width=MeasUIElementPosition.ARRAY_WIDTH,
                        value_type=input_datatype.name,
                        is_array=True,
                    )
                )
                input_top_alignment += MeasUIElementPosition.TOP_ALIGNMENT_INCREMENTAL_VALUE + (
                    MeasUIElementPosition.TOP_ALIGNMENT_ADDITIONAL_INCREMENTAL_VALUE
                    * MeasUIElementPosition.INCREASE_FACTOR
                )

        except ValueError:
            pass

    return create_control_elements(input_elements), input_top_alignment


def create_output_elements_from_client(
    outputs: List[Union[V1Output, V2Output]],
    client_id: Union[str, UUID] = CLIENT_ID,
    output_top_alignment: Union[int, float] = MeasUIElementPosition.TOP_ALIGNMENT_START_VALUE,
    output_left_alignment: Union[int, float] = (
        MeasUIElementPosition.LEFT_ALIGNMENT_START_VALUE
        + MeasUIElementPosition.LEFT_ALIGNMENT_INCREMENTAL_VALUE
    ),
) -> str:
    """Create output elements.

    Args:
        outputs (List[Union[V1Output, V2Output]]): Output elements from Metadata.
        client_id (Union[str, UUID], optional): Client ID. Defaults to CLIENT_ID.
        output_top_alignment (Union[int, float], optional): Output top alignment value. \
        Defaults to MeasUIElementPosition.TOP_ALIGNMENT_START_VALUE.
        output_left_alignment (Union[int, float], optional): Output left alignment value.\
        Defaults to \
        (MeasUIElementPosition.LEFT_ALIGNMENT_START_VALUE + 
        MeasUIElementPosition.LEFT_ALIGNMENT_INCREMENTAL_VALUE).

    Returns:
        str: Indicator elements.
    """
    output_elements = []

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
                        client_id=client_id,
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
                    MeasUIElementPosition.TOP_ALIGNMENT_ADDITIONAL_INCREMENTAL_VALUE
                    * MeasUIElementPosition.INCREASE_FACTOR
                )

            elif output.type == DataType.Boolean.value and not (
                hasattr(output, "repeated") and output.repeated
            ):
                output_elements.append(
                    DataElement(
                        client_id=client_id,
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
                    + MeasUIElementPosition.TOP_ALIGNMENT_ADDITIONAL_INCREMENTAL_VALUE
                    * MeasUIElementPosition.REDUCE_FACTOR
                )

            elif (
                output.type == DataType.String.value
                and not (hasattr(output, "repeated") and output.repeated)
                and not output.annotations
            ):
                output_elements.append(
                    DataElement(
                        client_id=client_id,
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
                        client_id=client_id,
                        name=output.name,
                        left_alignment=output_left_alignment,
                        top_alignment=output_top_alignment,
                        value_type=output_datatype.name,
                    )
                )
                output_top_alignment += MeasUIElementPosition.TOP_ALIGNMENT_INCREMENTAL_VALUE

            elif (
                output.type == DataType.String.value and output.repeated and not output.annotations
            ):
                output_elements.append(
                    DataElement(
                        client_id=client_id,
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
                    MeasUIElementPosition.TOP_ALIGNMENT_ADDITIONAL_INCREMENTAL_VALUE
                    * MeasUIElementPosition.INCREASE_FACTOR
                )

        except ValueError:
            pass

    return create_indicator_elements(output_elements)
