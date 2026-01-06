"""
Roles - Services.

This module contains the services for the Roles.
"""

from __future__ import annotations

from fastapi import HTTPException, status

from src.apps.roles.messages import Messages
from src.apps.roles.models import RolesModel
from src.apps.roles.schemas import (
    RoleDataSchema,
    RoleSchema,
    RoleUpdateDataSchema,
)
from src.apps.roles.services.utils import get_permission_models, get_role_model
from src.libs.database.pagination import paginate
from src.libs.log import get_context as _
from src.libs.log import get_logger
from src.libs.pagination.schema import PaginatedSchema

log = get_logger()


async def list_roles(
    page: int,
    limit: int,
    allow_deleted: bool = False,
) -> PaginatedSchema[RoleSchema]:
    """
    Service - Paginate Roles.
    """

    log.debug(f"{_()}: Listing roles with page {page} and limit {limit}")

    filters = [RolesModel.deleted_at.is_(None)] if not allow_deleted else []

    return paginate(
        model=RolesModel,
        page=page,
        page_size=limit,
        schema=RoleSchema,
        filter=filters,
    )


def get_role(role_identifier: int | str) -> RoleSchema:
    """
    Service - Get role by ID or slug.
    """

    log.debug(f"{_()}: Getting role with ID or slug {role_identifier}")

    role = get_role_model(role_identifier, raise_error=True)

    return RoleSchema.from_model(role)


def create_role(data: RoleDataSchema) -> RoleSchema:
    """
    Service - Create a new role.

    This function will create a new role with the provided data.
    """

    log.debug(f"{_()}: Creating role with data: {data}")

    role = get_role_model(data.slug)

    if role:
        if role.deleted_at:
            role.restore()
            return update_role(role.id, data)

        message = Messages.Roles.Error.ALREADY_EXISTS
        log.error(f"{_()}: {message}")

        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=message,
        )

    payload = data.model_dump(exclude_unset=True)
    permissions_ids = payload.pop("permissions", [])

    # Creating Role Model
    role_model = RolesModel(**payload)
    role_model.save()

    # Adding Permissions
    if permissions_ids:
        permission_models = get_permission_models(permissions_ids)
        role_model.permissions = permission_models

    role_model.save()

    return RoleSchema.from_model(role_model)


def update_role(
    role_identifier: int | str,
    data: RoleDataSchema | RoleUpdateDataSchema,
) -> RoleSchema:
    """
    Service - Update a role.

    This function will update a role with the provided data.
    """

    log.debug(
        f"{_()}: Updating role with ID {role_identifier} and data: {data}",
    )

    role_model = get_role_model(role_identifier, raise_error=True)

    log.debug(f"{_()}: Updating role with data: {data}")

    if data.slug and get_role_model(data.slug) and data.slug != role_model.slug:
        message = Messages.Roles.Error.ALREADY_EXISTS
        log.error(f"{_()}: {message}")

        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=message,
        )

    payload = data.model_dump(exclude_unset=True)
    permissions_ids = payload.pop("permissions", [])

    # Updating the role model
    log.debug(f"{_()}: Updating role model with payload: {payload}")

    if payload:
        log.debug(f"{_()}: Setting attributes for role model: {payload}")

        for key, value in payload.items():
            setattr(role_model, key, value)

    # Updating permissions
    if permissions_ids:
        permissions = get_permission_models(permissions_ids)
        role_model.permissions = permissions
    else:
        role_model.permissions.clear()

    role_model.save()

    return RoleSchema.from_model(role_model)


def delete_role(
    role_identifier: int | str,
    hard_delete: bool = False,
) -> None:
    """
    Service - Delete a role.

    This function will delete a role by its ID or slug.
    """

    log.debug(f"{_()}: Deleting role with ID or slug {role_identifier}")

    role_model = get_role_model(role_identifier, raise_error=True)

    log.debug(f"{_()}: Role found: {role_model}")
    log.debug(f"{_()}: Deleting role from list.")

    try:
        log.debug(f"{_()}: Clearing permissions for role: {role_model}")

        role_model.permissions.clear()
        role_model.save()

        log.debug(f"{_()}: Deleting role from database: {role_model}")

        role_model.delete(soft=not hard_delete)

    except Exception as error:
        log.exception(f"{_()}: Error deleting role.")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=Messages.Roles.Error.NOT_DELETED,
        ) from error

    log.debug(f"{_()}: Role deleted from list: {role_model}")
