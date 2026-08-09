"""
Logging configuration.

Provides a centralized logger
configuration for the Support
Assistant module.
"""

from __future__ import annotations

import logging

from logging.handlers import (
    RotatingFileHandler,
)

from config.settings import (
    LOGS_DIRECTORY,
)

# Create log directory
LOGS_DIRECTORY.mkdir(
    parents=True,
    exist_ok=True,
)

LOG_FILE = (
    LOGS_DIRECTORY
    / "support_assistant.log"
)

LOG_FORMAT = (
    "%(asctime)s | "
    "%(levelname)s | "
    "%(name)s | "
    "%(message)s"
)


def get_logger(
    name: str,
) -> logging.Logger:
    """
    Create and return a configured
    logger instance.

    Parameters
    ----------
    name : str
        Logger name.

    Returns
    -------
    logging.Logger
    """

    logger = logging.getLogger(
        name,
    )

    if logger.handlers:
        return logger

    logger.setLevel(
        logging.INFO,
    )

    formatter = logging.Formatter(
        LOG_FORMAT,
    )

    console_handler = logging.StreamHandler()

    console_handler.setFormatter(
        formatter,
    )

    file_handler = RotatingFileHandler(
        LOG_FILE,
        maxBytes=5 * 1024 * 1024,
        backupCount=5,
        encoding="utf-8",
    )

    file_handler.setFormatter(
        formatter,
    )

    logger.addHandler(
        console_handler,
    )

    logger.addHandler(
        file_handler,
    )

    logger.propagate = False

    return logger
