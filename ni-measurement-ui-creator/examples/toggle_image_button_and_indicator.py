"""Example to create toggle image button and toggle image indicator measui elements.

Note: CLIENT_ID should be same throughout a measui file.
"""

import uuid

from ni_measurement_ui_creator.models import DataElement
from ni_measurement_ui_creator.utils._create_measui import create_measui
from ni_measurement_ui_creator.utils._toggle_elements import (
    create_toggle_image_buttons,
    create_toggle_image_indicators,
)


# Any unique id will work.
client_id = uuid.uuid4()

toggle_image_buttons = create_toggle_image_buttons(
    elements_parameter=[
        DataElement(client_id=client_id, name="Bool In"),
        DataElement(client_id=client_id, name="Second Bool In"),
    ]
)

toggle_image_indicators = create_toggle_image_indicators(
    elements_parameter=[
        DataElement(client_id=client_id, name="Bool Out"),
        DataElement(client_id=client_id, name="Second Bool Out"),
    ]
)

# Create a .measui file.
create_measui(
    filepath="toggle_image_buttons_indicators",
    input_output_elements=toggle_image_buttons + toggle_image_indicators,
)

print(toggle_image_buttons, toggle_image_indicators, sep="\n\n---------------\n\n")
print("\nMeasUI File Created")
