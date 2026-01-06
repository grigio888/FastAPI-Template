"""
Authentication - Middleware - Utilities.

This module contains utility functions to work with JWT tokens.
"""

from __future__ import annotations

from copy import deepcopy
from datetime import UTC, datetime, timedelta

import jwt
from fastapi import HTTPException, status

from src.libs.authentication.messages import Messages
from src.libs.authentication.middleware.errors import ExpiredSignatureError, PyJWTError
from src.libs.log import get_context as _
from src.libs.log import get_logger
from src.libs.redis import RedisClient
from src.settings import Settings

log = get_logger()
redis = RedisClient()

SECRET_KEY = Settings.SECRET_KEY
ALGORITHM = Settings.ALGORITHM


def deconstruct_auth_header(auth_header: str) -> tuple:
    """
    # Deconstruct the Authorization header.

    into its schema and token parts.

    ---

    Args:
        auth_header (str): The Authorization header from the request.

    Returns:
        tuple: A tuple containing the schema and token parts.

    Raises:
        HTTPException: If the Authorization header is invalid.
            - **401**: Messages.JWT_INVALID_HEADER.

    """

    try:
        schema, token = auth_header.split()

    except (ValueError, AttributeError) as error:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=Messages.JWT_INVALID_HEADER,
        ) from error

    if not schema or not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=Messages.JWT_INVALID_HEADER,
        )

    return schema, token


def create_jwt(data: dict, expires_delta: timedelta | None = None) -> str:
    """
    Create a JWT token with the given data and expiration time.
    """

    payload = deepcopy(data)

    delta = expires_delta or timedelta(minutes=15)
    expire = datetime.now(UTC) + delta
    payload.update({"exp": expire})

    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)


def decode_jwt(token: str) -> dict:
    """
    Decode a JWT token and return the payload.
    """

    try:
        return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

    except jwt.ExpiredSignatureError as error:
        message = Messages.JWT_EXPIRED

        raise ValueError(message) from error

    except jwt.InvalidTokenError as error:
        message = Messages.JWT_INVALID_ACCESS_TOKEN

        raise ValueError(message) from error


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
