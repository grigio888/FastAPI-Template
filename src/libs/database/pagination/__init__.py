"""
Database - Pagination.

This module contains the pagination utility function.
"""

from __future__ import annotations

from typing import TypeVar

from src.libs.database.base_model import BaseModel, DeclarativeBaseModel
from src.libs.database.pagination.utils import apply_filters
from src.libs.database.session import get_session
from src.libs.pagination.schema import PaginatedSchema
from src.libs.schemas import BaseModel as SchemaBaseModel

T = TypeVar("T", bound=BaseModel)
TD = TypeVar("TD", bound=DeclarativeBaseModel)
S = TypeVar("S", bound=SchemaBaseModel)
db = get_session()


def paginate(
    model: type[T | TD],
    page: int = 1,
    page_size: int = 10,
    schema: type[S] | None = None,
    schema_options: dict = {},
    **kwargs: str | int | bool | list,
) -> PaginatedSchema:
    """
    Paginate data.
    """

    # parsing info
    cursor = (page - 1) * page_size

    # constructing query
    model_query = apply_filters(model.query(), skip=[], **kwargs)

    # fetch page
    page_items = model_query.limit(page_size).offset(cursor)
    items = list(page_items.all())

    if schema:
        items = [schema.from_model(m, **schema_options) for m in items]

    # fetch count
    count = model_query.count()

    # parsing remaining info
    next_page: int | None = page + 1 if (page * page_size) < count else None
    previous_page: int | None = page - 1 if page > 1 else None
    total_pages = (count + page_size - 1) // page_size

    return PaginatedSchema(
        count=count,
        items=items,
        next_page=next_page,
        previous_page=previous_page,
        total_pages=total_pages,
        per_page=page_size,
        current_page=page,
    )
