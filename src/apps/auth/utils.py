"""
Authentication - Services - Utilities.

This module contains the utilities for the User's Authentication.
"""

from __future__ import annotations

import base64
from datetime import timedelta

from fastapi import Form, Header, HTTPException, status

from src.apps.auth.schemas import (
    AccessTokenSchema,
    AuthSchema,
    RefreshTokenSchema,
    TokensSchema,
)
from src.apps.users.messages import Messages as UsersMessages
from src.apps.users.models import UsersModel
from src.libs.authentication.messages import Messages
from src.libs.authentication.middleware.errors import ExpiredSignatureError, PyJWTError
from src.libs.authentication.middleware.hash import compare_hash
from src.libs.authentication.middleware.utils import create_jwt, decode_jwt
from src.libs.log import get_context as _
from src.libs.log import get_logger
from src.libs.redis import RedisClient
from src.settings import Settings

log = get_logger()
redis = RedisClient()
token_values = {
    "access": {
        "unit": Settings.TOKEN_ACCESS_UNIT,
        "value": Settings.TOKEN_ACCESS_VALUE,
    },
    "refresh": {
        "unit": Settings.TOKEN_REFRESH_UNIT,
        "value": Settings.TOKEN_REFRESH_VALUE,
    },
}


async def get_basic_token(
    authorization: str | None = Header(None),
    username: str | None = Form(None),
    password: str | None = Form(None),
) -> str:
    """
    Get basic token.

    Return the basic token from the Authorization header or,
    if missing, generate it from the username and password form fields.
    """

    # Receives from the Authorization header.
    if authorization and "basic" in authorization.lower():
        return authorization

    # Receives from the username and password from the Swagger.
    if username is not None and password is not None:
        token = f"{username}:{password}"
        return "Basic " + base64.b64encode(token.encode()).decode()

    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail=Messages.JWT_INVALID_TYPE,
    )


def validate_user(token: str) -> AuthSchema:
    """
    Validate user against the Users Private API.

    It checks if the user info is correct in the Users Private API.
    """

    log.debug(f"{_()}: Decoding basic token")

    basic_token = token.split(" ")

    if basic_token[0].lower() != "basic":
        log.error(f"{_()}: Invalid token type")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=Messages.NOT_BASIC_TOKEN,
        )

    if len(basic_token) != 2:
        log.error(f"{_()}: Invalid token structure")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=Messages.JWT_INVALID_STRUCTURE,
        )

    try:
        decoded_token = base64.b64decode(basic_token[1]).decode("utf-8")
        username, password = decoded_token.split(":")
    except ValueError as error:
        log.exception(f"{_()}: Error decoding basic token")

        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=Messages.INVALID_CREDENTIALS,
        ) from error

    log.debug(f"{_()}: Basic token decoded successfully")
    log.debug(f"{_()}: Verifying user against the Database")

    user_model = (
        UsersModel.query()
        .filter(
            (UsersModel.username == username) | (UsersModel.email == username),
        )
        .first()
    )

    if not user_model:
        log.error(f"{_()}: User not found")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=Messages.INVALID_CREDENTIALS,
        )

    if not user_model.is_active:
        log.error(f"{_()}: Inactive user {username}")

        raise HTTPException(
            status_code=status.HTTP_406_NOT_ACCEPTABLE,
            detail=UsersMessages.Users.Error.INACTIVE_USER,
        )

    if not compare_hash(password, user_model.password):
        log.error(f"{_()}: Invalid password for user {username}")

        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=Messages.INVALID_CREDENTIALS,
        )

    return AuthSchema(username=user_model.email)


def get_sub(
    string: str,
) -> str:
    """
    Generate sub based on email or username.
    """

    base64_sub_length = 10

    return base64.b64encode(string.encode())[:base64_sub_length].decode()


def get_token_data(
    token: str,
) -> dict:
    """
    Get the token data.

    It retrieves the token data from the redis database.
    """

    try:
        log.debug(f"{_()}: Retrieving token data")
        decoded_token = decode_jwt(token)

    except PyJWTError as error:
        log.exception(f"{_()}: Error decoding token")

        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=Messages.JWT_INVALID_STRUCTURE,
        ) from error

    except ValueError as error:
        log.exception(f"{_()}: Error decoding token")

        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(error),
        ) from error

    token_pattern = f"{decoded_token['sub']}:{token}"
    token_data = redis.get(token_pattern)

    if not token_data:
        log.error(f"{_()}: USER_NOT_FOUND. User not found in redis")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=UsersMessages.Users.Error.NOT_FOUND,
        )

    return token_data


def validate_token_info(
    token: str,
    token_type: str = "access",
) -> dict:
    """
    Validate a token.

    It checks if the token is valid and if it has expired.
    """

    try:
        log.debug(f"{_()}: Validating token")
        decoded_token = decode_jwt(token)

    except ValueError as error:
        log.exception(f"{_()}: Error decoding token")

        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=Messages.JWT_INVALID_STRUCTURE,
        ) from error

    except PyJWTError as error:
        log.exception(f"{_()}: Error decoding token")

        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=Messages.JWT_INVALID,
        ) from error

    except Exception as error:
        log.exception(f"{_()}: Caught an unexpected error")

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=Messages.GENERIC_ERROR,
        ) from error

    log.debug(f"{_()}: Decoded token successfully: {decoded_token}")

    try:
        redis_token = redis.search(f"*:{token}")

        if (
            not decoded_token
            or not redis_token
            or redis_token[0].get("type") != token_type
        ):
            log.error(
                f"{_()}: Decoded token is invalid or not the expected type",
            )
            log.error(
                f"{_()}: {token_type} - token_info: {redis_token}",
            )

            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=Messages.JWT_EXPIRED,
            )

        log.debug(f"{_()}: Token is valid and of the expected type")

    except ExpiredSignatureError as error:
        log.exception(f"{_()}: Token has expired")

        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=Messages.JWT_EXPIRED,
        ) from error

    except Exception as error:
        log.exception(f"{_()}: Error validating token")

        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=Messages.JWT_INVALID_ACCESS_TOKEN,
        ) from error

    return decoded_token


