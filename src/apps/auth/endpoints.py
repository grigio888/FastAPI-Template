"""
Authentication - Endpoints.

This module contains the endpoints for the Users.
"""

from fastapi import APIRouter, Depends, Header, Security, status
from fastapi.security import APIKeyHeader

from src.apps.auth import services
from src.apps.auth.schemas import TokensSchema
from src.apps.auth.utils import get_basic_token
from src.apps.users.messages import Messages as UsersMessages
from src.libs.authentication.messages import Messages
from src.libs.schemas.messages import MessageSchema

router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    responses={
        status.HTTP_201_CREATED: {
            "model": TokensSchema,
            "description": Messages.JWT_GENERATED,
        },
        status.HTTP_400_BAD_REQUEST: {
            "model": MessageSchema,
            "description": "Bad request scenarios.",
            "content": {
                "application/json": {
                    "examples": {
                        "invalid_type": {
                            "value": {
                                "detail": Messages.JWT_INVALID_TYPE,
                            },
                            "summary": Messages.JWT_INVALID_TYPE,
                        },
                        "invalid_structure": {
                            "value": {
                                "detail": Messages.JWT_INVALID_STRUCTURE,
                            },
                            "summary": Messages.JWT_INVALID_STRUCTURE,
                        },
                    },
                },
            },
        },
        status.HTTP_401_UNAUTHORIZED: {
            "model": MessageSchema,
            "description": "Unauthorized scenarios.",
            "content": {
                "application/json": {
                    "examples": {
                        "invalid_credentials": {
                            "value": {
                                "detail": Messages.INVALID_CREDENTIALS,
                            },
                            "summary": Messages.INVALID_CREDENTIALS,
                        },
                    },
                },
            },
        },
        status.HTTP_500_INTERNAL_SERVER_ERROR: {
            "model": MessageSchema,
            "description": Messages.GENERIC_ERROR,
            "content": {
                "application/json": {
                    "example": {
                        "detail": Messages.GENERIC_ERROR,
                    },
                },
            },
        },
    },
)
async def generate_token(
    basic_token: str = Depends(get_basic_token),
) -> TokensSchema:
    """
    Generate a pair of tokens.

    It receives the user data and returns a pair of tokens (access and refresh).
    """

    return await services.generate_token(
        basic_token=basic_token,
    )


@router.put(
    "/",
    responses={
        status.HTTP_200_OK: {
            "model": TokensSchema,
            "description": Messages.JWT_REFRESHED,
        },
        status.HTTP_400_BAD_REQUEST: {
            "model": MessageSchema,
            "description": Messages.INVALID_CREDENTIALS,
            "content": {
                "application/json": {
                    "examples": {
                        "invalid_token_type": {
                            "summary": Messages.JWT_INVALID_TYPE,
                            "value": {
                                "detail": Messages.JWT_INVALID_TYPE,
                            },
                        },
                        "invalid_credentials": {
                            "summary": Messages.INVALID_CREDENTIALS,
                            "value": {
                                "detail": Messages.INVALID_CREDENTIALS,
                            },
                        },
                    },
                },
            },
        },
        status.HTTP_401_UNAUTHORIZED: {
            "model": MessageSchema,
            "description": "Unauthorized scenarios.",
            "content": {
                "application/json": {
                    "examples": {
                        "invalid_token_structure": {
                            "summary": Messages.JWT_INVALID_STRUCTURE,
                            "value": {
                                "detail": Messages.JWT_INVALID_STRUCTURE,
                            },
                        },
                        "user_not_found": {
                            "summary": UsersMessages.Users.Error.NOT_FOUND,
                            "value": {
                                "detail": UsersMessages.Users.Error.NOT_FOUND,
                            },
                        },
                    },
                },
            },
        },
        status.HTTP_500_INTERNAL_SERVER_ERROR: {
            "model": MessageSchema,
            "description": Messages.GENERIC_ERROR,
            "content": {
                "application/json": {
                    "example": {
                        "detail": Messages.GENERIC_ERROR,
                    },
                },
            },
        },
    },
)
def refresh_token(
    refreshtoken: str = Header(...),
) -> TokensSchema:
    """
    Refresh the access token.

    It receives the refresh token and returns a new access token.
    """

    return services.refresh_token(
        refreshtoken=refreshtoken,
    )


@router.delete(
    "/",
    status_code=status.HTTP_204_NO_CONTENT,
    responses={
        status.HTTP_204_NO_CONTENT: {
            "description": Messages.JWT_REVOKED,
        },
        status.HTTP_400_BAD_REQUEST: {
            "model": MessageSchema,
            "description": Messages.JWT_EXPIRED,
            "content": {
                "application/json": {
                    "example": {
                        "detail": Messages.JWT_EXPIRED,
                    },
                },
            },
        },
        status.HTTP_401_UNAUTHORIZED: {
            "model": MessageSchema,
            "description": "Unauthorized scenarios.",
            "content": {
                "application/json": {
                    "examples": {
                        "invalid_header": {
                            "summary": Messages.JWT_INVALID_HEADER,
                            "value": {
                                "detail": Messages.JWT_INVALID_HEADER,
                            },
                        },
                        "invalid_token_structure": {
                            "summary": Messages.JWT_INVALID_STRUCTURE,
                            "value": {
                                "detail": Messages.JWT_INVALID_STRUCTURE,
                            },
                        },
                        "invalid_access_token": {
                            "summary": Messages.JWT_INVALID_ACCESS_TOKEN,
                            "value": {
                                "detail": Messages.JWT_INVALID_ACCESS_TOKEN,
                            },
                        },
                        "invalid_token": {
                            "summary": Messages.JWT_INVALID,
                            "value": {
                                "detail": Messages.JWT_INVALID,
                            },
                        },
                        "token_expired": {
                            "summary": Messages.JWT_EXPIRED,
                            "value": {
                                "detail": Messages.JWT_EXPIRED,
                            },
                        },
                        "user_not_found": {
                            "summary": UsersMessages.Users.Error.NOT_FOUND,
                            "value": {
                                "detail": UsersMessages.Users.Error.NOT_FOUND,
                            },
                        },
                        "token_not_revoked": {
                            "summary": Messages.JWT_NOT_REVOKED,
                            "value": {
                                "detail": Messages.JWT_NOT_REVOKED,
                            },
                        },
                    },
                },
            },
        },
        status.HTTP_500_INTERNAL_SERVER_ERROR: {
            "model": MessageSchema,
            "description": Messages.GENERIC_ERROR,
            "content": {
                "application/json": {
                    "example": {
                        "detail": Messages.GENERIC_ERROR,
                    },
                },
            },
        },
    },
)
def revoke_token(
    authorization: str = Security(
        APIKeyHeader(name="Authorization"),
    ),
) -> None:
    """
    Revoke the access token.

    It receives the refresh token and revokes both tokens.
    """

    services.revoke_token(
        authorization=authorization,
    )
