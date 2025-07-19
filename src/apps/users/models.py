"""
ToDo - Model.

This module contains the model for the todo.
"""

import sqlalchemy as sa

from src.libs.database.base_model import BaseModel


class UsersModel(BaseModel):
    """
    Users.

    This class represents the users model.
    """

    __tablename__ = "users"

    name = sa.Column(sa.String(255), nullable=False)
    email = sa.Column(sa.String(255), nullable=False, unique=True)
    password = sa.Column(sa.String(255), nullable=False)

    is_active = sa.Column(sa.Boolean, default=True)
    is_superuser = sa.Column(sa.Boolean, default=False)
