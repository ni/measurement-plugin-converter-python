"""Implementation of logger."""

import logging
import os
import sys
from logging import Logger, StreamHandler, handlers

from ni_measurement_plugin_converter.constants import (
    LOG_DATE_FORMAT,
    LOG_FILE_COUNT_LIMIT,
    LOG_FILE_MSG_FORMAT,
    LOG_FILE_NAME,
    LOG_FILE_SIZE_LIMIT_IN_BYTES,
)


def initialize_logger(name: str, log_directory: str) -> Logger:
    """Initialize logger object.

    Args:
        name (str): Logger name.
        log_directory (str): Log directory.

    Returns:
        Logger: Logger object.
    """
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)

    if log_directory:
        add_file_handler(logger, log_directory)

    add_stream_handler(logger=logger)

    return logger


def add_file_handler(logger: Logger, log_directory: str) -> None:
    """Add file handler.

    Args:
        logger (Logger): Logger object.
        log_directory (str): Log directory.
    """
    handler = __create_file_handler(log_directory=log_directory, file_name=LOG_FILE_NAME)
    logger.addHandler(handler)


def __create_file_handler(log_directory: str, file_name: str) -> handlers.RotatingFileHandler:
    log_file = os.path.join(log_directory, file_name)

    handler = handlers.RotatingFileHandler(
        log_file,
        maxBytes=LOG_FILE_SIZE_LIMIT_IN_BYTES,
        backupCount=LOG_FILE_COUNT_LIMIT,
    )
    handler.setLevel(logging.DEBUG)

    formatter = logging.Formatter(LOG_FILE_MSG_FORMAT, datefmt=LOG_DATE_FORMAT)
    handler.setFormatter(formatter)

    return handler


def add_stream_handler(logger: Logger) -> None:
    """Add stream handler.

    Args:
        logger (Logger): Logger object.
    """
    stream_handler = __create_stream_handler()
    logger.addHandler(stream_handler)


def __create_stream_handler() -> StreamHandler:
    handler = logging.StreamHandler(sys.stdout)
    handler.setLevel(logging.INFO)

    return handler


def remove_handlers(logger: Logger) -> None:
    """Remove Log Handlers.

    Args:
        logger (Logger): Logger object.
    """
    for handler in logger.handlers:
        logger.removeHandler(handler)
