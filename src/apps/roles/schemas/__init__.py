"""
Roles - Schema.

This module contains the schema for the roles model.
"""

from __future__ import annotations

from datetime import UTC, datetime

from pydantic import Field

from src.apps.roles.schemas.permissions import (
    PermissionRelationshipSchema,
)
from src.libs.schemas import BaseModel
from src.libs.schemas.utils import return_schema_example


class RoleDataSchema(BaseModel):
    """
    Role data schema for POST operations.
    """

    slug: str = Field(
        ...,
        min_length=1,
        max_length=255,
        description="Slug of the role",
        examples=["admin", "user"],
    )
    title: str = Field(
        ...,
        min_length=1,
        max_length=255,
        description="Title of the role",
        examples=["Administrator", "User"],
    )
    permissions: list[int] = Field(
        default=[],
        description="List of permission IDs associated with the role",
        examples=[[1, 2]],
    )


class RoleUpdateDataSchema(BaseModel):
    """
    Role update data schema.
    """

    slug: str | None = Field(
        default=None,
        min_length=1,
        max_length=255,
        description="Slug of the role",
        examples=["admin", "user"],
    )
    title: str | None = Field(
        default=None,
        min_length=1,
        max_length=255,
        description="Title of the role",
        examples=["Administrator", "User"],
    )
    permissions: list[int] | None = Field(
        default=None,
        description="List of permission IDs associated with the role",
        examples=[[1, 2]],
    )


class RoleSchema(BaseModel):
    """
    Role schema.
    """

    id: int = Field(
        ...,
        description="ID of the role",
        examples=[1, 2, 3],
    )
    slug: str = Field(
        ...,
        min_length=1,
        max_length=255,
        description="Slug of the role",
        examples=["admin", "user"],
    )
    title: str = Field(
        ...,
        min_length=1,
        max_length=255,
        description="Title of the role",
        examples=["Administrator", "User"],
    )
    permissions: list[PermissionRelationshipSchema] = Field(
        default=[],
        description="List of permissions associated with the role",
        examples=[return_schema_example(PermissionRelationshipSchema)],
    )
    created_at: datetime = Field(
        ...,
        description="Creation date of the role",
        examples=[datetime.now(tz=UTC)],
    )
    updated_at: datetime = Field(
        ...,
        description="Last update date of the role",
        examples=[datetime.now(tz=UTC)],
    )
    deleted_at: datetime | None = Field(
        default=None,
        description="Deletion date of the role",
        examples=[None, datetime.now(tz=UTC)],
    )


class RoleRelatioshipSchema(BaseModel):
    """
    Role data schema for POST operations.
    """

    slug: str = Field(
        ...,
        min_length=1,
        max_length=255,
        description="Slug of the role",
        examples=["admin", "user"],
    )
    title: str = Field(
        ...,
        min_length=1,
        max_length=255,
        description="Title of the role",
        examples=["Administrator", "User"],
    )
    permissions: list[PermissionRelationshipSchema] = Field(
        default=[],
        description="List of permission IDs associated with the role",
        examples=[[1, 2]],
    )
