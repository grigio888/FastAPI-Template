"""
Pagination utilities.

This module contains utilities for paginating data.

Disclaimer:
This pagination should not be used to paginate large datasets (E.g. Salesforce ORM).
It is recommended to use the ORM's built-in pagination features for large datasets.
"""

from collections.abc import Generator

from src.libs.pagination.schema import PaginatedSchema
from src.settings import Settings


def get_data_generator(data: list, page_size: int) -> Generator[list[dict]]:
    """
    Generate data in chunks.
    """

    for i in range(0, len(data), page_size):
        yield data[i : i + page_size]


async def paginate(
    data: list,
    page: int = 1,
    page_size: int = Settings.PAGE_SIZE,
) -> PaginatedSchema:
    """
    Paginate data.

    :param data: List of data to paginate.
    :param page: Page number.
    :param page_size: Number of items per page.

    :return: Paginated data.
    """
    data_generator = get_data_generator(data, page_size)
    items = next(
        (chunk for idx, chunk in enumerate(data_generator, start=1) if idx == page),
        [],
    )

    next_page: int | None = page + 1 if (page * page_size) < len(data) else None
    previous_page: int | None = page - 1 if page > 1 else None
    total_pages = (len(data) + page_size - 1) // page_size

    return PaginatedSchema(
        count=len(data),
        items=items,
        next_page=next_page,
        previous_page=previous_page,
        total_pages=total_pages,
        per_page=page_size,
        current_page=page,
    )
