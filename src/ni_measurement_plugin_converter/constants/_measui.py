"""Constants utilized in the .measui file creation."""

import ni_measurement_plugin_sdk_service as nims

SUPPORTED_NIMS_DATATYPES = [
    nims.DataType.Int64.name,
    nims.DataType.Double.name,
    nims.DataType.String.name,
    nims.DataType.Boolean.name,
    nims.DataType.Int64Array1D.name,
    nims.DataType.DoubleArray1D.name,
]
