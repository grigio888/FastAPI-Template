"""
ToDo - Schema.

This module contains the schema for the todo model.
"""

from __future__ import annotations

from datetime import datetime, timezone
from typing import Annotated

from pydantic import AfterValidator, Field

from src.apps.users.schemas.validators import validate_email, validate_password
from src.libs.schemas import BaseModel


class UserDataSchema(BaseModel):
    """
    User data schema.
    """

    name: str = Field(
        ...,
        min_length=1,
        max_length=255,
        description="Name of the user",
        examples=["John Doe", "Jane Smith"],
    )
    email: Annotated[
        str,
        AfterValidator(validate_email),
    ] = Field(
        ...,
        min_length=1,
        max_length=255,
        description="Email of the user",
        examples=["john.doe@example.com", "jane.smith@example.com"],
    )
    password: Annotated[
        str,
        AfterValidator(validate_password),
    ] = Field(
        ...,
        max_length=255,
        description="Password of the user",
        examples=["password123", "securepassword"],
    )


class UserUpdateDataSchema(BaseModel):
    """
    User update data schema.
    """

    name: str | None = Field(
        None,
        min_length=1,
        max_length=255,
        description="Name of the user",
        examples=["John Doe", "Jane Smith"],
    )
    email: (
        Annotated[
            str,
            AfterValidator(validate_email),
        ]
        | None
    ) = Field(
        None,
        min_length=1,
        max_length=255,
        description="Email of the user",
        examples=["john.doe@example.com", "jane.smith@example.com"],
    )
    password: (
        Annotated[
            str,
            AfterValidator(validate_password),
        ]
        | None
    ) = Field(
        None,
        max_length=255,
        description="Password of the user",
        examples=["password123", "securepassword"],
    )


class UserSchema(BaseModel):
    """
    User schema.
    """

    id: int = Field(
        ...,
        description="ID of the user",
        examples=[1, 2, 3],
    )
    name: str = Field(
        ...,
        min_length=1,
        max_length=255,
        description="Name of the user",
        examples=["John Doe", "Jane Smith"],
    )
    email: str = Field(
        ...,
        min_length=1,
        max_length=255,
        description="Email of the user",
        examples=["john.doe@example.com", "jane.smith@example.com"],
    )
    is_active: bool = Field(
        default=True,
        description="Is the user active",
    )
    is_superuser: bool = Field(
        default=False,
        description="Is the user a superuser",
    )

    created_at: datetime = Field(
        ...,
        description="Creation date of the user",
        examples=[datetime.now(timezone.utc).isoformat()],
    )
    updated_at: datetime = Field(
        ...,
        description="Last update date of the user",
        examples=[datetime.now(timezone.utc).isoformat()],
    )
    deleted_at: datetime | None = Field(
        None,
        description="Deletion date of the user",
    )
