"""
ToDo - Endpoints.

This module contains the endpoints for the ToDo.
"""

from fastapi import APIRouter, Query, status

from src.apps.users import services as users
from src.apps.users.schemas import UserDataSchema, UserSchema, UserUpdateDataSchema
from src.libs.pagination.schema import PaginatedSchema
from src.libs.schemas import MessageSchema
from src.messages import Messages

router = APIRouter(prefix="/users", tags=["Users"])


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
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1),
) -> PaginatedSchema[UserSchema]:
    """
    List a page with users.

    This endpoint will return a object of a page the users in it.
    """

    return await users.list_users(page, limit)


@router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    responses={
        status.HTTP_201_CREATED: {
            "model": UserSchema,
            "description": "User created successfully",
        },
        status.HTTP_400_BAD_REQUEST: {
            "model": MessageSchema,
            "description": Messages.USER_POST_ERROR,
            "content": {
                "application/json": {
                    "example": {
                        "detail": Messages.USER_POST_ERROR,
                    },
                },
            },
        },
    },
)
def create_user(data: UserDataSchema) -> UserSchema:
    """
    Create a new user.

    This endpoint will create a new user with the provided data.
    """

    return users.create_user(data)


@router.get(
    "/{user_id}",
    responses={
        status.HTTP_200_OK: {
            "model": UserSchema,
            "description": "User found",
        },
        status.HTTP_404_NOT_FOUND: {
            "model": MessageSchema,
            "description": Messages.USER_NOT_FOUND,
            "content": {
                "application/json": {
                    "example": {
                        "detail": Messages.USER_NOT_FOUND,
                    },
                },
            },
        },
    },
)
def get_user(user_id: int) -> UserSchema:
    """
    Get a user.

    This endpoint will return a user by its ID.
    """

    return users.get_user(user_id)


@router.put(
    "/{user_id}",
    responses={
        status.HTTP_200_OK: {
            "model": UserSchema,
            "description": "User updated successfully",
        },
        status.HTTP_404_NOT_FOUND: {
            "model": MessageSchema,
            "description": Messages.USER_NOT_FOUND,
            "content": {
                "application/json": {
                    "example": {
                        "detail": Messages.USER_NOT_FOUND,
                    },
                },
            },
        },
    },
)
def update_user(user_id: int, data: UserUpdateDataSchema) -> UserSchema:
    """
    Update a user.

    This endpoint will update a user by its ID.
    """

    return users.update_user(user_id, data)


@router.delete(
    "/{user_id}",
    status_code=204,
    responses={
        status.HTTP_204_NO_CONTENT: {
            "description": "User deleted successfully",
        },
        status.HTTP_404_NOT_FOUND: {
            "model": MessageSchema,
            "description": Messages.USER_NOT_FOUND,
            "content": {
                "application/json": {
                    "example": {
                        "detail": Messages.USER_NOT_FOUND,
                    },
                },
            },
        },
    },
)
def delete_user(user_id: int) -> None:
    """
    Delete a user.

    This endpoint will delete a user by its ID.
    """

    users.delete_user(user_id)
