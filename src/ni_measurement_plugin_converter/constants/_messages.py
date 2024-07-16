"""Constants utilitzed in User and Debug Messages."""


class UserMessage:
    """User facing messages logged in console and log file."""

    STARTING_EXECUTION = "Starting NI Measurement Plugin Converter..."
    INVALID_FILE_DIR = (
        "Invalid measurement file directory. Please provide valid measurement file directory."
    )
    ACCESS_DENIED = (
        "Access is denied. "
        "Please run the tool with Admin privileges or provide a different file directory."
    )

    VALIDATE_CLI_ARGS = "Inputs validated successfully."
    FUNCTION_NOT_FOUND = "Function {function} not found in file {measurement_file_dir}"

    EXTRACT_INPUT_INFO = "Extracting inputs information from measurement function..."
    EXTRACT_OUTPUT_INFO = "Extracting outputs information from measurement function..."

    ADD_RESERVE_SESSION = "Adding session reservation.."
    ADD_SESSION_INITIALIZATION = "Adding session initialization..."

    MEASUREMENT_PLUGIN_CREATED = "Measurement plugin is created at {plugin_dir}"

    ERROR_OCCURRED = "Error occurred."
    PROCESS_COMPLETED = "Process completed."


class DebugMessage:
    """Debug messages logged in log file."""

    VERSION = "NI Measurement Plugin Converter - {version}"
    FILE_MIGRATED = "File migrated successfully."
    GET_FUNCTION = "Getting function node tree..."

    FILE_MIGRATED = "Migrated file is created."
    BATCH_FILE_CREATED = "Batch file is created."
    HELPER_FILE_CREATED = "Helper file is created."
    MEASUREMENT_FILE_CREATED = "Measurement file is created."
    SERVICE_CONFIG_CREATED = "Service config is created."
