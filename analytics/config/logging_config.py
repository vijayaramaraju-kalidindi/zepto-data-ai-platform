"""
Logging configuration for the Analytics Pipeline.
"""

from __future__ import annotations

import logging
from pathlib import Path


from config.settings import (
    LOG_DIRECTORY,
    LOG_FILE_NAME,
    LOG_LEVEL,
)


def get_logger(
    name: str,
) -> logging.Logger:
    """
    Create and configure a logger.

    Args:
        name:
            Logger name.

    Returns:
        Configured logger instance.
    """

    LOG_DIRECTORY.mkdir(
        parents=True,
        exist_ok=True,
    )

    logger = logging.getLogger(
        name,
    )

    if logger.handlers:

        return logger

    logger.setLevel(
        LOG_LEVEL,
    )

    formatter = logging.Formatter(
        (
            "%(asctime)s | "
            "%(levelname)s | "
            "%(name)s | "
            "%(message)s"
        )
    )

    log_file = (
        LOG_DIRECTORY
        / LOG_FILE_NAME
    )

    file_handler = logging.FileHandler(
        log_file,
        encoding="utf-8",
    )

    file_handler.setFormatter(
        formatter,
    )

    console_handler = logging.StreamHandler()

    console_handler.setFormatter(
        formatter,
    )

    logger.addHandler(
        file_handler,
    )

    logger.addHandler(
        console_handler,
    )

    logger.propagate = False

    return logger