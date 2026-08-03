"""
Logging configuration.
"""

import logging
from pathlib import Path

from config.settings import LOG_DIRECTORY, LOG_LEVEL


def get_logger(name: str) -> logging.Logger:
    """
    Configure and return a logger.
    """

    Path(LOG_DIRECTORY).mkdir(
        parents=True,
        exist_ok=True,
    )

    logger = logging.getLogger(name)

    if logger.handlers:
        return logger

    logger.setLevel(LOG_LEVEL)

    formatter = logging.Formatter(
        "%(asctime)s | %(levelname)s | %(name)s | %(message)s"
    )

    file_handler = logging.FileHandler(
    LOG_DIRECTORY / "application.log"
    )

    file_handler.setFormatter(formatter)

    console_handler = logging.StreamHandler()

    console_handler.setFormatter(formatter)

    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    return logger