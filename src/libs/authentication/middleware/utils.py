"""
JWT - Utilities.

This module contains utility functions to work with JWT tokens.
"""

from __future__ import annotations

from copy import deepcopy
from datetime import datetime, timedelta, timezone

import httpx
import jwt
from decouple import config
from fastapi import HTTPException

from src.libs.log import get_logger
from src.messages import Messages

SECRET_KEY = config("SECRET_KEY", default="")
ALGORITHM = config("ALGORITHM", default="HS256")
EXCLUDED_PATHS = config("EXCLUDED_PATHS", default="", cast=lambda x: x.split(","))
AUTH_SERVICE_URL = config("AUTH_SERVICE_URL", default="")
AUTH_VERIFY_ENDPOINT = config(
    "AUTH_VERIFY_ENDPOINT",
    default="v1/token/validate",
)

logger = get_logger()


def deconstruct_auth_header(auth_header: str) -> tuple:
    """
    Deconstruct the Authorization header into its schema and token parts.
    """

    try:
        schema, token = auth_header.split()

    except (ValueError, AttributeError) as error:
        raise HTTPException(
            status_code=401,
            detail=Messages.JWT_ERROR_INVALID_HEADER,
        ) from error

    if not schema or not token:
        raise HTTPException(status_code=401, detail=Messages.JWT_ERROR_INVALID_HEADER)

    return schema, token


def create_jwt(data: dict, expires_delta: timedelta | None = None) -> str:
    """
    Create a JWT token with the given data and expiration time.
    """

    payload = deepcopy(data)

    delta = expires_delta or timedelta(minutes=15)
    expire = datetime.now(timezone.utc) + delta
    payload.update({"exp": expire})

    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)


def decode_jwt(token: str) -> dict:
    """
    Decode a JWT token and return the payload.
    """

    try:
        return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

    except jwt.ExpiredSignatureError as error:
        message = Messages.JWT_ERROR_EXPIRED

        raise ValueError(message) from error

    except jwt.InvalidTokenError as error:
        message = Messages.JWT_ERROR_INVALID_ACCESS_TOKEN

        raise ValueError(message) from error


async def is_service_up() -> bool:
    """
    Check if the authentication service is up and running.
    """

    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(AUTH_SERVICE_URL)
            response.raise_for_status()

        except httpx.RequestError:
            logger.exception("Error checking service health")
            return False

        return True


def validate_token(auth_header: str) -> bool:
    """
    Validate a JWT token locally.
    """

    try:
        _, token = deconstruct_auth_header(auth_header)
        decode_jwt(token)

    except ValueError as error:
        logger.exception("Error validating token")
        raise HTTPException(
            status_code=401,
            detail=str(error),
        ) from error

    return True


async def validate_token_against_service(auth_header: str) -> bool:
    """
    Validate a JWT token against the authentication service.
    """

    async with httpx.AsyncClient() as client:
        try:
            _, token = deconstruct_auth_header(auth_header)

        except ValueError as error:
            logger.exception("Error validating token (ValueError)")
            raise HTTPException(
                status_code=401,
                detail=str(error),
            ) from error

        try:
            response = await client.get(
                AUTH_SERVICE_URL + AUTH_VERIFY_ENDPOINT,
                headers={"Authorization": f"Bearer {token}"},
            )
            response.raise_for_status()

        except httpx.RequestError as error:
            logger.exception("Error validating token (httpx.RequestError)")
            raise HTTPException(
                status_code=503,
                detail="Authentication service is down",
            ) from error

        except httpx.HTTPStatusError as error:
            logger.exception("Error validating token (httpx.HTTPStatusError)")
            raise HTTPException(
                status_code=error.response.status_code,
                detail=error.response.json()["detail"],
            ) from error

        return True
