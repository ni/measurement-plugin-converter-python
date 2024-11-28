"""Example to create numeric control and numeric indicator measui elements.

Note: CLIENT ID should be same throughout a measui file.
"""

import uuid
from pathlib import Path

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

numeric_control_elements = create_control_elements(
    inputs=[
        DataElement(
            client_id=client_id,
            name="Numeric input",
            value_type=SupportedDataType.DOUBLE,
            left_alignment=MeasUIElementPosition.LEFT_ALIGNMENT_START_VALUE,
            top_alignment=MeasUIElementPosition.TOP_ALIGNMENT_START_VALUE,
        ),
        DataElement(
            client_id=client_id,
            name="Second Numeric input",
            value_type=SupportedDataType.UINT64,
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
            value_type=SupportedDataType.DOUBLE,
            left_alignment=(
                MeasUIElementPosition.LEFT_ALIGNMENT_START_VALUE
                + MeasUIElementPosition.LEFT_ALIGNMENT_INCREMENTAL_VALUE
            ),
            top_alignment=MeasUIElementPosition.TOP_ALIGNMENT_START_VALUE,
        ),
        DataElement(
            client_id=client_id,
            name="Second Numeric output",
            value_type=SupportedDataType.UINT64,
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

write_measui(
    filepath=Path("numeric_controls_indicators"),
    service_class="Sample Measurement",
    input_output_elements=numeric_indicator_elements + numeric_control_elements,
)

print(numeric_control_elements, numeric_indicator_elements, sep="\n\n---------------\n\n")
print("\nMeasUI File created.")
