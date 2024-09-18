"""CLI input and user messages."""

CLI_CONTEXT_SETTINGS = {"help_option_names": ["-h", "--help"]}


class CliHelpMessage:
    """CLI help messages for arguments."""

    OUTPUT_FOLDER = "Output directory path where the .measui file is created."


class UserMessage:
    """Messages displayed."""

    CLI_STARTING = "Starting the NI Measurement UI Creator..."
    SUPPORTED_ELEMENTS = "Supported UI Elements: {elements}"

    GET_ACTIVE_MEASUREMENTS = "Getting the active measurements..."
    NO_MEASUREMENTS_RUNNING = "No measurement services are running."

    AVAILABLE_MEASUREMENTS = "Available services:"
    AVAILABLE_MEASUI_FILES = "Available Measurement UI Files:"

    INVALID_MEASUREMENT_CHOICE = "Invalid measurement plug-in selected."
    INVALID_MEASUI_CHOICE = "Invalid measurement UI selected."

    NO_MEASUI_FILE = "No measurement UI file available. Creating a new measui file for the selected measurement..."

    SELECT_MEASUREMENT = (
        "Select a measurement service index ({start}-{end}) to generate measui file: "
    )

    SELECT_MEASUI_FILE = "Select a measurement UI file index ({start}-{end}) to update: "

    INVALID_MEASUI_FILE = (
        "Invalid measurement UI file. Creating a new measui file for the selected measurement..."
    )

    CREATED_UI = "Measurement UI created successfully at {filepath}"
    CREATING_FILE = "Creating Measurement UI..."

    RENDER_TEMPLATE_ERROR = "Error occurred while rendering measui template."

    ERROR_OCCURRED = "Error occurred. Please find the log file at {log_file}"
    ABORTED = "Aborted!"
    PROCESS_COMPLETED = "Process completed."
