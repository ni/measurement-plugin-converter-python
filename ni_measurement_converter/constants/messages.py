"""NI Measurement Plugin Package Builder status messages."""


class UserMessages:
    """User facing console messages."""

    STARTED_EXECUTION = "Starting the NI Measurement Plugin Converter..."
    CHECK_LOG_FILE = "Error occurred. Please check the log file for further details."
    LOG_FILE_LOCATION = "Log File Directory: {log_dir}"
    PROCESS_COMPLETED = "Process Completed."
    VERSION = "Package Version - {version}"
    ACCESS_DENIED = "Access is denied.\
 Please run the tool with Admin privileges or provide a different file directory."
    EXTRACT_INPUTS = "Extracting inputs..."
    EXTRACT_OUTPUTS = "Extracting outputs..."
    INVALID_FILE_DIR = "Invalid measurement file directory."
    TEMPLATE_ERROR = "An error occurred while rendering template."
    FILE_MIGRATED = "Migrated file is created."
    BATCH_FILE_CREATED = "Batch file is created."
    HELPER_FILE_CREATED = "Helper file is created."
    MEASUREMENT_FILE_CREATED = "Measurement file is created."
    SERVICE_CONFIG_CREATED = "Service config is created."
    MEASUREMENT_PLUGIN_CREATED = "Measurement plugin is created. Please find at {file_dir}"
