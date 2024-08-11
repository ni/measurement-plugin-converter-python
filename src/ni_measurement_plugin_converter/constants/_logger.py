"""Constants utilized in logger implementation."""

LOG_FILE_NAME = "log.txt"
LOG_FILE_COUNT_LIMIT = 20
LOG_FILE_SIZE_LIMIT_IN_BYTES = 10 * 1024 * 1024  # 10MB
LOG_FILE_MSG_FORMAT = "%(asctime)s [%(name)s] [%(levelname)s] %(message)s"
LOG_DATE_FORMAT = "%Y-%m-%d %H:%M:%S"

DEBUG_LOGGER = "debug_logger"
CONSOLE_LOGGER = "console_logger"
