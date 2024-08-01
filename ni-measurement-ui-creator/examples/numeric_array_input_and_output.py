"""Example to create numeric array input and numeric array output measui elements.

Note: CLIENT ID should be same throughout a measui file.
"""

import uuid

from ni_measurement_ui_creator.constants._ui_elements import MeasUIElementPosition
from ni_measurement_ui_creator.models import DataElement
from ni_measurement_ui_creator.utils._create_measui import create_measui
from ni_measurement_ui_creator.utils._helpers import (
    create_control_elements,
    create_indicator_elements,
)


# Refer `SupportedDataType` Enum for supported `value_type`.
# Use corresponding key strings according to the needs.

# Any unique id will work.
client_id = uuid.uuid4()

array_input_elements = create_control_elements(
    inputs=[
        DataElement(
            client_id=client_id,
            name="Array In",
            value_type="Double",  # Refer `SupportedDataType`.
            left_alignment=MeasUIElementPosition.LEFT_START_VALUE,
            top_alignment=MeasUIElementPosition.TOP_START_VALUE,
        ),
        DataElement(
            client_id=client_id,
            name="Second Array In",
            value_type="UInt32",  # Refer `SupportedDataType`.
            left_alignment=MeasUIElementPosition.LEFT_START_VALUE,
            top_alignment=(
                MeasUIElementPosition.TOP_START_VALUE + MeasUIElementPosition.TOP_INCREMENTAL_VALUE
            ),
        ),
    ]
)

array_output_elements = create_indicator_elements(
    outputs=[
        DataElement(
            client_id=client_id,
            name="Array Out",
            value_type="Double",  # Refer `SupportedDataType`.
            left_alignment=(
                MeasUIElementPosition.LEFT_START_VALUE
                + MeasUIElementPosition.LEFT_INCREMENTAL_VALUE
            ),
            top_alignment=MeasUIElementPosition.TOP_START_VALUE,
        ),
        DataElement(
            client_id=client_id,
            name="Second Array Out",
            value_type="UInt32",  # Refer `SupportedDataType`.
            left_alignment=(
                MeasUIElementPosition.LEFT_START_VALUE
                + MeasUIElementPosition.LEFT_INCREMENTAL_VALUE
            ),
            top_alignment=(
                MeasUIElementPosition.TOP_START_VALUE + MeasUIElementPosition.TOP_INCREMENTAL_VALUE
            ),
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
