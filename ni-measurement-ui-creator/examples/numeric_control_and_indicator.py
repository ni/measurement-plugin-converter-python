"""Example to create numeric control and numeric indicator measui elements.

Note: CLIENT ID should be same throughout a measui file.
"""

import uuid

from ni_measurement_ui_creator.models import DataElement
from ni_measurement_ui_creator.utils._create_measui import create_measui
from ni_measurement_ui_creator.utils._numeric_elements import (
    create_numeric_controls,
    create_numeric_indicators,
)


# Refer `SupportedDataType` Enum for supported `value_type`.
# Use corresponding key strings according to the needs.

# Any unique id will work.
client_id = uuid.uuid4()

numeric_control_elements = create_numeric_controls(
    elements_parameter=[
        DataElement(
            client_id=client_id,
            name="Numeric input",
            value_type="Double",  # Refer `SupportedDataType`.
        ),
        DataElement(
            client_id=client_id,
            name="Second Numeric input",
            value_type="UInt64",  # Refer `SupportedDataType`.
        ),
    ]
)


numeric_indicator_elements = create_numeric_indicators(
    elements_parameter=[
        DataElement(
            client_id=client_id,
            name="Numeric output",
            value_type="Double",  # Refer `SupportedDataType`.
        ),
        DataElement(
            client_id=client_id,
            name="Second Numeric output",
            value_type="UInt64",  # Refer `SupportedDataType`.
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
