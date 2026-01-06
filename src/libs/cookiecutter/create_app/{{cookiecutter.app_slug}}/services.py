"""
{{ cookiecutter.app_name.title() }} - Service.

This module contains the business logic for the {{ cookiecutter.app_name.title() }} service.
"""

from __future__ import annotations

from fastapi import HTTPException, status
from sqlalchemy import or_

from src.apps.{{cookiecutter.app_slug}}.messages import Messages
from src.apps.{{cookiecutter.app_slug}}.models import {{ cookiecutter.app_name.title() }}Model
from src.apps.{{cookiecutter.app_slug}}.schemas import (
    {{ cookiecutter.app_name.title() }}PublicSchema,
)
from src.libs.log import get_context as _
from src.libs.log import get_logger
from src.settings import Settings

log = get_logger()


def get_{{ cookiecutter.app_slug }}_model(
    model_identifier: int | str,
    raise_error: bool = True,
) -> {{ cookiecutter.app_name.title() }}Model:
    """
    Get {{ cookiecutter.app_name.title() }} model by ID or model identifier.
    """

    log.debug(f"{_()}: Getting {{ cookiecutter.app_name.title() }} model with identifier: {model_identifier}")

    filters = [{{ cookiecutter.app_name.title() }}Model.deleted_at.is_(None)]

    if isinstance(model_identifier, int) or model_identifier.isdigit():
        filters.append({{ cookiecutter.app_name.title() }}Model.id == model_identifier)
    else:
        filters.append(
            or_(
                {{ cookiecutter.app_name.title() }}Model.x == model_identifier,
                {{ cookiecutter.app_name.title() }}Model.y == model_identifier,
                {{ cookiecutter.app_name.title() }}Model.z == model_identifier,
            ),
        )

    model = {{ cookiecutter.app_name.title() }}Model.query().filter(*filters).first()

    if not model and raise_error:
        message = Messages.{{ cookiecutter.app_name.title() }}.Error.NOT_FOUND
        log.error(f"{_()}: {message}")

        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=message,
        )

    log.debug(f"{_()}: {{ cookiecutter.app_name.title() }} model found: {model}")

    return model


def get_{{ cookiecutter.app_slug }}(model_id: int | str) -> {{ cookiecutter.app_name.title() }}PublicSchema:
    """
    Get {{ cookiecutter.app_name.title() }} by ID.
    """

    log.debug(f"{_()}: Getting {{ cookiecutter.app_name.title() }} with ID {model_id}")

    model = get_{{ cookiecutter.app_slug }}_model(model_id)

    log.debug(f"{_()}: {{ cookiecutter.app_name.title() }} found: {model}")
    return {{ cookiecutter.app_name.title() }}PublicSchema.from_model(model)
