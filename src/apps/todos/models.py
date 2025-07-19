"""
ToDo - Model.

This module contains the model for the todo.
"""

import sqlalchemy as sa

from src.libs.database.base_model import BaseModel


class TodoModel(BaseModel):
    """
    TodoModel.

    This class represents the todo model.
    """

    __tablename__ = "todos"

    id = sa.Column(sa.Integer, primary_key=True)

    name = sa.Column(sa.String(255), nullable=False)
    percentage = sa.Column(sa.Float, default=0.0)
    description = sa.Column(sa.String(1000), nullable=True)

    created_at = sa.Column(sa.DateTime, server_default=sa.text("CURRENT_TIMESTAMP"))
    updated_at = sa.Column(
        sa.DateTime,
        server_default=sa.text("CURRENT_TIMESTAMP"),
        onupdate=sa.text("CURRENT_TIMESTAMP"),
    )
    deleted_at = sa.Column(sa.DateTime, nullable=True)
