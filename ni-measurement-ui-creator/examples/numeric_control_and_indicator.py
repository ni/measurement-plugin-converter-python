"""Example to create numeric control and numeric indicator measui elements.

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

numeric_control_elements = create_control_elements(
    inputs=[
        DataElement(
            client_id=client_id,
            name="Numeric input",
            value_type="Double",  # Refer `SupportedDataType`.
            left_alignment=MeasUIElementPosition.LEFT_ALIGNMENT_START_VALUE,
            top_alignment=MeasUIElementPosition.TOP_ALIGNMENT_START_VALUE,
        ),
        DataElement(
            client_id=client_id,
            name="Second Numeric input",
            value_type="UInt64",  # Refer `SupportedDataType`.
            left_alignment=MeasUIElementPosition.LEFT_ALIGNMENT_START_VALUE,
            top_alignment=(
                MeasUIElementPosition.TOP_ALIGNMENT_START_VALUE
                + MeasUIElementPosition.TOP_ALIGNMENT_INCREMENTAL_VALUE
            ),
        ),
    ]
)


numeric_indicator_elements = create_indicator_elements(
    outputs=[
        DataElement(
            client_id=client_id,
            name="Numeric output",
            value_type="Double",  # Refer `SupportedDataType`.
            left_alignment=(
                MeasUIElementPosition.LEFT_ALIGNMENT_START_VALUE
                + MeasUIElementPosition.LEFT_ALIGNMENT_INCREMENTAL_VALUE
            ),
            top_alignment=MeasUIElementPosition.TOP_ALIGNMENT_START_VALUE,
        ),
        DataElement(
            client_id=client_id,
            name="Second Numeric output",
            value_type="UInt64",  # Refer `SupportedDataType`.
            left_alignment=(
                MeasUIElementPosition.LEFT_ALIGNMENT_START_VALUE
                + MeasUIElementPosition.LEFT_ALIGNMENT_INCREMENTAL_VALUE
            ),
            top_alignment=(
                MeasUIElementPosition.TOP_ALIGNMENT_START_VALUE
                + MeasUIElementPosition.TOP_ALIGNMENT_INCREMENTAL_VALUE
            ),
        ),
    ]
)

# Create a .measui file
create_measui(
    filepath="numeric_controls_indicators",
    input_output_elements=numeric_indicator_elements + numeric_control_elements,
)

print(numeric_control_elements, numeric_indicator_elements, sep="\n\n---------------\n\n")
print("\nMeasUI File created.")
