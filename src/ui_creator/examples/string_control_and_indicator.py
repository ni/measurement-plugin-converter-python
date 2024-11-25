"""Example to create string control and string indicator measui elements.

Note: CLIENT_ID should be same throughout a measui file.
"""

import uuid

from ni_measurement_plugin_ui_creator.constants import MeasUIElementPosition, SupportedDataType
from ni_measurement_plugin_ui_creator.models import DataElement
from ni_measurement_plugin_ui_creator.utils.create_measui import write_measui
from ni_measurement_plugin_ui_creator.utils.helpers import (
    create_control_elements,
    create_indicator_elements,
)

# Refer `SupportedDataType` class for supported `value_type`.

# Any unique id will work.
client_id = uuid.uuid4()

string_control_elements = create_control_elements(
    inputs=[
        DataElement(
            client_id=client_id,
            name="String In",
            left_alignment=MeasUIElementPosition.LEFT_ALIGNMENT_START_VALUE,
            top_alignment=MeasUIElementPosition.TOP_ALIGNMENT_START_VALUE,
            value_type=SupportedDataType.STR,
        ),
        DataElement(
            client_id=client_id,
            name="Second String In",
            left_alignment=MeasUIElementPosition.LEFT_ALIGNMENT_START_VALUE,
            top_alignment=(
                MeasUIElementPosition.TOP_ALIGNMENT_START_VALUE
                + MeasUIElementPosition.TOP_ALIGNMENT_INCREMENTAL_VALUE
            ),
            value_type=SupportedDataType.STR,
        ),
    ]
)

string_indicator_elements = create_indicator_elements(
    outputs=[
        DataElement(
            client_id=client_id,
            name="String Out",
            left_alignment=(
                MeasUIElementPosition.LEFT_ALIGNMENT_START_VALUE
                + MeasUIElementPosition.LEFT_ALIGNMENT_INCREMENTAL_VALUE
            ),
            top_alignment=MeasUIElementPosition.TOP_ALIGNMENT_START_VALUE,
            value_type=SupportedDataType.STR,
        ),
        DataElement(
            client_id=client_id,
            name="Second String Out",
            left_alignment=(
                MeasUIElementPosition.LEFT_ALIGNMENT_START_VALUE
                + MeasUIElementPosition.LEFT_ALIGNMENT_INCREMENTAL_VALUE
            ),
            top_alignment=(
                MeasUIElementPosition.TOP_ALIGNMENT_START_VALUE
                + MeasUIElementPosition.TOP_ALIGNMENT_INCREMENTAL_VALUE
            ),
            value_type=SupportedDataType.STR,
        ),
    ]
)

# Write to file.
write_measui(
    filepath="string_controls_indicators",
    input_output_elements=string_control_elements + string_indicator_elements,
)

print(string_control_elements, string_indicator_elements, sep="\n\n---------------\n\n")
print("\nMeasUI File created.")
