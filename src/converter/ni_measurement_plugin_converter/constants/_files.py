"""Constants utilized in accessing files."""

MEASUREMENT_VERSION = 1.0
MIGRATED_MEASUREMENT_FILENAME = "_migrated.py"
TEMPLATE_DIR = "templates"

ENCODING = "utf-8"

ALPHANUMERIC_PATTERN = r"[^a-zA-Z0-9]"


class TemplateFile:
    """Template file."""

    MEASUREMENT_TEMPLATE = "measurement.py.mako"
    MEASUREMENT_FILENAME = "measurement.py"

    HELPER_TEMPLATE = "_helpers.py.mako"
    HELPER_FILENAME = "_helpers.py"

    SERVICE_CONFIG_TEMPLATE = "measurement.serviceconfig.mako"
    SERVICE_CONFIG_FILE_EXTENSION = ".serviceconfig"

    BATCH_TEMPLATE = "start.bat.mako"
    BATCH_FILENAME = "start.bat"
