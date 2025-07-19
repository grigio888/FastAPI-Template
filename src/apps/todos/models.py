"""
To Do - Model.

This module contains the model for the To Do.
"""

import sqlalchemy as sa

from src.libs.database.base_model import BaseModel


class TodoModel(BaseModel):
    """
    TodoModel.

    This class represents the todo model.
    """

    __tablename__ = "todos"

    name = sa.Column(sa.String(255), nullable=False)
    percentage = sa.Column(sa.Float, default=0.0)
    description = sa.Column(sa.String(1000), nullable=True)
