"""Fastapp Logging
Logging configuration functionality

Author: Collin Meyer
Created: 2024-01-10 22:48
"""
import logging

from fastapp.core.settings import get_settings

settings = get_settings()


def get_logger(name: str) -> logging.Logger:
    """Get logger with correct settings

    Args:
        name (str): Name of logger

    Returns:
        logging.Logger: Configured logger
    """

    logger = logging.getLogger(name)
    logger.setLevel(logging.getLevelName(settings.log_level.upper()))

    formatter = logging.Formatter(
        "[%(asctime)s] [%(name)s] [%(levelname)s] %(message)s"
    )

    # Stderr logging
    handler = logging.StreamHandler()
    handler.setLevel(logging.getLevelName(settings.log_level.upper()))
    handler.setFormatter(formatter)

    # File logging
    file_handler = logging.FileHandler(settings.log_file)
    file_handler.setLevel(logging.getLevelName(settings.log_level.upper()))
    file_handler.setFormatter(formatter)

    logger.addHandler(handler)
    logger.addHandler(file_handler)

    return logger
