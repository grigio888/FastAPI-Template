"""
Authentication - Services.

This module contains the services for the User's Authentication.
"""

from fastapi import HTTPException, status

from src.apps.auth.schemas import AuthSchema, TokensSchema
from src.apps.auth.utils import (
    create_pair_tokens,
    create_token,
    delete_token_pair,
    get_token_data,
    link_tokens,
    revoke_tokens_from_redis,
    set_pair_tokens,
    set_token,
    validate_token_info,
    validate_user,
)
from src.apps.users.messages import Messages as UsersMessages
from src.libs.authentication.messages import Messages
from src.libs.authentication.middleware.utils import deconstruct_auth_header
from src.libs.log import get_context as _
from src.libs.log import get_logger
from src.libs.redis import RedisClient

log = get_logger()
redis = RedisClient()


async def generate_token(
    basic_token: str,
) -> TokensSchema:
    """
    Generate a pair of tokens.

    It receives the basic token and returns a pair of tokens.
    """

    log.info(f"{_()}: Generating token for {basic_token}")

    user = validate_user(basic_token)

    tokens = create_pair_tokens(user)

    set_pair_tokens(
        {
            "authorization": tokens.access_token,
            "refreshtoken": tokens.refresh_token,
        },
        user.username,
    )
    link_tokens(
        tokens.access_token,
        tokens.refresh_token,
        user.username,
    )

    return tokens


def refresh_token(
    refreshtoken: str,
) -> TokensSchema:
    """
    Refresh the access token.

    It receives the refresh token and returns a new access token.
    """

    token_data = get_token_data(refreshtoken)

    if not token_data:
        log.error(f"{_()}: USER_NOT_FOUND. User not found in redis")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=UsersMessages.Users.Error.NOT_FOUND,
        )

    user = AuthSchema(username=token_data["email"])

    # Creating a new access token.
    new_access_token = create_token(user, "access")

    # Revoking the old access token
    revoke_tokens_from_redis([token_data["pair"]])

    set_token(
        new_access_token.access_token,  # type: ignore[union-attr]
        user.username,
        "access",
    )
    link_tokens(
        new_access_token.access_token,  # type: ignore[union-attr]
        refreshtoken,
        user.username,
    )

    log.debug(f"{_()}: Tokens refreshed successfully")

    return TokensSchema(
        access_token=new_access_token.access_token,  # type: ignore[union-attr]
        refresh_token=refreshtoken,
        detail=Messages.JWT_REFRESHED,
    )


def revoke_token(
    authorization: str,
) -> None:
    """
    Revoke the access token.

    It receives the refresh token and revokes both tokens.
    """

    _a_schema, access_token = deconstruct_auth_header(authorization)

    # Retrieving the user information from redis.
    decoded_token = validate_token_info(access_token)
    token_pattern = f"{decoded_token['sub']}:{access_token}"
    token_data = redis.get(token_pattern)

    if not token_data:
        message = UsersMessages.Users.Error.NOT_FOUND
        log.error(f"{_()}: {message}")

        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=message,
        )

    if not delete_token_pair(access_token, token_data["pair"]):
        message = Messages.JWT_NOT_REVOKED
        log.error(f"{_()}: {message}")

        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=message,
        )
