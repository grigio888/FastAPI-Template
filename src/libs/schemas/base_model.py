"""
Schemas - Base Model.

This module will define the base model for all schemas.
"""

from typing import TYPE_CHECKING, Self, TypeVar

if TYPE_CHECKING:
    from src.libs.database.base_model import BaseModel as DBBaseModel

from pydantic import BaseModel as PydanticBaseModel

T = TypeVar("T", bound="BaseModel")


class BaseModel(PydanticBaseModel):
    """
    Base model.
    """

    @classmethod
    def from_model(cls, model: "DBBaseModel") -> Self:
        """
        Convert a SQLAlchemy model to a Pydantic model.
        """

        return cls(**model.to_dict())
