"""A module to initialize logger functions."""

import logging
import logging.handlers
import os
import sys
from logging import Logger
from pathlib import Path

from ni_measurement_converter.constants.logger import (
    LOG_DATE_FORMAT,
    LOG_FILE_COUNT_LIMIT,
    LOG_FILE_MSG_FORMAT,
    LOG_FILE_NAME,
    LOG_FILE_SIZE_LIMIT_IN_BYTES,
)


def __create_file_handler(
    log_folder_path: str,
    file_name: str,
) -> logging.handlers.RotatingFileHandler:
    log_file = os.path.join(log_folder_path, file_name)
    folder_path_obj = Path(log_folder_path)

    if not folder_path_obj.exists():
        folder_path_obj.mkdir(parents=True)

    handler = logging.handlers.RotatingFileHandler(
        log_file,
        maxBytes=LOG_FILE_SIZE_LIMIT_IN_BYTES,
        backupCount=LOG_FILE_COUNT_LIMIT,
    )
    handler.setLevel(logging.DEBUG)

    formatter = logging.Formatter(LOG_FILE_MSG_FORMAT, datefmt=LOG_DATE_FORMAT)
    handler.setFormatter(formatter)

    return handler


def __create_stream_handler():
    handler = logging.StreamHandler(sys.stdout)
    handler.setLevel(logging.INFO)

    return handler


def initialize_logger(name: str) -> Logger:
    """Initialize logger object for logging.

    Args:
        name (str): Logger name.

    Returns:
        Logger: Logger object.
    """
    new_logger = logging.getLogger(name)
    new_logger.setLevel(logging.DEBUG)

    return new_logger


def add_stream_handler(logger: Logger) -> None:
    """Add stream handler.

    Args:
        logger (Logger): Logger object.

    Returns:
        None.
    """
    stream_handler = __create_stream_handler()
    logger.addHandler(stream_handler)


def add_file_handler(logger: Logger, log_folder_path: str) -> None:
    """Add file handler.

    Args:
        logger (Logger): Logger object.
        log_folder_path (str): Log folder path.

    Returns:
        None.
    """
    handler = __create_file_handler(log_folder_path=log_folder_path, file_name=LOG_FILE_NAME)
    logger.addHandler(handler)


def remove_handlers(log: Logger) -> None:
    """Remove Log Handlers.

    Args:
        logger (Logger): Logger object.

    Returns:
        None.
    """
    for handler in log.handlers:
        log.removeHandler(handler)