"""Constants reused across files."""

DEBUG_LOGGER = "debug_logger"
ENCODING = "utf-8"
ALPHANUMERIC_PATTERN = r"[^a-zA-Z0-9]"
RESERVATION = "reservation"
NI_DRIVERS = [
    "nidcpower",
    "nidmm",
    "nidigital",
    "niscope",
    "nifgen",
    "niswitch",
    "nidaqmx",
]
ACCESS_DENIED = (
    "Access is denied. "
    "Please run the tool with Admin privileges or provide a different file directory."
)
ADD_SESSION = "Adding sessions params..."
