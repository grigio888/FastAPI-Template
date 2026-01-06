"""
Validators for roles and permissions schemas.
"""

from __future__ import annotations

from pydantic import field_validator


class PermissionSchemaValidator:
    """Validator for PermissionSchema."""

    @field_validator("permission")
    def validate_permission(self, v: str) -> str:
        """
        Validate permission field.
        """
        if not v or not v.strip():
            raise ValueError("Permission name cannot be empty.")
        if len(v) > 255:
            raise ValueError("Permission name must be at most 255 characters.")
        return v


class RoleDataSchemaValidator:
    """Validator for RoleDataSchema."""

    @field_validator("slug")
    def validate_slug(self, v: str) -> str:
        """
        Validate slug field.
        """
        if not v or not v.strip():
            raise ValueError("Slug cannot be empty.")
        if len(v) > 255:
            raise ValueError("Slug must be at most 255 characters.")
        return v

    @field_validator("title")
    def validate_title(self, v: str) -> str:
        """
        Validate title field.
        """
        if not v or not v.strip():
            raise ValueError("Title cannot be empty.")
        if len(v) > 255:
            raise ValueError("Title must be at most 255 characters.")
        return v

    @field_validator("permissions")
    def validate_permissions(self, v: list[int]) -> list[int]:
        """
        Validate permissions field.
        """
        if not isinstance(v, list):
            raise TypeError("Permissions must be a list of IDs.")
        if not all(isinstance(i, int) for i in v):
            raise ValueError("All permissions must be integers.")
        return v


class RoleUpdateDataSchemaValidator:
    """Validator for RoleUpdateDataSchema."""

    @field_validator("slug")
    def validate_slug(self, v: str | None) -> str | None:
        """
        Validate slug field.
        """
        if v is not None:
            if not v.strip():
                raise ValueError("Slug cannot be empty.")
            if len(v) > 255:
                raise ValueError("Slug must be at most 255 characters.")
        return v

    @field_validator("title")
    def validate_title(self, v: str | None) -> str | None:
        """
        Validate title field.
        """
        if v is not None:
            if not v.strip():
                raise ValueError("Title cannot be empty.")
            if len(v) > 255:
                raise ValueError("Title must be at most 255 characters.")
        return v

    @field_validator("permissions")
    def validate_permissions(self, v: list[int] | None) -> list[int] | None:
        """
        Validate permissions field.
        """
        if v is not None:
            if not isinstance(v, list):
                raise TypeError("Permissions must be a list of IDs.")
            if not all(isinstance(i, int) for i in v):
                raise ValueError("All permissions must be integers.")
        return v
