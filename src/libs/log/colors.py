"""
Logger - Colors.

This module provides a colored formatter for the application's logging configuration.
"""

import logging
from typing import ClassVar

from colorama import Fore, Style


class ColoredFormatter(logging.Formatter):
    """
    A colored formatter for the application's logging configuration.
    """

    COLORS: ClassVar = {
        "DEBUG": Fore.WHITE,
        "INFO": Fore.BLUE,
        "WARNING": Fore.YELLOW,
        "ERROR": Fore.RED,
        "CRITICAL": Fore.MAGENTA,
    }

    def format(self, record: logging.LogRecord) -> str:
        """
        Format the log record with the appropriate color.
        """

        log_color = self.COLORS.get(record.levelname, Fore.WHITE)
        log_message = super().format(record)

        return f"{log_color}{log_message}{Style.RESET_ALL}"
