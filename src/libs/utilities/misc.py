"""
Utilities - Miscellaneous.

This module contains utility functions for dictionaries.
"""

from __future__ import annotations

from collections.abc import Iterable
from datetime import UTC, datetime, timedelta
from typing import Any

from src.settings import Settings

LOG_THRESHOLD_UNIT = Settings.LOG_THRESHOLD_UNIT
LOG_THRESHOLD_VALUE = Settings.LOG_THRESHOLD_VALUE

LOG_TIME_THRESHOLD = datetime.now(tz=UTC)


def _iter_values(data: Any) -> Iterable[Any]:  # noqa: ANN401
    """Return iterable values for dictionaries, iterables, or objects."""

    if isinstance(data, dict):
        return data.values()

    if isinstance(data, dict | list | tuple | set):
        return data

    attrs = getattr(data, "__dict__", None)
    if attrs is not None:
        return attrs.values()

    return [data]


def is_filled(data: Any) -> bool:  # noqa: ANN401
    """
    Check if at least one field is filled in a nested dictionary.

    This function will check if at least one field is filled in the
    dictionary, recursively.
    """

    for value in _iter_values(data):
        if isinstance(value, dict | list | tuple | set):
            if is_filled(value):
                return True
            continue

        if getattr(value, "__dict__", None) is not None:
            if is_filled(value.__dict__):
                return True
            continue

        if value:
            return True

    return False


def order_dict(data: dict) -> dict:
    """
    Order dictionary keys alphabetically in a nested dictionary.

    This function will order the dictionary keys alphabetically,
    recursively.
    """

    return {
        k: order_dict(v) if isinstance(v, dict) else v for k, v in sorted(data.items())
    }


def clean_dict(data: dict, values: list = []) -> dict:
    """
    Clean dictionary from None and other values in a nested dictionary.

    This function will remove all None values from the dictionary,
    recursively.
    """

    skip = [None, [], {}, *values]

    return {
        k: clean_dict(v, values) if isinstance(v, dict) else v
        for k, v in data.items()
        if v not in skip
    }


def should_log() -> bool:
    """
    Check if the log should be printed based on the threshold.

    :param log_time: Time of the log.
    :return: Boolean indicating if the log should be printed.
    """

    return datetime.now(tz=UTC) >= LOG_TIME_THRESHOLD


def generate_log_threshold() -> datetime:
    """
    Generate threshold.
    """

    return datetime.now(tz=UTC) + timedelta(**{LOG_THRESHOLD_UNIT: LOG_THRESHOLD_VALUE})


def refresh_log_threshold() -> None:
    """
    Refresh the log threshold.
    """

    global LOG_TIME_THRESHOLD
    LOG_TIME_THRESHOLD = generate_log_threshold()


def slugfy(text: str) -> str:
    """
    # Slugify a given text.

    ---

    Args:
        text: Text to be slugified.

    Returns:
        Slugified text.

    ---

    Example:
        ```python
        slug = slugfy("Hello World")
        print(slug)  # Output: "hello-world"
        ```

    """

    return text.lower().replace(" ", "-")
