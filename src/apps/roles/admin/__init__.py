"""
Roles - Admin.

This module contains the admin views for the Roles app.
"""

from typing import ClassVar

from src.apps.roles.models import PermissionsModel, RolesModel
from src.libs.admin.views.model_view import CustomModelView


class RolesAdmin(  # type: ignore[call-arg]
    CustomModelView,
    model=RolesModel,
):
    """
    Admin view for the Roles model.
    """

    column_list: ClassVar = [
        RolesModel.id,
        RolesModel.slug,
        RolesModel.title,
    ]
    column_searchable_list: ClassVar = [
        RolesModel.id,
        RolesModel.slug,
        RolesModel.title,
    ]
    column_sortable_list: ClassVar = [
        RolesModel.id,
        RolesModel.slug,
        RolesModel.title,
    ]
    column_default_sort: ClassVar = [
        (RolesModel.id, False),
        (RolesModel.slug, False),
        (RolesModel.title, False),
    ]

    category: str = "Roles"
    category_icon: str = "fa-solid fa-gavel"

    name: str = "Role"
    name_plural: str = "Roles"
    icon: str = "fa-solid fa-gavel"


class PermissionsAdmin(  # type: ignore[call-arg]
    CustomModelView,
    model=PermissionsModel,
):
    """
    Admin view for the Permissions model.
    """

    column_list: ClassVar = [
        PermissionsModel.id,
        PermissionsModel.permission,
    ]
    column_searchable_list: ClassVar = [
        PermissionsModel.id,
        PermissionsModel.permission,
    ]
    column_sortable_list: ClassVar = [
        PermissionsModel.id,
        PermissionsModel.permission,
    ]
    column_default_sort: ClassVar = [
        (PermissionsModel.id, False),
        (PermissionsModel.permission, False),
    ]

    category: str = "Roles"
    category_icon: str = "fa-solid fa-gavel"

    name: str = "Permission"
    name_plural: str = "Permissions"
    icon: str = "fa-solid fa-gavel"
