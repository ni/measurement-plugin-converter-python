"""Example to create numeric array input and numeric array output measui elements.

Note: CLIENT ID should be same throughout a measui file.
"""

import uuid

from ni_measurement_ui_creator.models import DataElement
from ni_measurement_ui_creator.utils._numeric_elements import (
    create_numeric_array_inputs,
    create_numeric_array_outputs,
)
from ni_measurement_ui_creator.utils._write_xml import write_to_xml


# Refer `SupportedDataType` Enum for supported `value_type`.
# Use corresponding key strings according to the needs.

# Any unique id will work.
client_id = uuid.uuid4()

array_input_elements = create_numeric_array_inputs(
    elements_parameter=[
        DataElement(
            client_id=client_id,
            name="Array In",
            value_type="Double",  # Refer `SupportedDataType`.
        ),
        DataElement(
            client_id=client_id,
            name="Second Array In",
            value_type="UInt32",  # Refer `SupportedDataType`.
        ),
    ]
)

array_output_elements = create_numeric_array_outputs(
    elements_parameter=[
        DataElement(
            client_id=client_id,
            name="Array Out",
            value_type="Double",  # Refer `SupportedDataType`.
        ),
        DataElement(
            client_id=client_id,
            name="Second Array Out",
            value_type="UInt32",  # Refer `SupportedDataType`.
        ),
    ]
)

# Create a .measui file.
write_to_xml(
    filepath="numeric_arrays",
    input_output_elements=array_input_elements + array_output_elements,
)

print(array_input_elements, array_output_elements, sep="\n\n---------------\n\n")
print("\nMeasUI File created.")
