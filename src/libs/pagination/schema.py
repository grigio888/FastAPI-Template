"""
Pagination - Schema.

This module contains the schema for paginated data.
"""

from __future__ import annotations

from typing import Generic, TypeVar

from pydantic import BaseModel, Field

M = TypeVar("M")


class PaginatedSchema(BaseModel, Generic[M]):
    """
    Paginated schema.
    """

    count: int = Field(
        ...,
        description="Total number of items",
        examples=[1],
    )
    items: list[M] = Field(
        ...,
        description="List of items in the current page",
    )
    next_page: int | None = Field(
        None,
        description="Next page number, if available",
        examples=[None],
    )
    previous_page: int | None = Field(
        None,
        description="Previous page number, if available",
        examples=[None],
    )
    total_pages: int = Field(
        ...,
        description="Total number of pages",
        examples=[1],
    )
    per_page: int = Field(
        ...,
        description="Number of items per page",
        examples=[10],
    )
    current_page: int = Field(
        ...,
        description="Current page number",
        examples=[1],
    )
