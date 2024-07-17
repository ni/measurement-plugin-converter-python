"""Constants utilized in accessing template files."""

MEASUREMENT_VERSION = 1.0
MIGRATED_MEASUREMENT_FILENAME = "_migrated.py"
TEMPLATE_DIR = "templates"

class TemplateFile:
    """Template file names."""

    MEASUREMENT_TEMPLATE = "measurement.py.mako"
    MEASUREMENT_FILENAME = "measurement.py"

    HELPER_TEMPLATE = "_helpers.py.mako"
    HELPER_FILENAME = "_helpers.py"

    SERVICE_CONFIG_TEMPLATE = "measurement.serviceconfig.mako"
    SERVICE_CONFIG_FILENAME = "measurement.serviceconfig"

    BATCH_TEMPLATE = "start.bat.mako"
    BATCH_FILENAME = "start.bat"

    ENCODING = "utf-8"
