"""Constants utilized in the .measui file creation."""

import ni_measurement_plugin_sdk_service as nims


PIN_NAMES = "pin_names"
SUPPORTED_NIMS_DATATYPES = [
    nims.DataType.Int64.name,
    nims.DataType.Float.name,
    nims.DataType.String.name,
    nims.DataType.Boolean.name,
    nims.DataType.Int64Array1D.name,
    nims.DataType.FloatArray1D.name,
]
