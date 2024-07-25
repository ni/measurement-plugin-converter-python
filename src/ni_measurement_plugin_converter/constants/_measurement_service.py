"""Constants utilized in measurement file."""

from enum import Enum


class DriverSession(Enum):
    """Instrument drivers' session."""

    nidcpower = "nims.session_management.INSTRUMENT_TYPE_NI_DCPOWER"
    nidmm = "nims.session_management.INSTRUMENT_TYPE_NI_DMM"


# Python native data types and its corresponding `measurement_plugin_sdk_service` data types.
NIMS_TYPE = {
    "int": "nims.DataType.Int64",
    "float": "nims.DataType.Float",
    "str": "nims.DataType.String",
    "bool": "nims.DataType.Boolean",
    "List[int]": "nims.DataType.Int64Array1D",
    "List[float]": "nims.DataType.FloatArray1D",
    "List[str]": "nims.DataType.StringArray1D",
    "List[bool]": "nims.DataType.BooleanArray1D",
}

# Default values for datatypes.
TYPE_DEFAULT_VALUES = {
    "int": 1,
    "float": 1.1,
    "str": "",
    "bool": True,
    "List[int]": [1],
    "List[float]": [1.1],
    "List[str]": [""],
    "List[bool]": [True],
}
