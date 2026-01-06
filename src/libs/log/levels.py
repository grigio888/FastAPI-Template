"""
Logger - Levels.

This module provides the configuration for the application's logging levels.
"""

import logging


class MaxLevelFilter(logging.Filter):
    """
    Module to allow only certain logs equal or bellow a certain level.

    Used to filter DEBUG and INFO from the rest.
    """

    def __init__(self, max_level: int) -> None:
        """
        Initializator.
        """

        super().__init__()
        self.max_level = max_level

    def filter(self, record: logging.LogRecord) -> bool:
        """
        Define which level should be logged.
        """

        return record.levelno <= self.max_level
