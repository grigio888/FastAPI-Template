"""
Roles - Schema - Permissions.

This module contains the schema for the roles model.
"""

from __future__ import annotations

from datetime import UTC, datetime

from pydantic import Field

from src.apps.roles.enums import PermissionsEnum
from src.libs.schemas import BaseModel


class PermissionDataSchema(BaseModel):
    """
    Schema for creating or updating permissions.
    """

    permission: PermissionsEnum = Field(
        ...,
        description="Permission name",
        examples=[
            PermissionsEnum.ADMIN,
            PermissionsEnum.USER,
        ],
    )


class PermissionSchema(BaseModel):
    """
    Schema for permissions.
    """

    id: int = Field(
        ...,
        description="ID of the permission",
        examples=[1, 2],
    )
    permission: PermissionsEnum = Field(
        ...,
        description="Permission name",
        examples=[
            PermissionsEnum.ADMIN,
            PermissionsEnum.USER,
        ],
    )
    created_at: datetime = Field(
        ...,
        description="Creation timestamp",
        examples=[datetime.now(UTC)],
    )
    updated_at: datetime = Field(
        ...,
        description="Last update timestamp",
        examples=[datetime.now(UTC)],
    )
    deleted_at: datetime | None = Field(
        default=None,
        description="Deletion timestamp",
        examples=[None, datetime.now(UTC)],
    )


class PermissionRelationshipSchema(BaseModel):
    """
    Schema for creating or updating permissions.
    """

    permission: PermissionsEnum = Field(
        ...,
        description="Permission name",
        examples=[
            PermissionsEnum.ADMIN,
            PermissionsEnum.USER,
        ],
    )
