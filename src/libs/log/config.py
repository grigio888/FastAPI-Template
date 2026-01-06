"""
Logger - Configuration.
"""

from src.settings import Settings

LOG_LEVEL = Settings.LOG_LEVEL
LOG_FORMAT = Settings.LOG_FORMAT
LOG_NAME = Settings.LOG_NAME

__all__ = ["LOG_FORMAT", "LOG_LEVEL", "LOG_NAME"]
