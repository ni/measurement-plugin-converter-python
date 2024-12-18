"""Example to create Pin control and IOResource element.

Note: CLIENT_ID should be same throughout a measui file.
"""

import uuid
from pathlib import Path

from ni_measurement_plugin_ui_creator.constants import MeasUIElementPosition, SupportedDataType
from ni_measurement_plugin_ui_creator.models import DataElement
from ni_measurement_plugin_ui_creator.utils.create_measui import write_measui
from ni_measurement_plugin_ui_creator.utils.helpers import create_control_elements

# Refer `SupportedDataType` class for supported `value_type`.

# Any unique id will work.
client_id = uuid.uuid4()

pin_control_elements = create_control_elements(
    inputs=[
        DataElement(
            client_id=client_id,
            name="Pin1",
            left_alignment=MeasUIElementPosition.LEFT_ALIGNMENT_START_VALUE,
            top_alignment=MeasUIElementPosition.TOP_ALIGNMENT_START_VALUE,
            value_type=SupportedDataType.PIN,
        ),
        DataElement(
            client_id=client_id,
            name="Pin2",
            left_alignment=MeasUIElementPosition.LEFT_ALIGNMENT_START_VALUE,
            top_alignment=(
                MeasUIElementPosition.TOP_ALIGNMENT_START_VALUE
                + MeasUIElementPosition.TOP_ALIGNMENT_INCREMENTAL_VALUE
            ),
            value_type=SupportedDataType.IORESOURCE,  # Both IOResource and Pin data type will create Pin Control only.
        ),
    ]
)

ioresource_arr_control_elements = create_control_elements(
    inputs=[
        DataElement(
            client_id=client_id,
            name="PinGroup1",
            left_alignment=(
                MeasUIElementPosition.LEFT_ALIGNMENT_START_VALUE
                + MeasUIElementPosition.LEFT_ALIGNMENT_INCREMENTAL_VALUE
            ),
            top_alignment=MeasUIElementPosition.TOP_ALIGNMENT_START_VALUE,
            value_type=SupportedDataType.IORESOURCE_ARR,
        ),
        DataElement(
            client_id=client_id,
            name="PinGroup2",
            left_alignment=(
                MeasUIElementPosition.LEFT_ALIGNMENT_START_VALUE
                + MeasUIElementPosition.LEFT_ALIGNMENT_INCREMENTAL_VALUE
            ),
            top_alignment=(
                MeasUIElementPosition.TOP_ALIGNMENT_START_VALUE
                + MeasUIElementPosition.TOP_ALIGNMENT_INCREMENTAL_VALUE
            ),
            value_type=SupportedDataType.IORESOURCE_ARR,
        ),
    ]
)

write_measui(
    filepath=Path("pin_and_IOResource_control_element"),
    service_class="Sample Measurement",
    input_output_elements=pin_control_elements + ioresource_arr_control_elements,
)

print(pin_control_elements, ioresource_arr_control_elements, sep="\n\n---------------\n\n")
print("\nMeasUI File created.")
