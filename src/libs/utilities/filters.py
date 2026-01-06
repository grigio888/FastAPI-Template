"""
Utilities - Field Filters.

This module contains the functions to filter the user information.
"""

from src.libs.log import get_context as _
from src.libs.log import get_logger

log = get_logger()


def apply_filter(
    parameters: dict,
    info: dict,
) -> dict:
    """
    Apply filter.

    This method expects a dictionary with parameters:

    {
        "only": "field1,field2",
        "exclude": "field3,field4"
    }

    It will perform a validation based on the parameters given and, if everything
    runs well, will perform the filtering on the info.
    """

    if not parameters.get("only") and not parameters.get("exclude"):
        return info

    if parameters.get("only") and parameters.get("exclude"):
        message = "Only one of 'only' and 'exclude' can be used"
        log.error(f"{_()}: {message}")

        raise AttributeError(message)

    if parameters.get("only"):
        log.debug(f"{_()}: Filtering only the given fields: {parameters['only']}")
        filters = parameters["only"].split(",")

        return filter_only(
            info,
            filters,
        )

    filters = parameters["exclude"].split(",")
    log.debug(f"{_()}: Filtering excluding the given fields: {parameters['exclude']}")

    return filter_exclude(
        info,
        filters,
    )


def filter_only(
    info: dict,
    filters: list[str],
) -> dict:
    """
    Filter only.

    Filter the user information to show only the given fields.
    """

    parser = {}
    for f in filters:
        if f not in info:
            continue

        parser[f] = info[f]

    if not parser:
        message = "No fields to show after filtering"
        log.error(f"{_()}: {message}")

        raise ValueError(message)

    return parser


def filter_exclude(
    info: dict,
    filters: list[str],
) -> dict:
    """
    Filter exclude.

    Filter the user information to exclude the given fields.
    """

    parser = info.copy()
    for f in filters:
        if f not in info:
            continue

        del parser[f]

    if not parser:
        message = "No fields left to show"
        log.error(f"{_()}: {message}")

        raise ValueError(message)

    return parser
