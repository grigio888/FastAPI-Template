"""
Shiori - Database - Base Model.

This module will define the base model for the Shiori API database.
"""

from datetime import UTC, datetime
from typing import TYPE_CHECKING

from sqlalchemy.orm import DeclarativeBase

from src.libs.database.session import Session, get_session
from src.libs.log import get_logger

if TYPE_CHECKING:
    from sqlalchemy.orm import Query, sessionmaker

log = get_logger()


class BaseModel(DeclarativeBase):
    """
    Base model.

    This model will contain the base model for the Shiori API.
    """

    __abstract__ = True

    @classmethod
    def __session__(cls) -> "sessionmaker":
        """Return the session."""

        try:
            log.debug("db.base_model » Getting session.")
            db = get_session()
            log.debug("db.base_model » Session fetch.")

            if db is None:
                raise LookupError

        except LookupError:
            log.exception(
                "db.base_model » Operating outside app context. "
                "Multiple queries and/or relationships may not work properly.",
            )
            db = Session()

        return db

    @classmethod
    def query(cls) -> "Query":
        """Return the query object for the model."""
        return cls.__session__().query(cls)

    def __repr__(self) -> str:
        """Stringfy Object."""
        return f"<{self.__table__} - id:{self.id}>"

    @classmethod
    def get(cls, target_id: int) -> "BaseModel":
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

        if flush:
            session.flush()
        else:
            session.commit()

    def delete(self, soft: bool = True) -> None:
        """
        Delete the model.

        This method will delete the model from the database.
        """

        session = self.__session__()

        if soft:
            self.deleted_at = datetime.now(tz=UTC)
            session.add(self)

        else:
            session.delete(self)

        session.commit()

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
