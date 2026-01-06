"""
{{ cookiecutter.app_name.title() }} - Schema.

This module contains the schema for the {{ cookiecutter.app_name.title() }} schemas.
"""

from __future__ import annotations

from datetime import UTC, datetime
from pydantic import Field

from src.libs.schemas import BaseModel


class {{ cookiecutter.app_name.title() }}PublicSchema(BaseModel):
    """
    {{ cookiecutter.app_name.title() }} schema.
    """

    id: int = Field(
        ...,
        description="ID of the {{ cookiecutter.app_name.title() }}",
        examples=[1, 2, 3],
    )
    x: str = Field(
        ...,
        min_length=1,
        max_length=255,
        description="X",
        examples=["Some x value", "Another x value"],
    )
    y: str = Field(
        ...,
        min_length=1,
        max_length=255,
        description="Y",
        examples=["Some y value", "Another y value"],
    )
    z: str = Field(
        ...,
        min_length=3,
        max_length=255,
        description="Z",
        examples=["Some z value", "Another z value"],
    )
    created_at: datetime = Field(
        ...,
        description="Creation date of the Histories",
        examples=[datetime.now(UTC)],
    )
    updated_at: datetime = Field(
        ...,
        description="Last update date of the Histories",
        examples=[datetime.now(UTC)],
    )
    deleted_at: datetime | None = Field(
        None,
        description="Deletion date of the Histories",
        examples=[datetime.now(UTC), None],
    )
