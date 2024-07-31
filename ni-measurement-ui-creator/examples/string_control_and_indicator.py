"""Example to create string control and string indicator measui elements.

Note: CLIENT_ID should be same throughout a measui file.
"""

import uuid

from ni_measurement_ui_creator.models import DataElement
from ni_measurement_ui_creator.utils._string_elements import (
    create_string_controls,
    create_string_indicators,
)
from ni_measurement_ui_creator.utils._create_measui import create_measui

# Any unique id will work.
client_id = uuid.uuid4()

string_control_elements = create_string_controls(
    elements_parameter=[
        DataElement(client_id=client_id, name="String In"),
        DataElement(client_id=client_id, name="Second String In"),
    ]
)

string_indicator_elements = create_string_indicators(
    elements_parameter=[
        DataElement(client_id=client_id, name="String Out"),
        DataElement(client_id=client_id, name="Second String Out"),
    ]
)

# Create a .measui file.
create_measui(
    filepath="string_controls_indicators",
    input_output_elements=string_control_elements + string_indicator_elements,
)

print(string_control_elements, string_indicator_elements, sep="\n\n---------------\n\n")
print("\nMeasUI File created.")
