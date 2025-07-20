"""
Common Libs - Logging.

This module provides a logging configuration for the application.
"""

import inspect
import logging
import logging.config

from src.libs.log.colors import ColoredFormatter
from src.libs.log.config import LOG_FORMAT, LOG_LEVEL, LOG_NAME
from src.libs.log.filters import SensitiveDataFilter
from src.libs.log.levels import MaxLevelFilter


def setup_logging(
    level: str = LOG_LEVEL,
    output_format: str = LOG_FORMAT,
    name: str = LOG_NAME,
) -> logging.Logger:
    """
    Set up logging configuration for the application.
    """

    logging_config = {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "default": {
                "format": output_format,
                "()": ColoredFormatter,
            },
        },
        "handlers": {
            "stdout_handler": {
                "class": "logging.StreamHandler",
                "stream": "ext://sys.stdout",
                "formatter": "default",
                "filters": ["sensitive_data", "max_info_level"],
                "level": "DEBUG",
            },
            "stderr_handler": {
                "class": "logging.StreamHandler",
                "stream": "ext://sys.stderr",
                "formatter": "default",
                "filters": ["sensitive_data"],
                "level": "WARNING",
            },
        },
        "filters": {
            "sensitive_data": {
                "()": SensitiveDataFilter,
            },
            "max_info_level": {
                "()": MaxLevelFilter,
                "max_level": logging.INFO,
            },
        },
        "loggers": {
            name: {
                "level": level,
                "handlers": ["stdout_handler", "stderr_handler"],
                "propagate": False,
            },
        },
        "root": {
            "level": "WARNING",
            "handlers": [],
        },
    }

    logging.config.dictConfig(logging_config)
    return logging.getLogger(name)


def get_logger(name: str = LOG_NAME) -> logging.Logger:
    """
    Get a logger instance with the specified name.

    If the logger does not have any handlers, it will be configured with the
    default settings.
    """
    if not logging.getLogger(name).handlers:
        setup_logging()

    return logging.getLogger(name)


def get_context() -> str:
    """
    Get the context of the caller function.

    This function returns the filename and the function name of the caller
    function
    """

    filename: str = (
        inspect.currentframe()
        .f_back.f_code.co_filename.split(  # type: ignore[union-attr]
            "/",
        )[-1]
        .replace(".py", "")
    )
    function_name: str = inspect.currentframe().f_back.f_code.co_name  # type: ignore[union-attr]

    return filename + "." + function_name
