"""
Roles - Models.

This module contains the models for the Roles.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from src.apps.users.models import UsersModel

import sqlalchemy as sa
from sqlalchemy.orm import Mapped as M  # noqa: N817
from sqlalchemy.orm import mapped_column as MColumn  # noqa: N812
from sqlalchemy.orm import relationship

from src.apps.roles.enums import RolesEnum
from src.libs.database.base_model import BaseModel

roles_permissions = sa.Table(
    "roles_permissions",
    BaseModel.metadata,
    sa.Column(
        "role_id",
        sa.Integer,
        sa.ForeignKey("roles_roles.id"),
        primary_key=True,
    ),
    sa.Column(
        "permission_id",
        sa.Integer,
        sa.ForeignKey("roles_permission.id"),
        primary_key=True,
    ),
    sa.Column(
        "created_at",
        sa.DateTime,
        server_default=sa.text("CURRENT_TIMESTAMP"),
        nullable=True,
    ),
)


class PermissionsModel(BaseModel):
    """
    Permissions.

    This class represents the permissions model.
    """

    __tablename__ = "roles_permission"

    permission: M[str] = MColumn(sa.String(255), nullable=False)

    roles: M[list[RolesModel]] = relationship(
        "RolesModel",
        secondary=roles_permissions,
        back_populates="permissions",
        lazy=False,
    )

    def __repr__(self) -> str:
        """
        Representation of the PermissionsModel instance.
        """
        return f"<PermissionsModel - id:{self.id} - permission:{self.permission}>"


class RolesModel(BaseModel):
    """
    Roles.

    This class represents the roles model.
    """

    __tablename__ = "roles_roles"

    slug: M[RolesEnum] = MColumn(
        sa.Enum(RolesEnum, name="roles_enum"),
        nullable=False,
    )
    title: M[str] = MColumn(sa.String(255), nullable=False)

    permissions: M[list[PermissionsModel]] = relationship(
        "PermissionsModel",
        secondary=roles_permissions,
        back_populates="roles",
        lazy="selectin",
    )
    users: M[list[UsersModel]] = relationship(
        "UsersModel",
        back_populates="role",
        lazy="selectin",
    )

    def __repr__(self) -> str:
        """
        Representation of the RolesModel instance.
        """
        return f"<RolesModel - id:{self.id} - slug:{self.slug}>"
