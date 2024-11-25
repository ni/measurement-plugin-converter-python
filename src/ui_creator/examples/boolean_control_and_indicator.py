"""Example to create toggle image button and toggle image indicator measui elements.

Note: CLIENT_ID should be same throughout a measui file.
"""

import uuid

from ni_measurement_plugin_ui_creator.constants import (
    MeasUIElementPosition,
    SupportedDataType,
)
from ni_measurement_plugin_ui_creator.models import DataElement
from ni_measurement_plugin_ui_creator.utils.create_measui import write_measui
from ni_measurement_plugin_ui_creator.utils.helpers import (
    create_control_elements,
    create_indicator_elements,
)

# Refer `SupportedDataType` class for supported `value_type`.

# Any unique id will work.
client_id = uuid.uuid4()

boolean_hortizontal_sliders = create_control_elements(
    inputs=[
        DataElement(
            client_id=client_id,
            name="Bool In",
            left_alignment=MeasUIElementPosition.LEFT_ALIGNMENT_START_VALUE,
            top_alignment=MeasUIElementPosition.TOP_ALIGNMENT_START_VALUE,
            value_type=SupportedDataType.BOOL,
            height=MeasUIElementPosition.BOOLEAN_HORIZONTAL_SLIDER_HEIGHT,
            width=MeasUIElementPosition.BOOLEAN_HORIZONTAL_SLIDER_WIDTH,
        ),
        DataElement(
            client_id=client_id,
            name="Second Bool In",
            left_alignment=MeasUIElementPosition.LEFT_ALIGNMENT_START_VALUE,
            top_alignment=(
                MeasUIElementPosition.TOP_ALIGNMENT_START_VALUE
                + MeasUIElementPosition.TOP_ALIGNMENT_INCREMENTAL_VALUE
                + MeasUIElementPosition.TOP_ALIGNMENT_ADDITIONAL_INCREMENTAL_VALUE
                * MeasUIElementPosition.REDUCE_FACTOR
            ),
            value_type=SupportedDataType.BOOL,
            height=MeasUIElementPosition.BOOLEAN_HORIZONTAL_SLIDER_HEIGHT,
            width=MeasUIElementPosition.BOOLEAN_HORIZONTAL_SLIDER_WIDTH,
        ),
    ]
)

boolean_leds = create_indicator_elements(
    outputs=[
        DataElement(
            client_id=client_id,
            name="Bool Out",
            left_alignment=(
                MeasUIElementPosition.LEFT_ALIGNMENT_START_VALUE
                + MeasUIElementPosition.LEFT_ALIGNMENT_INCREMENTAL_VALUE
            ),
            top_alignment=MeasUIElementPosition.TOP_ALIGNMENT_START_VALUE,
            value_type=SupportedDataType.BOOL,
            height=MeasUIElementPosition.BOOLEAN_LED_HEIGHT,
            width=MeasUIElementPosition.BOOLEAN_LED_WIDTH,
        ),
        DataElement(
            client_id=client_id,
            name="Second Bool Out",
            left_alignment=(
                MeasUIElementPosition.LEFT_ALIGNMENT_START_VALUE
                + MeasUIElementPosition.LEFT_ALIGNMENT_INCREMENTAL_VALUE
            ),
            top_alignment=(
                MeasUIElementPosition.TOP_ALIGNMENT_START_VALUE
                + MeasUIElementPosition.TOP_ALIGNMENT_INCREMENTAL_VALUE
                + MeasUIElementPosition.TOP_ALIGNMENT_ADDITIONAL_INCREMENTAL_VALUE
                * MeasUIElementPosition.REDUCE_FACTOR
            ),
            value_type=SupportedDataType.BOOL,
            height=MeasUIElementPosition.BOOLEAN_LED_HEIGHT,
            width=MeasUIElementPosition.BOOLEAN_LED_WIDTH,
        ),
    ]
)

# Create a .measui file.
write_measui(
    filepath="boolean_elements",
    input_output_elements=boolean_hortizontal_sliders + boolean_leds,
)

print(boolean_hortizontal_sliders, boolean_leds, sep="\n\n---------------\n\n")
print("\nMeasUI File Created")
