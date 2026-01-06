"""
Users - Endpoints.

This module contains the endpoints for the Users.
"""

from __future__ import annotations

from fastapi import APIRouter, Depends, File, Query, Response, UploadFile, status

from src.apps.users.enums import AvailableImagesEnum
from src.apps.users.messages import Messages
from src.apps.users.models import UsersModel
from src.apps.users.schemas import (
    UserDataSchema,
    UserEmailVerificationSchema,
    UserPublicSchema,
    UserSchema,
    UserUpdateDataSchema,
)
from src.apps.users.services import users
from src.libs.authentication.decorators import only_admin, only_user
from src.libs.pagination.schema import PaginatedSchema
from src.libs.schemas import MessageSchema

router = APIRouter()


@router.get(
    "/",
    responses={
        status.HTTP_200_OK: {
            "model": PaginatedSchema[UserSchema],
            "description": "List of users",
        },
    },
)
async def list_users(
    _user_info: UsersModel = Depends(only_admin),
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1),
) -> PaginatedSchema[UserSchema]:
    """
    List a page with users.

    This endpoint will return a object of a page the users in it.
    """

    return await users.list_users(page, limit)


@router.post(
    "/create",
    status_code=status.HTTP_201_CREATED,
    responses={
        status.HTTP_201_CREATED: {
            "model": UserSchema,
            "description": "User created successfully",
        },
        status.HTTP_400_BAD_REQUEST: {
            "model": MessageSchema,
            "description": Messages.Users.Error.NOT_CREATED,
            "content": {
                "application/json": {
                    "example": {
                        "detail": Messages.Users.Error.NOT_CREATED,
                    },
                },
            },
        },
    },
)
async def create_user(data: UserDataSchema) -> UserSchema:
    """
    Create a new user.

    This endpoint will create a new user with the provided data.
    """

    return await users.create_user(data)


@router.get(
    "/me",
    responses={
        status.HTTP_200_OK: {
            "model": UserSchema,
            "description": "User found",
        },
        status.HTTP_404_NOT_FOUND: {
            "model": MessageSchema,
            "description": Messages.Users.Error.NOT_FOUND,
            "content": {
                "application/json": {
                    "example": {
                        "detail": Messages.Users.Error.NOT_FOUND,
                    },
                },
            },
        },
    },
)
def get_my_user(
    user_info: UsersModel = Depends(only_user),
) -> UserSchema:
    """
    Get the authenticated user.

    This endpoint will return the user information of the authenticated user.

    ---

    It uses the `only_user` dependency to ensure that the user is authenticated.
    If the user is not authenticated, it will raise an HTTP 401 Unauthorized error.
    If the user is not found, it will raise an HTTP 404 Not Found error.
    """

    return UserSchema.from_model(
        user_info,
        relationship_recursively=True,
    )


@router.get(
    "/{user_id}",
    responses={
        status.HTTP_200_OK: {
            "model": UserPublicSchema,
            "description": "User found",
        },
        status.HTTP_404_NOT_FOUND: {
            "model": MessageSchema,
            "description": Messages.Users.Error.NOT_FOUND,
            "content": {
                "application/json": {
                    "example": {
                        "detail": Messages.Users.Error.NOT_FOUND,
                    },
                },
            },
        },
    },
)
def get_user(user_id: int | str) -> UserPublicSchema:
    """
    Get a user.

    This endpoint will return a user by its ID.
    """

    return users.get_user(user_id)


@router.patch(
    "/{user_id}",
    responses={
        status.HTTP_200_OK: {
            "model": UserSchema,
            "description": "User updated successfully",
        },
        status.HTTP_404_NOT_FOUND: {
            "model": MessageSchema,
            "description": Messages.Users.Error.NOT_FOUND,
            "content": {
                "application/json": {
                    "example": {
                        "detail": Messages.Users.Error.NOT_FOUND,
                    },
                },
            },
        },
    },
)
def update_user(
    user_id: int | str,
    data: UserUpdateDataSchema,
    current_user_info: UsersModel = Depends(only_user),
) -> UserSchema:
    """
    Update a user.

    This endpoint will update a user by its ID.

    ---

    It uses the `only_user` dependency to ensure that the user is authenticated.
    If the user access this route, it will check if it's the same user or an admin.
    If the user is not authenticated, it will raise an HTTP 401 Unauthorized error.
    If the user is not found, it will raise an HTTP 404 Not Found error.
    """

    return users.update_user(user_id, data, current_user_info)


@router.post(
    "/{user_id}/image",
    status_code=status.HTTP_201_CREATED,
    responses={
        status.HTTP_201_CREATED: {
            "model": UserSchema,
            "description": "User image updated successfully",
        },
        status.HTTP_404_NOT_FOUND: {
            "model": MessageSchema,
            "description": Messages.Users.Error.NOT_FOUND,
            "content": {
                "application/json": {
                    "example": {
                        "detail": Messages.Users.Error.NOT_FOUND,
                    },
                },
            },
        },
    },
)
async def update_user_image(
    user_id: int | str,
    image: UploadFile = File(...),
    type_of: AvailableImagesEnum = Query(...),
    current_user_info: UsersModel = Depends(only_user),
) -> UserSchema:
    """
    Update a user image.

    This endpoint will update a user image by its ID.

    ---

    It uses the `only_user` dependency to ensure that the user is authenticated.
    If the user access this route, it will check if it's the same user or an admin.
    If the user is not authenticated, it will raise an HTTP 401 Unauthorized error.
    If the user is not found, it will raise an HTTP 404 Not Found error.
    """

    return await users.update_user_image(
        user_id,
        type_of,
        image,
        current_user_info,
    )


@router.delete(
    "/{user_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    responses={
        status.HTTP_204_NO_CONTENT: {
            "description": "User deleted successfully",
        },
        status.HTTP_404_NOT_FOUND: {
            "model": MessageSchema,
            "description": Messages.Users.Error.NOT_FOUND,
            "content": {
                "application/json": {
                    "example": {
                        "detail": Messages.Users.Error.NOT_FOUND,
                    },
                },
            },
        },
    },
)
def delete_user(
    user_id: int | str,
    _user_info: UsersModel = Depends(only_admin),
) -> Response:
    """
    Delete a user.

    This endpoint will delete a user by its ID.

    TODO: This Response shouldn't be necessary, but something is wrong probably on
    the middlewares that are preventing FastAPI to return a 204 with no content.
    """

    users.delete_user(user_id)

    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.post(
    "/verify-email",
    responses={
        status.HTTP_200_OK: {
            "model": MessageSchema,
            "description": "Email verified successfully",
            "content": {
                "application/json": {
                    "example": {
                        "detail": Messages.Users.Success.EMAIL_VERIFIED,
                    },
                },
            },
        },
        status.HTTP_404_NOT_FOUND: {
            "model": MessageSchema,
            "description": Messages.Users.Error.INVALID_VERIFICATION_TOKEN,
            "content": {
                "application/json": {
                    "example": {
                        "detail": Messages.Users.Error.INVALID_VERIFICATION_TOKEN,
                    },
                },
            },
        },
    },
)
def verify_email(token: UserEmailVerificationSchema) -> MessageSchema:
    """
    Verify user email.

    This endpoint will verify the user email using the provided token.
    """

    return users.verify_email(token.token)
