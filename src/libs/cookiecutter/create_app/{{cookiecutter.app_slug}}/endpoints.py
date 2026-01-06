"""
{{ cookiecutter.app_name.title() }} - Endpoints.

This module contains the endpoints for the {{ cookiecutter.app_name.title() }}.
"""

from fastapi import APIRouter, status

from src.apps.{{cookiecutter.app_slug}} import services
from src.apps.{{cookiecutter.app_slug}}.messages import Messages
from src.apps.{{cookiecutter.app_slug}}.schemas import {{ cookiecutter.app_name.title() }}PublicSchema
from src.libs.schemas import MessageSchema

router = APIRouter(tags=["{{ cookiecutter.app_name.title() }}"])

@router.get(
    "/{model_id}",
    responses={
        status.HTTP_200_OK: {
            "model": {{ cookiecutter.app_name.title() }}PublicSchema,
            "description": "Successful Response",
        },
        status.HTTP_404_NOT_FOUND: {
            "model": MessageSchema,
            "description": "{{ cookiecutter.app_name.title() }} not found.",
            "content": {
                "application/json": {
                    "example": {
                        "detail": Messages.{{ cookiecutter.app_name.title() }}.Error.NOT_FOUND,
                    },
                },
            },
        },
    },
)
def get_{{ cookiecutter.app_slug }}(model_id: int | str) -> {{ cookiecutter.app_name.title() }}PublicSchema:
    """
    ### Endpoint.

    This endpoint will return a {{ cookiecutter.app_name.title() }} model.
    """

    return services.get_{{ cookiecutter.app_slug }}_model(model_id)