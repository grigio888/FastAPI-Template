"""
Database - Alembic - Custom Types.

Theses custom types are used to avoid import issues in Alembic migrations.
Initially, they are used as extension to fastapi_storages types.
"""

from typing import Any

from fastapi_storages import FileSystemStorage
from fastapi_storages.integrations.sqlalchemy import FileType as _FileType


class FileType(_FileType):
    """
    File Type.

    This class represents a file type for SQLAlchemy models.
    """

    def __init__(self, *args: Any, **kwargs: Any) -> None:  # noqa: ANN401
        """
        Initialize the FileType with a default FileSystemStorage.
        """

        super().__init__(storage=FileSystemStorage(path="/vol/static"), *args, **kwargs)  # noqa: B026


class fastapi_storages:  # noqa: N801
    """
    Monkey patching fastapi_storages to avoid import issues in Alembic migrations.
    """

    class integrations:  # noqa: N801
        """
        Monkey patching.
        """

        class sqlalchemy:  # noqa: N801
            """
            Monkey patching.
            """

            FileType = FileType
