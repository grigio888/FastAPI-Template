"""
Users - Model.

This module contains the model for the Users.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from src.apps.roles.models import RolesModel

import sqlalchemy as sa
from sqlalchemy.event import listens_for as sa_event_listens_for
from sqlalchemy.orm import Mapped as M  # noqa: N817
from sqlalchemy.orm import Mapper, relationship
from sqlalchemy.orm import mapped_column as MColumn  # noqa: N812

from src.apps.users.enums import ColorEnum, ReadingModeEnum, ThemeEnum
from src.libs.database.base_model import BaseModel
from src.libs.locale.enums import LanguageEnum


class UsersModel(BaseModel):
    """
    Users.

    This class represents the users model.
    """

    __tablename__ = "users"

    first_name: M[str] = MColumn(sa.String(255), nullable=True)
    last_name: M[str] = MColumn(sa.String(255), nullable=True)
    username: M[str] = MColumn(sa.String(255), nullable=False, unique=True)
    email: M[str] = MColumn(sa.String(255), nullable=False, unique=True)
    password: M[str] = MColumn(sa.String(255), nullable=False)

    avatar: M[str | None] = MColumn(sa.String(255), nullable=True)
    banner: M[str | None] = MColumn(sa.String(255), nullable=True)
    bio: M[str | None] = MColumn(sa.Text, nullable=True)
    preferences: M[UserPreferencesModel] = relationship(
        "UserPreferencesModel",
        uselist=False,
        back_populates="user",
        cascade="all, delete-orphan",
    )

    is_active: M[bool] = MColumn(sa.Boolean, default=False)

    verification_token: M[str | None] = MColumn(sa.String(255), nullable=True)
    reset_token: M[str | None] = MColumn(sa.String(255), nullable=True)

    is_superuser: M[bool] = MColumn(sa.Boolean, default=False)

    role_id: M[int] = MColumn(
        sa.Integer,
        sa.ForeignKey("roles_roles.id"),
        nullable=False,
    )

    role: M[RolesModel] = relationship(
        "RolesModel",
        back_populates="users",
        uselist=False,
    )

    def __repr__(self) -> str:
        """
        Representation of the UsersModel.
        """
        return f"<UsersModel - id:{self.id} - username:{self.username}>"

    def __str__(self) -> str:
        """
        Return string representation of the UsersModel.
        """

        return f"{self.username} ({self.email})"

class UserPreferencesModel(BaseModel):
    """
    UserPreferencesModel.

    This class represents the user preferences model.
    """

    __tablename__ = "users_preferences"

    user_id: M[int] = MColumn(sa.Integer, sa.ForeignKey("users.id"), unique=True)

    theme: M[ThemeEnum] = MColumn(
        sa.Enum(ThemeEnum, name="theme_enum"),
        default=ThemeEnum.dark.value,
    )
    color: M[ColorEnum] = MColumn(
        sa.Enum(ColorEnum, name="color_enum"),
        default=ColorEnum.purple.value,
    )
    reading_mode: M[ReadingModeEnum] = MColumn(
        sa.Enum(ReadingModeEnum, name="reading_mode_enum"),
        default=ReadingModeEnum.horizontal.value,
    )
    language: M[LanguageEnum] = MColumn(
        sa.Enum(LanguageEnum, name="language_enum"),
        default=LanguageEnum.en_us.value,
    )

    user: M[UsersModel] = relationship(
        "UsersModel",
        back_populates="preferences",
        uselist=False,
    )


# -- Hooks -----------------------------------
@sa_event_listens_for(UsersModel, "after_insert")
def create_user_preferences(
    _mapper: Mapper,
    connection: sa.engine.Connection,
    target: UsersModel,
) -> None:
    """
    Create user preferences after a user is created.
    """
    pref_table: sa.Table = UserPreferencesModel.__table__  # type: ignore[assignment]
    connection.execute(
        sa.insert(pref_table).values(
            user_id=target.id,
            theme=ThemeEnum.dark.value,
            color=ColorEnum.purple.value,
            reading_mode=ReadingModeEnum.horizontal.value,
        ),
    )
