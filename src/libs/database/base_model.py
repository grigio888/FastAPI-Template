"""
Database - Base Model.

This module will define the base model for the Backend database.
"""

from __future__ import annotations

from datetime import UTC, datetime
from typing import TYPE_CHECKING, Self

import sqlalchemy as sa
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import DeclarativeBase, Session
from sqlalchemy.orm import Mapped as M  # noqa: N817
from sqlalchemy.orm import mapped_column as mc

from src.libs.database.session import get_session
from src.libs.log import get_logger

if TYPE_CHECKING:
    from sqlalchemy.orm import Query

log = get_logger()


class DeclarativeBaseModel(DeclarativeBase):
    """
    Declarative Base model.

    This model is used as base class for models and contain common fields.

    This base model, as it is, is supposed to be inherited by Models that are
    not supposed to have an auto-incrementing primary key (e.g., association tables).
    """

    __abstract__ = True

    created_at: M[datetime] = mc(server_default=sa.text("CURRENT_TIMESTAMP"))
    updated_at: M[datetime] = mc(
        server_default=sa.text("CURRENT_TIMESTAMP"),
        onupdate=sa.text("CURRENT_TIMESTAMP"),
    )
    deleted_at: M[datetime | None] = mc(nullable=True)

    @classmethod
    def __session__(cls) -> Session:
        """Return the session."""

        return get_session()

    @classmethod
    def query(cls) -> Query:
        """Return the query object for the model."""
        return cls.__session__().query(cls)

    def __repr__(self) -> str:
        """Stringfy Object."""
        return f"<{self.__table__}>"

    @classmethod
    def get(cls, target_id: int) -> Self | None:
        """
        Get the model.

        This method will get the model from the database based on the given id.
        """

        return cls.query().filter_by(id=target_id, deleted_at=None).first()

    def update(self, **kwargs: dict) -> None:
        """
        Update the model.

        This method will update the model with the given arguments.
        """

        flush = kwargs.pop("flush", False)

        for key, value in kwargs.items():
            setattr(self, key, value)

        if type(flush) is not bool:
            flush = False

        self.save(flush=flush)

    def save(self, flush: bool = False) -> None:
        """
        Save the model.

        This method will save the model to the database.
        """

        session = self.__session__()

        session.add(self)

        try:
            if flush:
                session.flush()
            else:
                session.commit()

        except SQLAlchemyError:
            session.rollback()
            log.exception("Failed to save model; rolled back transaction.")
            raise

    def delete(
        self,
        soft: bool = True,
        flush: bool = False,
    ) -> None:
        """
        Delete the model.

        This method will delete the model from the database.
        """

        session = self.__session__()

        if not hasattr(self, "deleted_at"):
            soft = False

        if soft:
            self.deleted_at = datetime.now(tz=UTC)
            session.add(self)

        else:
            session.delete(self)

        try:
            if flush:
                session.flush()
            else:
                session.commit()

        except SQLAlchemyError:
            session.rollback()
            log.exception("Failed to delete model; rolled back transaction.")
            raise

    def restore(self, flush: bool = False) -> None:
        """
        Restore the model.

        This method will restore the model from the soft delete.
        """

        self.deleted_at = None
        self.save(flush=flush)

    def to_dict(
        self,
        add_relationships: bool = True,
        recursively: bool = False,
    ) -> dict:
        """
        Convert the model to a dictionary.

        This method will convert the model to a dictionary.
        """
        data = {c.name: getattr(self, c.name) for c in self.__table__.columns}

        if add_relationships:
            for rel in self.__mapper__.relationships:
                value = getattr(self, rel.key)

                if value is not None:
                    if isinstance(value, list):
                        data[rel.key] = [
                            item.to_dict(add_relationships=recursively)
                            for item in value
                        ]

                    else:
                        data[rel.key] = value.to_dict(add_relationships=recursively)

        return data


class BaseModel(DeclarativeBaseModel):
    """
    Base model.

    This model is used as base class for all models and contain common fields,
    with addition of id column.

    This base model is the one suitable for use as a base class for all models.
    """

    __abstract__ = True

    id: M[int] = mc(primary_key=True, autoincrement=True)

    def __repr__(self) -> str:
        """Stringfy Object."""
        return f"<{self.__table__} - id:{self.id}>"
