"""Example to create numeric array input and numeric array output measui elements.

Note: CLIENT ID should be same throughout a measui file.
"""

import uuid

from ni_measurement_ui_creator.constants._ui_elements import (
    MeasUIElementPosition,
    SupportedDataType,
)
from ni_measurement_ui_creator.models import DataElement
from ni_measurement_ui_creator.utils._create_measui import create_measui
from ni_measurement_ui_creator.utils._helpers import (
    create_control_elements,
    create_indicator_elements,
)

# Refer `SupportedDataType` class for supported `value_type`.

# Any unique id will work.
client_id = uuid.uuid4()

array_input_elements = create_control_elements(
    inputs=[
        DataElement(
            client_id=client_id,
            name="Array In",
            value_type=SupportedDataType.DOUBLE,
            left_alignment=MeasUIElementPosition.LEFT_ALIGNMENT_START_VALUE,
            top_alignment=MeasUIElementPosition.TOP_ALIGNMENT_START_VALUE,
            is_array=True,
        ),
        DataElement(
            client_id=client_id,
            name="Second Array In",
            value_type=SupportedDataType.UINT32,
            left_alignment=MeasUIElementPosition.LEFT_ALIGNMENT_START_VALUE,
            top_alignment=(
                MeasUIElementPosition.TOP_ALIGNMENT_START_VALUE
                + MeasUIElementPosition.TOP_ALIGNMENT_INCREMENTAL_VALUE
                + MeasUIElementPosition.TOP_ALIGNMENT_ADDITIONAL_INCREMENTAL_VALUE
                * MeasUIElementPosition.INCREASE_FACTOR
            ),
            is_array=True,
        ),
    ]
)

array_output_elements = create_indicator_elements(
    outputs=[
        DataElement(
            client_id=client_id,
            name="Array Out",
            value_type=SupportedDataType.DOUBLE,
            left_alignment=(
                MeasUIElementPosition.LEFT_ALIGNMENT_START_VALUE
                + MeasUIElementPosition.LEFT_ALIGNMENT_INCREMENTAL_VALUE
            ),
            top_alignment=MeasUIElementPosition.TOP_ALIGNMENT_START_VALUE,
            is_array=True,
        ),
        DataElement(
            client_id=client_id,
            name="Second Array Out",
            value_type=SupportedDataType.UINT32,
            left_alignment=(
                MeasUIElementPosition.LEFT_ALIGNMENT_START_VALUE
                + MeasUIElementPosition.LEFT_ALIGNMENT_INCREMENTAL_VALUE
            ),
            top_alignment=(
                MeasUIElementPosition.TOP_ALIGNMENT_START_VALUE
                + MeasUIElementPosition.TOP_ALIGNMENT_INCREMENTAL_VALUE
                + MeasUIElementPosition.TOP_ALIGNMENT_ADDITIONAL_INCREMENTAL_VALUE
                * MeasUIElementPosition.INCREASE_FACTOR
            ),
            is_array=True,
        ),
    ]
)

# Create a .measui file.
create_measui(
    filepath="numeric_arrays",
    input_output_elements=array_input_elements + array_output_elements,
)

print(array_input_elements, array_output_elements, sep="\n\n---------------\n\n")
print("\nMeasUI File created.")
