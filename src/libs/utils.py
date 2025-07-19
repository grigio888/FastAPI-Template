"""
Utilities.

This module contains utility functions for dictionaries.
"""

from __future__ import annotations

from datetime import datetime, timedelta, timezone

from decouple import config

LOG_THRESHOLD_UNIT = config("LOG_THRESHOLD_UNIT", default="minutes")
LOG_THRESHOLD_VALUE = config("LOG_THRESHOLD_VALUE", default=1, cast=int)
LOG_TIME_THRESHOLD = datetime.now(tz=timezone.utc)


def is_filled(data: dict) -> bool:
    """
    Check if at least one field is filled in a nested dictionary.

    This function will check if at least one field is filled in the
    dictionary, recursively.
    """

    for v in data.__dict__.values():
        if isinstance(v, dict):
            return is_filled(v)

        if v:
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

    return datetime.now(tz=timezone.utc) >= LOG_TIME_THRESHOLD


def generate_log_threshold() -> datetime:
    """
    Generate threshold.
    """

    return datetime.now(tz=timezone.utc) + timedelta(
        **{LOG_THRESHOLD_UNIT: LOG_THRESHOLD_VALUE},
    )


def refresh_log_threshold() -> None:
    """
    Refresh the log threshold.
    """

    global LOG_TIME_THRESHOLD
    LOG_TIME_THRESHOLD = generate_log_threshold()
