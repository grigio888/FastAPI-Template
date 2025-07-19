"""
ToDo - Service.

This module contains the business logic for the todo service.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from fastapi import HTTPException, status

if TYPE_CHECKING:
    from src.libs.pagination.schema import PaginatedSchema

from src.apps.users.models import UsersModel
from src.apps.users.schemas import (
    UserDataSchema,
    UserSchema,
    UserUpdateDataSchema,
)
from src.libs.authentication.middleware.hash import hash_sha512
from src.libs.database.pagination import paginate
from src.libs.log import get_context as _
from src.libs.log import get_logger
from src.messages import Messages

log = get_logger()


async def list_users(page: int, limit: int) -> PaginatedSchema:
    """
    Paginate users.
    """

    log.debug(f"{_()}: Listing users with page {page} and limit {limit}")

    return paginate(
        model=UsersModel,
        page=page,
        page_size=limit,
        schema=UserSchema,
        filter=[UsersModel.deleted_at.is_(None)],
    )


def get_user(user_id: int) -> UserSchema:
    """
    Get user by ID.
    """

    log.debug(f"{_()}: Getting user with ID {user_id}")

    user = UsersModel.query().get(user_id)

    if not user:
        message = Messages.USER_NOT_FOUND
        log.error(f"{_()}: {message}")

        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=message,
        )

    log.debug(f"{_()}: User found: {user}")

    return UserSchema.from_model(user)


def create_user(data: UserDataSchema) -> UserSchema:
    """
    Create a new user.

    This function will create a new user with the provided data.
    """

    log.debug(f"{_()}: Creating user with data: {data}")

    if UsersModel.query().filter(UsersModel.email == data.email).first():
        message = Messages.USER_POST_ERROR_EMAIL_EXISTS
        log.error(f"{_()}: {message}")

        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=message,
        )

    payload = data.model_dump(exclude_unset=True)

    payload["password"] = hash_sha512(payload["password"])

    user_model = UsersModel(
        **payload,
    )

    user_model.save()

    return UserSchema.from_model(user_model)


def update_user(user_id: int, data: UserUpdateDataSchema) -> UserSchema:
    """
    Update a user.

    This function will update a user with the provided data.
    """

    log.debug(f"{_()}: Updating user with ID {user_id} and data: {data}")

    user_model = UsersModel.query().get(user_id)

    if not user_model:
        message = Messages.USER_NOT_FOUND
        log.error(f"{_()}: {message}")

        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=message,
        )

    log.debug(f"{_()}: User found: {user_model}")
    log.debug(f"{_()}: Updating user with data: {data}")

    payload = data.model_dump(exclude_unset=True)

    if "password" in payload:
        payload["password"] = hash_sha512(payload["password"])

    for key, value in payload.items():
        setattr(user_model, key, value)

    return UserSchema.from_model(user_model)


def delete_user(user_id: int) -> None:
    """
    Delete a user.

    This function will delete a user by its ID.
    """

    log.debug(f"{_()}: Deleting user with ID {user_id}")

    user_model = UsersModel.query().get(user_id)

    if not user_model:
        message = Messages.USER_NOT_FOUND
        log.error(f"{_()}: {message}")

        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=message,
        )

    log.debug(f"{_()}: User found: {user_model}")
    log.debug(f"{_()}: Deleting user from list.")

    user_model.delete()

    log.debug(f"{_()}: User deleted from list: {user_model}")
