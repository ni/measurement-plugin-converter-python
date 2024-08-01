"""Example to create string control and string indicator measui elements.

Note: CLIENT_ID should be same throughout a measui file.
"""

import uuid

from ni_measurement_ui_creator.constants._ui_elements import MeasUIElementPosition
from ni_measurement_ui_creator.models import DataElement
from ni_measurement_ui_creator.utils._create_measui import create_measui
from ni_measurement_ui_creator.utils._helpers import (
    create_control_elements,
    create_indicator_elements,
)

# Any unique id will work.
client_id = uuid.uuid4()

string_control_elements = create_control_elements(
    inputs=[
        DataElement(
            client_id=client_id,
            name="String In",
            left_alignment=MeasUIElementPosition.LEFT_START_VALUE,
            top_alignment=MeasUIElementPosition.TOP_START_VALUE,
        ),
        DataElement(
            client_id=client_id,
            name="Second String In",
            left_alignment=MeasUIElementPosition.LEFT_START_VALUE,
            top_alignment=(
                MeasUIElementPosition.TOP_START_VALUE + MeasUIElementPosition.TOP_INCREMENTAL_VALUE
            ),
        ),
    ]
)

string_indicator_elements = create_indicator_elements(
    outputs=[
        DataElement(
            client_id=client_id,
            name="String Out",
            left_alignment=(
                MeasUIElementPosition.LEFT_START_VALUE
                + MeasUIElementPosition.LEFT_INCREMENTAL_VALUE
            ),
            top_alignment=MeasUIElementPosition.TOP_START_VALUE,
        ),
        DataElement(
            client_id=client_id,
            name="Second String Out",
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
    filepath="string_controls_indicators",
    input_output_elements=string_control_elements + string_indicator_elements,
)

print(string_control_elements, string_indicator_elements, sep="\n\n---------------\n\n")
print("\nMeasUI File created.")
