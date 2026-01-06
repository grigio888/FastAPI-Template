"""
{{ cookiecutter.app_name.title() }} - Model.

This module contains the model for the {{ cookiecutter.app_name.title() }}.
"""

from __future__ import annotations

import sqlalchemy as sa
from sqlalchemy.orm import Mapped as M  # noqa: N817
from sqlalchemy.orm import mapped_column as MColumn  # noqa: N812

from src.apps.{{ cookiecutter.app_slug }}.messages import Messages
from src.libs.database.base_model import BaseModel


class {{ cookiecutter.app_name.title() }}Model(BaseModel):
    """
    {{ cookiecutter.app_name.title() }}.

    This class represents the {{ cookiecutter.app_name.title() }} model.
    """

    __tablename__ = "{{ cookiecutter.app_slug }}s"

    x: M[str] = MColumn(sa.String(255), primary_key=True, nullable=False)
    y: M[str] = MColumn(sa.String(255), nullable=False)
    z: M[str] = MColumn(sa.String(255), nullable=False, unique=True)

    def __repr__(self) -> str:
        """
        Representation of the {{ cookiecutter.app_name.title() }}Model.
        """

        return f"<{{ cookiecutter.app_name.title() }}Model - id:{self.id} - z:{self.z}>"
