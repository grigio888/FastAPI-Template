"""
Database - Pagination - Utils.
"""

from __future__ import annotations

from collections.abc import Iterable
from typing import TYPE_CHECKING, TypeVar

if TYPE_CHECKING:
    from sqlalchemy.orm import Query

from src.libs.database.base_model import BaseModel

T = TypeVar("T", bound=BaseModel)


def apply_filters(
    query: Query[T],
    skip: list[str] = [],
    **kwargs: str | int | bool | list,
) -> Query[T]:
    """
    Apply filters.
    """

    for method, value in kwargs.items() or []:
        if method in skip:
            continue

        func = getattr(query, method)

        if isinstance(value, Iterable) and not isinstance(value, str):
            query = func(*value)
        else:
            query = func(value)

    return query
