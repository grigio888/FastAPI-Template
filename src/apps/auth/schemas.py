"""
Authentication - Schema.

This module contains the schema for the authentication, including login input,
access tokens, and refresh tokens
"""

from __future__ import annotations

from pydantic import Field

from src.libs.authentication.messages import Messages
from src.libs.schemas import BaseModel


class AuthSchema(BaseModel):
    """
    Schema for user authentication input.

    This schema is used for user login and includes fields for username and password.
    """

    username: str = Field(
        ...,
        min_length=1,
        max_length=255,
        description="Username of the user",
        examples=["johndoe", "janesmith"],
    )


class AccessTokenSchema(BaseModel):
    """
    Schema for access token.

    This schema is used to represent the access token generated after user
    authentication.
    """

    access_token: str = Field(
        ...,
        description="Access token",
        examples=["eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."],
    )
    detail: str | None = Field(
        None,
        description="Detail message",
        examples=[Messages.JWT_GENERATED],
    )


class RefreshTokenSchema(BaseModel):
    """
    Schema for refresh token.

    This schema is used to represent the refresh token generated after user
    authentication.
    """

    refresh_token: str = Field(
        ...,
        description="Refresh token",
        examples=["eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."],
    )
    detail: str | None = Field(
        None,
        description="Detail message",
        examples=[Messages.JWT_GENERATED],
    )


class TokensSchema(AccessTokenSchema, RefreshTokenSchema):
    """
    Tokens schema.
    """
