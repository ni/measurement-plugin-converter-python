"""NI Measurement Plugin Package Builder status messages."""


class UserMessages:
    """User Facing console messages."""

    STARTED_EXECUTION = "Starting the NI Measurement Plugin Converter..."
    CHECK_LOG_FILE = "Error occurred. Please check the log file for further details."
    LOG_FILE_LOCATION = "Log File Directory: {log_dir}"
    PROCESS_COMPLETED = "Process Completed."
    VERSION = "Package Version - {version}"
    ACCESS_DENIED = "Access is denied.\
 Please run the tool with Admin privileges or provide a different output directory."
    EXTRACT_INPUTS = "Extracting inputs..."
    EXTRACT_OUTPUTS = "Extracting outputs..."
    INVALID_FILE_DIR = "Invalid measurement file directory."
    TEMPLATE_ERROR = "An error occurred while rendering template '{template_name}'."
