"""Implementation of logger."""

import logging
import sys
from logging import Logger, StreamHandler, handlers
from pathlib import Path
from typing import Optional

from ni_measurement_plugin_converter._constants import DEBUG_LOGGER

LOG_FILE_NAME = "log.txt"
LOG_FILE_COUNT_LIMIT = 20
LOG_FILE_SIZE_LIMIT_IN_BYTES = 10 * 1024 * 1024  # 10MB
LOG_FILE_MSG_FORMAT = "%(asctime)s [%(name)s] [%(levelname)s] %(message)s"
LOG_DATE_FORMAT = "%Y-%m-%d %H:%M:%S"
LOG_FILE = "Please find the log file at {log_file_path}"


def _add_file_handler(logger: Logger, log_directory: str) -> None:
    handler = _create_file_handler(log_directory=log_directory, file_name=LOG_FILE_NAME)
    logger.addHandler(handler)


def _create_file_handler(log_directory: str, file_name: str) -> handlers.RotatingFileHandler:
    log_file = Path(log_directory) / file_name

    handler = handlers.RotatingFileHandler(
        str(log_file),
        maxBytes=LOG_FILE_SIZE_LIMIT_IN_BYTES,
        backupCount=LOG_FILE_COUNT_LIMIT,
    )
    handler.setLevel(logging.DEBUG)

    formatter = logging.Formatter(LOG_FILE_MSG_FORMAT, datefmt=LOG_DATE_FORMAT)
    handler.setFormatter(formatter)

    return handler


def _add_stream_handler(logger: Logger) -> None:
    stream_handler = _create_stream_handler()
    logger.addHandler(stream_handler)


def _create_stream_handler() -> StreamHandler:
    handler = logging.StreamHandler(sys.stdout)
    handler.setLevel(logging.INFO)
    return handler


def remove_handlers(logger: Logger) -> None:
    """Remove all handlers from the specified logger.

    Args:
        logger: The logger instance from which handlers will be removed.
    """
    for handler in logger.handlers:
        logger.removeHandler(handler)


def print_log_file_location() -> None:
    """Print the location of the log file if it is available."""
    logger = logging.getLogger(DEBUG_LOGGER)

    for handler in logger.handlers:
        if isinstance(handler, handlers.RotatingFileHandler):
            logger.info(LOG_FILE.format(log_file_path=handler.baseFilename))


def initialize_logger(name: str, log_directory: Optional[str]) -> Logger:
    """Initialize and configure a logger instance.

    Args:
        name: The name of the logger.
        log_directory: The directory where log files should be stored.

    Returns:
        The configured logger instance.
    """
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)

    if log_directory:
        _add_file_handler(logger, log_directory)

    _add_stream_handler(logger)
    return logger
