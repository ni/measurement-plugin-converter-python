"""CLI input and user messages."""

CLI_CONTEXT_SETTINGS = {"help_option_names": ["-h", "--help"]}


class CliHelpMessage:
    """CLI help messages for arguments."""

    OUTPUT_FOLDER = "Output directory path where the .measui file is created."


class UserMessage:
    """Messages displayed."""

    STARTING = "Starting the NI Measurement UI Creator..."
    SUPPORTED_ELEMENTS = "Supported UI Elements: {elements}"

    GET_MEASUREMENTS_RUNNING = "Getting the measurements running..."
    NO_MEASUREMENTS_RUNNING = "No measurement services are running."
    AVAILABLE_MEASUREMENTS = "Available services:"

    INVALID_MEASUREMENT_CHOICE = "Invalid measurement plug-in selected."
    SELECT_MEASUREMENT = "Select Measurement Service index ({start}-{end}) to run\
 [Press Enter to exit]: "

    CREATED_UI = "Measurement UI created successfully at {filepath}"
    CREATING_FILE = "Creating Measurement UI..."

    RENDER_TEMPLATE_ERROR = "Error occurred while rendering measui template."

    ERROR_OCCURRED = "Error occurred. Please find more details in log file."
    ABORTED = "Aborted!"
    PROCESS_COMPLETED = "Process completed."
