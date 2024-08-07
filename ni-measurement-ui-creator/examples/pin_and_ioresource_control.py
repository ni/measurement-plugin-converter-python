"""Example to create Pin control  and IOResource element.

Note: CLIENT_ID should be same throughout a measui file.
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
)


# Refer `SupportedDataType` class for supported `value_type`.
# Use corresponding key strings according to the needs.

# Any unique id will work.
client_id = uuid.uuid4()

pin_control_elements = create_control_elements(
    inputs=[
        DataElement(
            client_id=client_id,
            name="Pin1",
            left_alignment=MeasUIElementPosition.LEFT_ALIGNMENT_START_VALUE,
            top_alignment=MeasUIElementPosition.TOP_ALIGNMENT_START_VALUE,
            value_type=SupportedDataType.PIN,  # Refer `SupportedDataType`
        ),
        DataElement(
            client_id=client_id,
            name="Pin2",
            left_alignment=MeasUIElementPosition.LEFT_ALIGNMENT_START_VALUE,
            top_alignment=(
                MeasUIElementPosition.TOP_ALIGNMENT_START_VALUE
                + MeasUIElementPosition.TOP_ALIGNMENT_INCREMENTAL_VALUE
            ),
            value_type=SupportedDataType.PIN,  # Refer `SupportedDataType`
        ),
    ]
)

ioresource_control_elements = create_control_elements(
    inputs=[
        DataElement(
            client_id=client_id,
            name="PinGroup1",
            left_alignment=(
                MeasUIElementPosition.LEFT_ALIGNMENT_START_VALUE
                + MeasUIElementPosition.LEFT_ALIGNMENT_INCREMENTAL_VALUE
            ),
            top_alignment=MeasUIElementPosition.TOP_ALIGNMENT_START_VALUE,
            value_type=SupportedDataType.IORESOURCE,  # Refer `SupportedDataType`
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
            value_type=SupportedDataType.IORESOURCE,  # Refer `SupportedDataType`
        ),
    ]
)

# Create a .measui file.
create_measui(
    filepath="Pin_and_Ioresource_control_element",
    input_output_elements=pin_control_elements + ioresource_control_elements,
)

print(pin_control_elements, sep="\n\n---------------\n\n")
print("\nMeasUI File created.")
