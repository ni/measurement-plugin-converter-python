"""CLI input and user messages."""

CLI_CONTEXT_SETTINGS = {"help_option_names": ["-h", "--help"]}


class UserMessage:
    """Messages displayed."""

    CLI_STARTING = "Starting the NI Measurement UI Creator..."
    SUPPORTED_ELEMENTS = "Supported UI Elements: {elements}"

    GET_ACTIVE_MEASUREMENTS = "Getting the active measurements..."
    NO_MEASUREMENTS_RUNNING = "No measurement services are running."

    AVAILABLE_MEASUREMENTS = "Available services:"
    AVAILABLE_MEASUI_FILES = "Available Measurement UI Files:"

    SELECT_MEASUREMENT = (
        "Select a measurement service index ({start}-{end}) to update/generate measui file: "
    )
    SELECT_MEASUI_FILE = "Select a measurement UI file index ({start}-{end}) to update: "

    INVALID_MEASUREMENT_CHOICE = "Invalid measurement plug-in selected."
    INVALID_MEASUI_CHOICE = "Invalid measurement UI selected."

    NO_MEASUI_FILE = (
        "No Measurement UI file available. "
        "Creating a new measui file for the selected measurement..."
    )
    INVALID_MEASUI_FILE = (
        "Invalid Measurement UI file. Creating a new measui file for the selected measurement..."
    )

    BINDING_ELEMENTS = "Binding UI controls and indicators..."
    INPUTS_BOUND = "Inputs are bound successfully."
    OUTPUTS_BOUND = "Outputs are bound successfully."

    CREATING_ELEMENTS = "Creating new controls and indicators..."
    CREATING_FILE = "Creating Measurement UI..."
    CREATED_UI = "Measurement UI created successfully at {filepath}"
    UPDATED_UI = "Measurement UI updated successfully. Please find at {filepath}"

    RENDER_TEMPLATE_ERROR = "Error occurred while rendering measui template."
    ERROR_OCCURRED = "Error occurred. Please find the log file at {log_file}"

    PROCESS_COMPLETED = "Process completed."
