"""
To Do - Schema.

This module contains the schema for the To Do model.
"""

from __future__ import annotations

from datetime import datetime, timezone

from pydantic import Field

from src.libs.schemas import BaseModel


class TodoDataSchema(BaseModel):
    """
    Todo data schema.
    """

    name: str = Field(
        ...,
        min_length=1,
        max_length=255,
        description="Name of the todo",
        examples=["Buy groceries", "Walk the dog"],
    )
    percentage: float = Field(
        0.0,
        ge=0.0,
        le=100.0,
        description="Percentage of completion of the todo",
        examples=[0.0, 50.0, 100.0],
    )
    description: str | None = Field(
        default=None,
        max_length=1000,
        description="Description of the todo",
        examples=["Buy groceries for the week", "Walk the dog in the park"],
    )


class TodoSchema(TodoDataSchema):
    """
    Todo schema.
    """

    id: int = Field(
        ...,
        description="ID of the todo",
        examples=[1, 2, 3],
    )
    created_at: str = Field(
        ...,
        description="Creation timestamp of the todo in ISO 8601 format",
        examples=[datetime.now(tz=timezone.utc).isoformat()],
    )
    updated_at: str = Field(
        ...,
        description="Last update timestamp of the todo in ISO 8601 format",
        examples=[datetime.now(timezone.utc).isoformat()],
    )
    deleted_at: str | None = Field(
        default=None,
        description="Deletion timestamp of the todo in ISO 8601 format, if deleted",
        examples=[None, datetime.now(timezone.utc).isoformat()],
    )