def create_token(
    user_schema: AuthSchema,
    token_type: str,
    custom_expires_delta: timedelta | None = None,
    **kwargs: str | bool,
) -> AccessTokenSchema | RefreshTokenSchema:
    """
    Create a token.

    It creates an token and adds it to the valid tokens set.
    """

    log.info(f"{_()}: Creating {token_type} token for user.")

    if not user_schema.username:
        message = Messages.INVALID_CREDENTIALS
        log.error(f"{_()}: {message}")

        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=message,
        )

    sub = get_sub(user_schema.username)

    if token_type not in ["access", "refresh"]:
        message = Messages.JWT_INVALID_TYPE
        log.error(f"{_()}: {message}")

        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=message,
        )

    log.debug(f"{_()}: Creating {token_type} token for user alias: {sub}")

    time_delta = custom_expires_delta or timedelta(  # type: ignore[misc]
        **{token_values[token_type]["unit"]: token_values[token_type]["value"]},  # type: ignore[arg-type]
    )
    token = create_jwt(
        {"sub": sub, "type": token_type},
        expires_delta=time_delta,
        **kwargs,
    )

    if token_type == "refresh":
        return RefreshTokenSchema(refresh_token=token)  # type: ignore[call-arg]

    return AccessTokenSchema(access_token=token)  # type: ignore[call-arg]


def create_pair_tokens(user_schema: AuthSchema) -> TokensSchema:
    """
    Create a pair of tokens.

    It creates an access token and a refresh token.
    """

    log.info(f"{_()}: Creating pair of tokens for user.")

    access_token = create_token(user_schema, "access")
    refresh_token = create_token(user_schema, "refresh")

    return TokensSchema(
        access_token=access_token.access_token,  # type: ignore[union-attr]
        refresh_token=refresh_token.refresh_token,  # type: ignore[union-attr]
        detail=Messages.JWT_GENERATED,
    )


def set_token(
    token: str,
    user_email: str,
    token_type: str,
    **kwargs: str | bool,
) -> bool:
    """
    Set token.

    Set the token on Redis.
    """

    sub = get_sub(user_email)

    redis.set(
        f"{sub}:{token}",
        {
            "pair": "",
            "email": user_email,
            "type": token_type,
            **kwargs,
        },
        timedelta(  # type: ignore[misc]
            **{token_values[token_type]["unit"]: token_values[token_type]["value"]},  # type: ignore[arg-type]
        ),
    )

    return True


def set_pair_tokens(
    headers: dict[str, str],
    user_email: str,
    **kwargs: str,
) -> None:
    """
    Set pair tokens.

    Set the pair of tokens on Redis.
    """

    access_token = headers.get("authorization")
    refresh_token = headers.get("refreshtoken")

    if not access_token or not refresh_token:
        message = Messages.TOKEN_ERROR_INVALID_CRED
        log.error(f"{_()}: {message}")

        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=message,
        )

    set_token(access_token, user_email, "access", **kwargs)
    set_token(refresh_token, user_email, "refresh")


def link_tokens(
    access_token: str,
    refresh_token: str,
    identifier: str,
) -> bool:
    """
    Link tokens together.

    This method link tokens together on redis to avoid a access_token being
    revoked and a refresh_token being left behind.
    """

    sub = get_sub(identifier)

    def search_and_add(
        target: str,
        pair: str,
    ) -> None:
        key = f"{sub}:{target}"
        entry = redis.get(key)

        if not entry:
            raise ValueError

        entry["pair"] = pair

        time_delta = timedelta(  # type: ignore[misc]
            **{  # type: ignore[arg-type]
                token_values[entry["type"]]["unit"]: token_values[entry["type"]][
                    "value"
                ],
            },
        )

        redis.set(
            key,
            entry,
            time_delta,
        )

    search_and_add(access_token, refresh_token)
    search_and_add(refresh_token, access_token)

    return True


def revoke_tokens_from_redis(tokens: list) -> None:
    """
    Revoke a token.
    """

    for item in tokens:
        pattern = f"*:{item}"
        search = redis.search(pattern)

        if search:
            redis.delete_pattern(pattern)


def delete_token_pair(access_token: str, refresh_token: str) -> bool:
    """
    Delete a pair of tokens.

    It deletes a pair of tokens from the valid tokens set.
    """

    try:
        validate_token_info(access_token)
        validate_token_info(refresh_token, "refresh")

    except HTTPException as error:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=Messages.JWT_ALREADY_REVOKED,
        ) from error

    revoke_tokens_from_redis(
        [
            access_token,
            refresh_token,
        ],
    )

    return True
