"""
Users - Service.

This module contains the business logic for the Users service.
"""

from __future__ import annotations

from pathlib import Path
from typing import TYPE_CHECKING

from fastapi import HTTPException, UploadFile, status
from sqlalchemy import or_

if TYPE_CHECKING:
    from src.libs.pagination.schema import PaginatedSchema

from src.apps.roles.models import RolesModel
from src.apps.users.messages import Messages
from src.apps.users.models import UsersModel
from src.apps.users.schemas import (
    UserDataSchema,
    UserPublicSchema,
    UserSchema,
    UserUpdateDataSchema,
)
from src.apps.users.utils import generate_random_name
from src.libs.authentication.middleware.hash import generate_random_string, hash_sha512
from src.libs.database.pagination import paginate
from src.libs.email import EmailController
from src.libs.image import ImageHandler
from src.libs.log import get_context as _
from src.libs.log import get_logger
from src.libs.schemas.messages import MessageSchema
from src.settings import Settings

log = get_logger()

DEFAULT_USER_ROLE_SLUG = "user"


def get_user_model(
    user_identifier: int | str,
    raise_error: bool = True,
) -> UsersModel:
    """
    Get user model by ID or email.
    """

    log.debug(f"{_()}: Getting user model with identifier: {user_identifier}")

    filters = [UsersModel.deleted_at.is_(None)]

    if isinstance(user_identifier, int) or user_identifier.isdigit():
        filters.append(UsersModel.id == user_identifier)
    else:
        identifier = user_identifier.lower()

        filters.append(
            or_(
                UsersModel.email.ilike(identifier),
                UsersModel.username.ilike(identifier),
            ),
        )

    user = UsersModel.query().filter(*filters).first()

    if not user and raise_error:
        message = Messages.Users.Error.NOT_FOUND
        log.error(f"{_()}: {message}")

        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=message,
        )

    log.debug(f"{_()}: User model found: {user}")

    return user


def check_permissions(
    user_model: UsersModel,
    current_user_info: UsersModel,
) -> None:
    """
    Check if the user has permission to perform an action.
    """

    log.debug(f"{_()}: Checking permissions for user: {current_user_info}")

    def has_permission(user: UsersModel, permission_slug: str) -> bool:
        role = getattr(user, "role", None)
        if not role:
            return False

        permissions = getattr(role, "permissions", [])
        return any(
            getattr(permission, "permission", None) == permission_slug
            for permission in permissions
        )

    if current_user_info.id != user_model.id and not has_permission(
        current_user_info,
        "admin",
    ):
        message = Messages.Users.Error.NOT_AUTHORIZED
        log.error(f"{_()}: {message}")

        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=message,
        )


def check_duplicates(
    payload: dict,
    existing_model: UsersModel | None = None,
) -> None:
    """
    Check for duplicate users.
    """

    log.debug(f"{_()}: Checking for duplicates with data: {payload}")

    def check_field(
        field: str,
        payload: dict,
        model: UsersModel | None = None,
    ) -> bool:
        """
        Check for duplicates in a specific field.

        Returns True if a duplicate is found, False otherwise.
        """
        if not payload.get(field):
            return False

        if not (fetch := get_user_model(payload[field], raise_error=False)):
            return False

        return not (model and fetch.id == model.id)

    fields = {
        "email": Messages.Users.Error.EMAIL_ALREADY_EXISTS,
        "username": Messages.Users.Error.USERNAME_ALREADY_EXISTS,
    }

    for field, error_message in fields.items():
        if check_field(field, payload, existing_model):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=error_message,
            )


# -- Services
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


def get_user(user_id: int | str) -> UserPublicSchema:
    """
    Get user by ID.
    """

    log.debug(f"{_()}: Getting user with ID {user_id}")

    user = get_user_model(user_id)

    log.debug(f"{_()}: User found: {user}")

    return UserPublicSchema.from_model(
        user,
        relationship_recursively=True,
    )


