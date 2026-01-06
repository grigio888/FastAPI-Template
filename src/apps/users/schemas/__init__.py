"""
Users - Schema.

This module contains the schema for the users model.
"""

from __future__ import annotations

from datetime import UTC, datetime
from typing import Annotated

from pydantic import AfterValidator, BeforeValidator, Field

from src.apps.roles.schemas import RoleRelatioshipSchema
from src.apps.users.enums import ColorEnum, ReadingModeEnum, ThemeEnum
from src.apps.users.schemas.validators import validate_email, validate_password
from src.libs.locale.enums import LanguageEnum
from src.libs.schemas import BaseModel
from src.libs.schemas.utils import return_schema_example


# -- POST -------------------------------------------------
class UserDataSchema(BaseModel):
    """
    User data schema.

    Commonly used for creating a new user.
    """

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


class UserEmailVerificationSchema(BaseModel):
    """
    User email verification schema.

    Used for verifying user email.
    """

    token: str = Field(
        ...,
        description="Verification token",
        examples=["abc123def456ghi789jkl012mno345pqr678stu901vwx234yz567"],
    )


# -- PATCH -------------------------------------------------
class UserPreferencesUpdateDataSchema(BaseModel):
    """
    User preferences update data schema.

    Used for updating user preferences.
    """

    theme: ThemeEnum | None = Field(
        None,
        description="Theme preference of the user",
        examples=[ThemeEnum.light, ThemeEnum.dark],
    )
    color: ColorEnum | None = Field(
        None,
        description="Color preference of the user",
        examples=[ColorEnum.purple, ColorEnum.amber, ColorEnum.red, ColorEnum.sky],
    )
    reading_mode: ReadingModeEnum | None = Field(
        None,
        description="Reading mode preference of the user",
        examples=[
            ReadingModeEnum.webtoon,
            ReadingModeEnum.vertical,
            ReadingModeEnum.horizontal,
        ],
    )
    language: LanguageEnum | None = Field(
        None,
        description="Language preference of the user",
        examples=[LanguageEnum.en_us, LanguageEnum.pt_br],
    )
    show_nsfw_content: bool | None = Field(
        None,
        description="Show NSFW content preference of the user",
        examples=[True, False],
    )


