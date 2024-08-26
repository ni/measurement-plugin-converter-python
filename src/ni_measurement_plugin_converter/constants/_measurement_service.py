"""Constants utilized in measurement file."""

# Python native data types and its corresponding `measurement_plugin_sdk_service` data types.
NIMS_TYPE = {
    "int": "nims.DataType.Int64",
    "float": "nims.DataType.Double",
    "str": "nims.DataType.String",
    "bool": "nims.DataType.Boolean",
    "List[int]": "nims.DataType.Int64Array1D",
    "List[float]": "nims.DataType.DoubleArray1D",
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


class SessionManagement:
    """Constants used in session management."""

    RESERVATION = "reservation"
    SESSION_INFO = "session_info"

    SESSION_CONSTRUCTOR = "session_constructor"
    INSTRUMENT_TYPE = "instrument_type"

    NI_DRIVERS = [
        "nidcpower",
        "nidmm",
        "nidigital",
        "niscope",
        "nifgen",
        "niswitch",
        "nidaqmx",
    ]
