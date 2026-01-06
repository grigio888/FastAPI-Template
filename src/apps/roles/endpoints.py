"""
Roles - Endpoints.

This module contains the endpoints for the Roles.
"""

from fastapi import APIRouter, Depends, Query, status

from src.apps.roles import services as roles
from src.apps.roles.messages import Messages
from src.apps.roles.schemas import RoleDataSchema, RoleSchema, RoleUpdateDataSchema
from src.apps.users.models import UsersModel
from src.libs.authentication.decorators import only_admin
from src.libs.pagination.schema import PaginatedSchema
from src.libs.schemas import MessageSchema

router = APIRouter(
    prefix="/roles",
    tags=["Users - Roles"],
)


@router.get(
    "/",
    responses={
        status.HTTP_200_OK: {
            "model": PaginatedSchema[RoleSchema],
            "description": "List of roles",
        },
    },
)
async def list_roles(
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1),
    _user_info: UsersModel = Depends(only_admin),
) -> PaginatedSchema[RoleSchema]:
    """
    List a page with roles.

    This endpoint will return a object of a page the roles in it.
    """

    return await roles.list_roles(page, limit)


@router.post(
    "/create",
    status_code=status.HTTP_201_CREATED,
    responses={
        status.HTTP_201_CREATED: {
            "model": RoleSchema,
            "description": "Role created successfully",
        },
        status.HTTP_400_BAD_REQUEST: {
            "model": MessageSchema,
            "description": Messages.Roles.Error.NOT_CREATED,
            "content": {
                "application/json": {
                    "example": {
                        "detail": Messages.Roles.Error.NOT_CREATED,
                    },
                },
            },
        },
    },
)
def create_role(
    data: RoleDataSchema,
    _user_info: UsersModel = Depends(only_admin),
) -> RoleSchema:
    """
    Create a new role.

    This endpoint will create a new role with the provided data.
    """

    return roles.create_role(data)


@router.get(
    "/{role_id}",
    responses={
        status.HTTP_200_OK: {
            "model": RoleSchema,
            "description": "Role found",
        },
        status.HTTP_404_NOT_FOUND: {
            "model": MessageSchema,
            "description": Messages.Roles.Error.NOT_FOUND,
            "content": {
                "application/json": {
                    "example": {
                        "detail": Messages.Roles.Error.NOT_FOUND,
                    },
                },
            },
        },
    },
)
def get_role(
    role_id: int,
    _user_info: UsersModel = Depends(only_admin),
) -> RoleSchema:
    """
    Get a role.

    This endpoint will return a role by its ID.
    """

    return roles.get_role(role_id)


@router.patch(
    "/{role_id}",
    responses={
        status.HTTP_200_OK: {
            "model": RoleSchema,
            "description": "Role updated successfully",
        },
        status.HTTP_404_NOT_FOUND: {
            "model": MessageSchema,
            "description": Messages.Roles.Error.NOT_FOUND,
            "content": {
                "application/json": {
                    "example": {
                        "detail": Messages.Roles.Error.NOT_FOUND,
                    },
                },
            },
        },
    },
)
def update_role(
    role_id: int,
    data: RoleUpdateDataSchema,
    _user_info: UsersModel = Depends(only_admin),
) -> RoleSchema:
    """
    Update a role.

    This endpoint will update a role by its ID.
    """

    return roles.update_role(role_id, data)


@router.delete(
    "/{role_id}",
    status_code=204,
    responses={
        status.HTTP_204_NO_CONTENT: {
            "description": "Role deleted successfully",
        },
        status.HTTP_404_NOT_FOUND: {
            "model": MessageSchema,
            "description": Messages.Roles.Error.NOT_FOUND,
            "content": {
                "application/json": {
                    "example": {
                        "detail": Messages.Roles.Error.NOT_FOUND,
                    },
                },
            },
        },
    },
)
def delete_role(
    role_id: int,
    _user_info: UsersModel = Depends(only_admin),
) -> None:
    """
    Delete a role.

    This endpoint will delete a role by its ID.
    """

    roles.delete_role(role_id)