class UserUpdateDataSchema(BaseModel):
    """
    User update data schema.

    Used for updating user information.
    """

    first_name: str | None = Field(
        None,
        min_length=1,
        max_length=255,
        description="First name of the user",
        examples=["John", "Jane"],
    )
    last_name: str | None = Field(
        None,
        min_length=1,
        max_length=255,
        description="Last name of the user",
        examples=["Doe", "Smith"],
    )
    username: str | None = Field(
        None,
        min_length=3,
        max_length=255,
        description="Username of the user",
        examples=["johndoe", "janesmith"],
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
    bio: str | None = Field(
        None,
        max_length=512,
        description="Bio of the user",
        examples=["I love manga.", "I enjoy playing video games."],
    )
    preferences: UserPreferencesUpdateDataSchema | None = Field(
        None,
        description="Preferences of the user",
        examples=[return_schema_example(UserPreferencesUpdateDataSchema)],
    )


# -- GET -------------------------------------------------
class UserPreferencesSchema(BaseModel):
    """
    User preferences schema.
    """

    theme: ThemeEnum = Field(
        ...,
        description="Theme preference of the user",
        examples=[ThemeEnum.light, ThemeEnum.dark],
    )
    color: ColorEnum = Field(
        ...,
        description="Color preference of the user",
        examples=[ColorEnum.purple, ColorEnum.amber, ColorEnum.red, ColorEnum.sky],
    )
    reading_mode: ReadingModeEnum = Field(
        ...,
        description="Reading mode preference of the user",
        examples=[
            ReadingModeEnum.webtoon,
            ReadingModeEnum.vertical,
            ReadingModeEnum.horizontal,
        ],
    )
    language: LanguageEnum = Field(
        ...,
        description="Language preference of the user",
        examples=[LanguageEnum.en_us, LanguageEnum.pt_br],
    )
    show_nsfw_content: bool = Field(
        ...,
        description="Show NSFW content preference of the user",
        examples=[True, False],
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
    first_name: str | None = Field(
        None,
        min_length=1,
        max_length=255,
        description="First name of the user",
        examples=["John", "Jane"],
    )
    last_name: str | None = Field(
        None,
        min_length=1,
        max_length=255,
        description="Last name of the user",
        examples=["Doe", "Smith"],
    )
    username: str = Field(
        ...,
        min_length=3,
        max_length=255,
        description="Username of the user",
        examples=["johndoe", "janesmith"],
    )
    email: str = Field(
        ...,
        min_length=1,
        max_length=255,
        description="Email of the user",
        examples=["john.doe@example.com", "jane.smith@example.com"],
    )
    role: RoleRelatioshipSchema = Field(
        ...,
        description="Role of the user",
        examples=[return_schema_example(RoleRelatioshipSchema)],
    )
    is_active: bool = Field(
        default=True,
        description="Is the user active",
    )
    is_superuser: bool = Field(
        default=False,
        description="Is the user a superuser",
    )
    avatar: (
        Annotated[
            str,
            BeforeValidator(lambda v: v.replace("/vol", "")),
        ]
        | None
    ) = Field(
        None,
        max_length=255,
        description="Avatar of the user",
        examples=["https://example.com/avatar1.png", "https://example.com/avatar2.png"],
    )
    banner: (
        Annotated[
            str,
            BeforeValidator(lambda v: v.replace("/vol", "")),
        ]
        | None
    ) = Field(
        None,
        max_length=255,
        description="Banner of the user",
        examples=["https://example.com/banner1.png", "https://example.com/banner2.png"],
    )
    bio: str | None = Field(
        None,
        max_length=512,
        description="Bio of the user",
        examples=["I love manga.", "I enjoy playing video games."],
    )
    preferences: UserPreferencesSchema = Field(
        ...,
        description="Preferences of the user",
        examples=[return_schema_example(UserPreferencesSchema)],
    )

    created_at: datetime = Field(
        ...,
        description="Creation date of the user",
        examples=[datetime.now(UTC).isoformat()],
    )
    updated_at: datetime = Field(
        ...,
        description="Last update date of the user",
        examples=[datetime.now(UTC).isoformat()],
    )
    deleted_at: datetime | None = Field(
        None,
        description="Deletion date of the user",
    )


class UserPublicSchema(BaseModel):
    """
    User schema.
    """

    id: int = Field(
        ...,
        description="ID of the user",
        examples=[1, 2, 3],
    )
    first_name: str | None = Field(
        None,
        min_length=1,
        max_length=255,
        description="First name of the user",
        examples=["John", "Jane"],
    )
    last_name: str | None = Field(
        None,
        min_length=1,
        max_length=255,
        description="Last name of the user",
        examples=["Doe", "Smith"],
    )
    username: str = Field(
        ...,
        min_length=3,
        max_length=255,
        description="Username of the user",
        examples=["johndoe", "janesmith"],
    )
    email: str = Field(
        ...,
        min_length=1,
        max_length=255,
        description="Email of the user",
        examples=["john.doe@example.com", "jane.smith@example.com"],
    )
    avatar: (
        Annotated[
            str,
            BeforeValidator(lambda v: v.replace("/vol", "")),
        ]
        | None
    ) = Field(
        None,
        max_length=255,
        description="Avatar of the user",
        examples=["https://example.com/avatar1.png", "https://example.com/avatar2.png"],
    )
    banner: (
        Annotated[
            str,
            BeforeValidator(lambda v: v.replace("/vol", "")),
        ]
        | None
    ) = Field(
        None,
        max_length=255,
        description="Banner of the user",
        examples=["https://example.com/banner1.png", "https://example.com/banner2.png"],
    )
    bio: str | None = Field(
        None,
        max_length=512,
        description="Bio of the user",
        examples=["I love manga.", "I enjoy playing video games."],
    )
