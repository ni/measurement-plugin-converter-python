"""Constants utilized in Command Line Interface implementation."""

CONTEXT_SETTINGS = {"help_option_names": ["-h", "--help"]}

"""I don't think it's a good OOPS practice to create classes that just hold a bunch of constants."""

class ArgsDescription:
    """Command line interface arguments' description."""

    DISPLAY_NAME = "Display name."
    MEASUREMENT_FILE_DIR = "Measurement file directory."
    FUNCTION = "Measurement function name."
    OUTPUT_DIR = "Output directory."
