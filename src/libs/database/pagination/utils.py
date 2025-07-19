"""
Database - Pagination - Utils.
"""

from __future__ import annotations

from src.libs.database.base_model import BaseModel


def apply_filters(
    model: BaseModel,
    skip: list[str] = [],
    **kwargs: str | int | bool | list,
) -> BaseModel:
    """
    Apply filters.
    """

    for method, value in kwargs.items() or []:
        if method in skip:
            continue

        func = getattr(model, method)
        model = func(*value) if value is not str else func(value)

    return model
