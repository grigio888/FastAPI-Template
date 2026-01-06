"""
Authentication - Decorators.

This module contains decorators for authentication-related functionalities.
"""

from fastapi import HTTPException, Security, status
from fastapi.security import APIKeyHeader

from src.apps.roles.enums import RolesEnum
from src.apps.roles.messages import Messages as RoleMessages
from src.apps.users.messages import Messages as UserMessages
from src.apps.users.models import UsersModel
from src.libs.authentication.messages import Messages as AuthMessages
from src.libs.authentication.middleware.utils import (
    deconstruct_auth_header,
)
from src.libs.log import get_context as _
from src.libs.log import get_logger
from src.libs.redis import RedisClient

log = get_logger()
redis = RedisClient()


async def retrieve_user_info(
    authorization: str,
) -> UsersModel:
    """
    # Get User Info based on Authorization token.

    Return the user information based on the Authorization token.

    ---

    Args:
        authorization (str): The Authorization header from the request.

    Returns:
        UsersModel: The user information extracted from the token.

    Raises:
        HTTPException: If the token is invalid or user information cannot be retrieved.
            - **401**: AuthMessages.JWT_INVALID.
            - **401**: UserMessages.Users.Error.NOT_FOUND.
            - **404**: UserMessages.Users.Error.NOT_FOUND.

    """

    schema, token = deconstruct_auth_header(authorization)

    log.debug(f"{_()}: [{schema}] {token}")

    # Sanitizing AUTH_SERVICE_URL
    token_data = redis.search(f"*:{token}")

    if not token_data:
        message = AuthMessages.JWT_INVALID
        log.error(f"{_()}: {message}")

        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=message,
        )

    user_email = token_data[0].get("email")

    if not user_email:
        message = UserMessages.Users.Error.NOT_FOUND
        log.error(f"{_()}: {message}")

        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=message,
        )

    user_model = UsersModel.query().filter_by(email=user_email).first()

    if not user_model:
        message = UserMessages.Users.Error.NOT_FOUND
        log.error(f"{_()}: {message}")

        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=message,
        )

    return user_model


async def only_user(
    authorization: str = Security(
        APIKeyHeader(name="Authorization"),
    ),
) -> UsersModel:
    """
    # Protect route under User Authentication.

    Protects the route under the condition that the user is authenticated.

    If the user is authenticated, will return the UserModel based on the Authorization
    token.

    ---

    Args:
        authorization (str): The Authorization header from the request.

    Returns:
        UsersModel: The user information extracted from the token.

    Raises:
        HTTPException: If the token is invalid or user information cannot be retrieved.
            - Raises from `retrieve_user_info`

    ---

    ## Usage:

    ```
    @router.get("/user-info")
    def get_user_info(
        user_info: dict = Depends(only_user),
    ) -> UsersModel:
    ```

    """

    return await retrieve_user_info(
        authorization=authorization,
    )


async def only_moderators(
    authorization: str = Security(
        APIKeyHeader(name="Authorization"),
    ),
) -> UsersModel:
    """
    # Protect route under Moderator Authentication.

    Protects the route under the condition that the moderator is authenticated.

    If the moderator is authenticated, will return the UserModel based on the
    Authorization token.

    ---

    Args:
        authorization (str): The Authorization header from the request.

    Returns:
        UsersModel: The organizer information extracted from the token.

    Raises:
        HTTPException: If the token is invalid or moderator information cannot be
        retrieved.
            - Raises from `retrieve_user_info`

    ---

    ## Usage:

    ```
    @router.get("/user-info")
    def get_user_info(
        user_info: dict = Depends(only_moderators),
    ) -> UsersModel:
    ```

    """

    user_info = await retrieve_user_info(
        authorization=authorization,
    )

    if user_info.role.slug not in [RolesEnum.MODERATOR, RolesEnum.ADMIN]:
        message = RoleMessages.Permissions.Error.ONLY_MODERATORS
        log.error(f"{_()}: {message}")

        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=message,
        )

    return user_info


async def only_admin(
    authorization: str = Security(
        APIKeyHeader(name="Authorization"),
    ),
) -> UsersModel:
    """
    # Protect route under Admin Authentication.

    Protects the route under the condition that the admin is authenticated.

    If the admin is authenticated, will return the UserModel based on the Authorization
    token.

    ---

    Args:
        authorization (str): The Authorization header from the request.

    Returns:
        UsersModel: The admin information extracted from the token.

    Raises:
        HTTPException: If the token is invalid or admin information cannot be
        retrieved.
            - Raises from `retrieve_user_info`

    ---

    ## Usage:

    ```
    @router.get("/user-info")
    def get_user_info(
        user_info: dict = Depends(only_admin),
    ) -> UsersModel:
    ```

    """

    user_info = await retrieve_user_info(
        authorization=authorization,
    )

    if user_info.role.slug != RolesEnum.ADMIN:
        message = RoleMessages.Permissions.Error.ONLY_ADMIN
        log.error(f"{_()}: {message}")

        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=message,
        )

    return user_info
