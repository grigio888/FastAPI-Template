"""
Roles - Services.

This module contains the services for the Roles.
"""

from __future__ import annotations

from typing import Literal, overload

from fastapi import HTTPException, status
from sqlalchemy import or_

from src.apps.roles.messages import Messages
from src.apps.roles.models import PermissionsModel, RolesModel
from src.libs.log import get_context as _
from src.libs.log import get_logger

log = get_logger()


@overload
def get_role_model(
    role_identifier: int | str,
    *,
    raise_error: Literal[True],
) -> RolesModel: ...
@overload
def get_role_model(
    role_identifier: int | str,
    *,
    raise_error: Literal[False] = ...,
) -> RolesModel | None: ...
def get_role_model(
    role_identifier: int | str,
    raise_error: bool = False,
) -> RolesModel | None:
    """
    Get role model by ID or slug.
    """

    log.debug(f"{_()}: Getting role with ID or slug {role_identifier}")

    model = None

    if isinstance(role_identifier, int) or (
        isinstance(role_identifier, str) and role_identifier.isdigit()
    ):
        model = RolesModel.get(int(role_identifier))
    else:
        model = (
            RolesModel.query()
            .filter(
                RolesModel.slug == role_identifier,
            )
            .first()
        )

    if not model and raise_error:
        message = Messages.Roles.Error.NOT_FOUND
        log.error(f"{_()}: {message}")

        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=message,
        )

    log.debug(f"{_()}: Role found: {model}")

    return model


@overload
def get_permission_models(
    permission_identifier: int | str,
    *,
    raise_error: Literal[True],
) -> list[PermissionsModel]: ...
@overload
def get_permission_models(
    permission_identifier: int | str,
    *,
    raise_error: Literal[False] = ...,
) -> list[PermissionsModel] | None: ...
@overload
def get_permission_models(
    permission_identifier: list[int | str],
    *,
    raise_error: Literal[True],
) -> list[PermissionsModel]: ...
@overload
def get_permission_models(
    permission_identifier: list[int | str],
    *,
    raise_error: Literal[False] = ...,
) -> list[PermissionsModel] | None: ...
def get_permission_models(
    permission_identifier: int | str | list[int | str],
    raise_error: bool = False,
) -> list[PermissionsModel]:
    """
    Get permission model by ID or slug.
    """

    log.debug(f"{_()}: Getting permission with ID or slug {permission_identifier}")

    filters = []

    if not isinstance(permission_identifier, list):
        permission_identifier = [permission_identifier]

    for perm in permission_identifier:
        if isinstance(perm, int) or (isinstance(perm, str) and perm.isdigit()):
            filters.append(PermissionsModel.id == int(perm))
        else:
            filters.append(PermissionsModel.permission == perm)

    models = PermissionsModel.query().filter(or_(*filters)).all()

    if not models and raise_error:
        message = Messages.Permissions.Error.NOT_FOUND
        log.error(f"{_()}: {message}")

        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=message,
        )

    log.debug(f"{_()}: Permissions found: {models}")

    return models
