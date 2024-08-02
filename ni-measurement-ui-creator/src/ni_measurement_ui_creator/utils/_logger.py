"""Logger implementation."""

import logging
import os
from logging import Logger


def add_stream_handler(logger: Logger) -> None:
    """Add stream handler to logger object.

    Args:
        logger (Logger): Logger object.

    Returns:
        None.
    """
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)

    logger.addHandler(console_handler)


def add_file_handler(logger: Logger, log_file_path: str) -> None:
    """Add file handler to logger object.

    Args:
        logger (Logger): Logger object.
        log_file_path (str): log file path.

    Returns:
        None
    """
    formatter = logging.Formatter("%(asctime)s | %(message)s", datefmt="%Y-%m-%d %H:%M:%S")

    file_handler = logging.FileHandler(log_file_path, mode="a")
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(formatter)

    logger.addHandler(file_handler)


def get_logger(log_file_path: str) -> Logger:
    """Get logger object.

    Args:
        log_file_path (str): Log file path.

    Returns:
        Logger: Logger object.
    """
    os.makedirs(log_file_path, exist_ok=True)
    log_file = os.path.join(log_file_path, "log.txt")

    logger = logging.getLogger("logger")
    logger.setLevel(logging.DEBUG)

    add_file_handler(logger=logger, log_file_path=log_file)
    add_stream_handler(logger=logger)

    return logger