async def create_user(data: UserDataSchema) -> UserSchema:
    """
    Create a new user.

    This function will create a new user with the provided data.
    """

    log.debug(f"{_()}: Creating user with data: {data}")

    payload = data.model_dump(exclude_unset=True)

    check_duplicates(payload)

    if payload.get("password"):
        payload["password"] = hash_sha512(payload["password"])

    if not payload.get("role_id"):
        default_role = RolesModel.query().filter_by(slug=DEFAULT_USER_ROLE_SLUG).first()

        if not default_role:
            message = Messages.Users.Error.NOT_CREATED
            log.error(
                f"{_()}: Default role '{DEFAULT_USER_ROLE_SLUG}' not found for user "
                "creation.",
            )

            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=message,
            )

        payload["role_id"] = default_role.id

    user_model = UsersModel(
        **payload,
        username=await generate_random_name(),
    )

    user_model.save(flush=True)

    log.debug(f"{_()}: User created: {user_model}")
    log.debug(f"{_()}: Generating verification token for user.")

    token = generate_random_string(size=100)
    user_model.verification_token = token
    user_model.save()

    log.debug(f"{_()}: Verification token generated.")
    log.debug(f"{_()}: Sending verification email to user.")

    email = EmailController()
    email.send_email_confirmation(
        to_email=user_model.email,
        token=token,
    )

    log.debug(f"{_()}: Verification email sent to user.")

    return UserSchema.from_model(
        user_model,
        relationship_recursively=True,
    )


def update_user(
    user_id: int | str,
    data: UserUpdateDataSchema,
    current_user_info: UsersModel,
) -> UserSchema:
    """
    Update a user.

    This function will update a user with the provided data.
    """

    log.debug(f"{_()}: Updating user with ID {user_id} and data: {data}")

    user_model = get_user_model(user_id)
    check_permissions(user_model, current_user_info)

    log.debug(f"{_()}: User found: {user_model}")
    log.debug(f"{_()}: Updating user with data: {data}")

    payload = data.model_dump(exclude_unset=True, exclude_none=True)

    if payload.get("password"):
        payload["password"] = hash_sha512(payload["password"])

    check_duplicates(payload, existing_model=user_model)

    preferences_data = payload.pop("preferences", None)
    if preferences_data:
        for key, value in preferences_data.items():
            setattr(user_model.preferences, key, value)

    for key, value in payload.items():
        setattr(user_model, key, value)

    user_model.save()

    return UserSchema.from_model(
        user_model,
        relationship_recursively=True,
    )


async def update_user_image(
    user_id: int | str,
    type_of: str,
    image: UploadFile,
    current_user_info: UsersModel,
) -> UserSchema:
    """
    Update a user's images.

    This function will update a user's avatar and banner images.
    """

    log.debug(f"{_()}: Updating user images with ID {user_id}")

    user_model = get_user_model(user_id)
    check_permissions(user_model, current_user_info)

    log.debug(f"{_()}: User found: {user_model}")
    log.debug(f"{_()}: Updating user {type_of} image.")

    # Manipulate image
    image_path = Settings.PATH_IMAGE_USER.replace("USER_ID", str(user_id))
    image_path = Path(image_path)  # type: ignore[assignment]

    image_obj = ImageHandler(
        file=image,
        path=image_path,
    )
    image_url = await image_obj.save()

    if other_file := getattr(user_model, type_of):
        image_obj.delete_other_file(
            file_path=other_file,
        )

    setattr(user_model, type_of, str(image_path / image_url))  # type: ignore[operator]
    user_model.save()

    return UserSchema.from_model(
        user_model,
        relationship_recursively=True,
    )


def verify_email(token: str) -> MessageSchema:
    """
    Verify user email.

    This function will verify the user email using the provided token.
    """

    log.debug(f"{_()}: Verifying email with token: {token}")

    user_model = (
        UsersModel.query()
        .filter_by(
            verification_token=token,
            deleted_at=None,
        )
        .first()
    )

    if not user_model:
        message = Messages.Users.Error.INVALID_VERIFICATION_TOKEN
        log.error(f"{_()}: {message}")

        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=message,
        )

    user_model.is_active = True
    user_model.verification_token = None
    user_model.save()

    log.debug(f"{_()}: Email verified for user: {user_model}")

    return MessageSchema(detail=Messages.Users.Success.EMAIL_VERIFIED)


def delete_user(user_id: int | str) -> None:
    """
    Delete a user.

    This function will delete a user by its ID.
    """

    log.debug(f"{_()}: Deleting user with ID {user_id}")

    user_model = get_user_model(user_id)

    log.debug(f"{_()}: User found: {user_model}")
    log.debug(f"{_()}: Deleting user from list.")

    user_model.delete()

    log.debug(f"{_()}: User deleted from list: {user_model}")
