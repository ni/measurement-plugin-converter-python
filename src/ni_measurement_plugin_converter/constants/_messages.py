"""Constants utilitzed in User and Debug Messages."""


class UserMessage:
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
    VALIDATE_CLI_ARGS = "Inputs validated successfully."

    EXTRACT_INPUT_INFO = "Extracting inputs information from measurement function..."
    EXTRACT_OUTPUT_INFO = "Extracting outputs information from measurement function..."

    UNSUPPORTED_INPUTS = "The inputs {params} are skipped because their data types are unsupported."
    UNSUPPORTED_OUTPUTS = (
        "The outputs {variables} are skipped because their data types are unsupported."
    )

    ADD_RESERVE_SESSION = "Adding session reservation..."
    REPLACE_SESSION_INITIALIZATION = "Replacing session initialization..."
    ASSIGN_SESSION_INFO = "Assigning session_info..."

    MEASUREMENT_PLUGIN_CREATED = "Measurement plug-in is created at {plugin_dir}"

    ERROR_OCCURRED = (
        "Error occurred. Please verify that the provided measurement is in the expected format."
    )
    PROCESS_COMPLETED = "Process completed."


class DebugMessage:
    """Debug messages logged in log file."""

    VERSION = "NI Measurement Plug-In Converter - {version}"

    GET_FUNCTION = "Getting function node tree..."
    MIGRATED_FILE_MODIFIED = "Migrated file is modified."

    MEASUREMENT_FILE_CREATED = "Measurement file is created."
    FILE_MIGRATED = "Migrated file is created."
    BATCH_FILE_CREATED = "Batch file is created."
    HELPER_FILE_CREATED = "Helper file is created."
    SERVICE_CONFIG_CREATED = "Service config is created."
