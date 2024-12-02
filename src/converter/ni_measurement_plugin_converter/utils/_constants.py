"""Constants utilized in measurement file."""
"""Constants utilized in accessing files."""

from enum import Enum

DEBUG_LOGGER = "debug_logger"

MEASUREMENT_VERSION = 1.0
MIGRATED_MEASUREMENT_FILENAME = "_migrated.py"
TEMPLATE_DIR = "templates"

ENCODING = "utf-8"

ALPHANUMERIC_PATTERN = r"[^a-zA-Z0-9]"

# Constants for Template File
MEASUREMENT_TEMPLATE = "measurement.py.mako"
MEASUREMENT_FILENAME = "measurement.py"

HELPER_TEMPLATE = "_helpers.py.mako"
HELPER_FILENAME = "_helpers.py"

SERVICE_CONFIG_TEMPLATE = "measurement.serviceconfig.mako"
SERVICE_CONFIG_FILE_EXTENSION = ".serviceconfig"

BATCH_TEMPLATE = "start.bat.mako"
BATCH_FILENAME = "start.bat"



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


# Constants for Session management
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

# User messages
"""User facing messages logged in console and log file."""

STARTING_EXECUTION = "Starting NI Measurement Plug-In Converter..."

INVALID_FILE_DIR = (
    "Invalid measurement file directory. Please provide valid measurement file directory."
)
ACCESS_DENIED = (
    "Access is denied. "
    "Please run the tool with Admin privileges or provide a different file directory."
)
FUNCTION_NOT_FOUND = (
    "Measurement function {function} not found in the file {measurement_file_dir}"
)
INVALID_DRIVERS = "Invalid/No driver used. Supported drivers: {supported_drivers}"
VALIDATE_CLI_ARGS = "Inputs validated successfully."

EXTRACT_INPUT_INFO = "Extracting inputs information from measurement function..."
EXTRACT_OUTPUT_INFO = "Extracting outputs information from measurement function..."
EXTRACT_DRIVER_SESSIONS = "Extracting driver sessions from measurement function..."

UNSUPPORTED_INPUTS = "The inputs {params} are skipped because their data types are unsupported."
UNSUPPORTED_OUTPUTS = (
    "The outputs {variables} are skipped because their data types are unsupported."
)

ADD_SESSION = "Adding sessions params..."
DEFINE_PINS_RELAYS = "Defining pins and relays..."
ADD_SESSION_MAPPING = "Adding session mapping..."
ADD_SESSION_INITIALIZATION = "Adding session initialization..."

MEASUREMENT_PLUGIN_CREATED = "Measurement plug-in is created at {plugin_dir}"

ERROR_OCCURRED = (
    "Error occurred. Please verify that the provided measurement is in the expected format."
)
LOG_FILE = "Please find the log file at {log_file_path}"
PROCESS_COMPLETED = "Process completed."


# DebugMessages
"""Debug messages logged in log file."""

VERSION = "NI Measurement Plug-In Converter - {version}"

GET_FUNCTION = "Getting function node tree..."
MIGRATED_FILE_MODIFIED = "Migrated file is modified."

MEASUI_FILE_CREATED = "Measurement UI file is created."
MEASUREMENT_FILE_CREATED = "Measurement file is created."
FILE_MIGRATED = "Migrated file is created."
BATCH_FILE_CREATED = "Batch file is created."
HELPER_FILE_CREATED = "Helper file is created."
SERVICE_CONFIG_CREATED = "Service config is created."
