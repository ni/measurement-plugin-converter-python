"""Logger implementation."""

import logging
from logging import Logger
from pathlib import Path

from ni_measurement_plugin_ui_creator.constants import LOGGER


def get_logger(log_file_path: Path) -> Logger:
    """Get logger object.

    Args:
        log_file_path (Path): Log file path.

    Returns:
        Logger: Logger object.
    """
    Path(log_file_path).mkdir(parents=True, exist_ok=True)
    log_file_path = log_file_path / "log.txt"

    logger = logging.getLogger(LOGGER)
    logger.setLevel(logging.DEBUG)

    add_file_handler(log_file_path=log_file_path)
    add_stream_handler()

    return logger


def add_file_handler(log_file_path: Path) -> None:
    """Add file handler to logger object.

    Args:
        log_file_path (Path): log file path.
    """
    logger = logging.getLogger(LOGGER)
    formatter = logging.Formatter("%(asctime)s | %(message)s", datefmt="%Y-%m-%d %H:%M:%S")

    file_handler = logging.FileHandler(log_file_path, mode="a")
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(formatter)

    logger.addHandler(file_handler)


def add_stream_handler() -> None:
    """Add stream handler to logger object."""
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)

    logger = logging.getLogger(LOGGER)
    logger.addHandler(console_handler)
