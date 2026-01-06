"""
Users - Admin.

This module contains the admin views for the Users app.
"""

from typing import ClassVar

from fastapi import HTTPException

from src.apps.users.models import UserPreferencesModel, UsersModel
from src.apps.users.services.users import check_duplicates
from src.libs.admin.views.model_view import CustomModelView
from src.libs.authentication.middleware.hash import hash_sha512, is_hash_valid


class UsersAdmin(  # type: ignore[call-arg]
    CustomModelView,
    model=UsersModel,
):
    """
    Admin view for the Users model.
    """

    column_list: ClassVar = [
        UsersModel.id,
        UsersModel.email,
        UsersModel.first_name,
        UsersModel.last_name,
        UsersModel.is_active,
    ]
    column_searchable_list: ClassVar = [
        UsersModel.id,
        UsersModel.email,
        UsersModel.first_name,
        UsersModel.last_name,
    ]
    column_sortable_list: ClassVar = [
        UsersModel.id,
        UsersModel.email,
        UsersModel.first_name,
        UsersModel.last_name,
    ]
    column_default_sort: ClassVar = [
        (UsersModel.id, False),
        (UsersModel.email, False),
        (UsersModel.first_name, False),
        (UsersModel.last_name, False),
        (UsersModel.is_active, False),
    ]

    category: str = "Users"
    category_icon: str = "fa-solid fa-user"

    name: str = "User"
    name_plural: str = "Users"
    icon: str = "fa-solid fa-user"

    async def on_model_change(
        self,
        data: dict,
        model: UsersModel,
        *_args: list,
        **_kwargs: dict,
    ) -> None:
        """
        Handle changes to the model.
        """

        password = data.get("password")

        if not is_hash_valid(str(password)):
            data["password"] = hash_sha512(str(data["password"]))

        try:
            check_duplicates(
                data,
                existing_model=model if model and model.id else None,
            )

        except HTTPException as e:
            raise ValueError(e.detail) from e


class UserPreferencesAdmin(  # type: ignore[call-arg]
    CustomModelView,
    model=UserPreferencesModel,
):
    """
    Admin view for the Users model.
    """

    column_list: ClassVar = [
        UserPreferencesModel.id,
        UserPreferencesModel.user,
        UserPreferencesModel.theme,
        UserPreferencesModel.color,
        UserPreferencesModel.reading_mode,
        UserPreferencesModel.language,
    ]
    column_searchable_list: ClassVar = [
        UserPreferencesModel.id,
        UserPreferencesModel.user_id,
    ]
    column_sortable_list: ClassVar = [
        UserPreferencesModel.id,
        UserPreferencesModel.theme,
        UserPreferencesModel.color,
        UserPreferencesModel.reading_mode,
        UserPreferencesModel.language,
    ]
    column_default_sort: ClassVar = [
        (UserPreferencesModel.id, False),
        (UserPreferencesModel.theme, False),
        (UserPreferencesModel.color, False),
        (UserPreferencesModel.reading_mode, False),
        (UserPreferencesModel.language, False),
    ]

    category: str = "Users"
    category_icon: str = "fa-solid fa-user"

    name: str = "User's Preferences"
    name_plural: str = "Users' Preferences"
    icon: str = "fa-solid fa-user"
