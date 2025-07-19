"""
Common Libs - Logging - Configuration.

This module provides the configuration for the application's logging.
"""

from decouple import config

LOG_LEVEL = config("LOG_LEVEL", default="DEBUG")
LOG_FORMAT = config(
    "LOG_FORMAT",
    default="[%(asctime)s - %(levelname)s] %(name)s %(message)s",
)
LOG_NAME = config("LOG_NAME", default="backend")
