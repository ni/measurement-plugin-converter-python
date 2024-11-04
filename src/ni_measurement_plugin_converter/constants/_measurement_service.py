"""Constants utilized in measurement file."""

"""I don't think it's a good OOPS practice to create classes that just hold a bunch of constants."""

from enum import Enum


class DriverSession(Enum):
    """Instrument drivers' session."""

    nidcpower = "nims.session_management.INSTRUMENT_TYPE_NI_DCPOWER"
    nidmm = "nims.session_management.INSTRUMENT_TYPE_NI_DMM"
    nidigital = "nims.session_management.INSTRUMENT_TYPE_NI_DIGITAL_PATTERN"
    nifgen = "nims.session_management.INSTRUMENT_TYPE_NI_FGEN"
    niscope = "nims.session_management.INSTRUMENT_TYPE_NI_SCOPE"
    niswitch = "nims.session_management.INSTRUMENT_TYPE_NI_RELAY_DRIVER"
    nidaqmx = "nims.session_management.INSTRUMENT_TYPE_NI_DAQMX"


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

    SESSIONS_AND_RESOURCES = "sessions_and_resources"
    ALL_SESSIONS_INFO = "all_sessions_info"
    SESSION_VAR = "session_var"
    SESSION_VALUES = "session_values"

    NI_DRIVERS = [
        "nidcpower",
        "nidmm",
        "nidigital",
        "niscope",
        "nifgen",
        "niswitch",
        "nidaqmx",
    ]
