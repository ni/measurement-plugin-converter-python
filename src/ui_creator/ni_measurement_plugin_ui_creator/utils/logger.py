"""Logger implementation."""

import logging
from logging import Logger
from pathlib import Path

from ni_measurement_plugin_ui_creator.constants import LOGGER


def get_logger(log_file_path: Path) -> Logger:
    """Get logger object.

    Args:
        log_file_path: Log file path.

    Returns:
        Logger object.
    """
    Path(log_file_path).mkdir(parents=True, exist_ok=True)
    log_file_path = log_file_path / "log.txt"

    logger = logging.getLogger(LOGGER)
    logger.setLevel(logging.DEBUG)

    _add_file_handler(log_file_path=log_file_path)
    _add_stream_handler()

    return logger


def _add_file_handler(log_file_path: Path) -> None:
    logger = logging.getLogger(LOGGER)
    formatter = logging.Formatter("%(asctime)s | %(message)s", datefmt="%Y-%m-%d %H:%M:%S")

    file_handler = logging.FileHandler(log_file_path, mode="a")
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(formatter)

    logger.addHandler(file_handler)


def _add_stream_handler() -> None:
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)

    logger = logging.getLogger(LOGGER)
    logger.addHandler(console_handler)
