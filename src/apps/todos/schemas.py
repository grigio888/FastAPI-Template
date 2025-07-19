"""
ToDo - Schema.

This module contains the schema for the todo model.
"""

from __future__ import annotations

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
