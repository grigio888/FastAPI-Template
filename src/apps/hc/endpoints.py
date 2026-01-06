"""
Health Checker - Endpoints.

This module contains the endpoints for the Health Checker.
"""

from datetime import UTC, datetime

from fastapi import APIRouter, status

from src.apps.hc.schemas import HealthCheckSchema
from src.settings import Settings

router = APIRouter(tags=["Health Checker"])


@router.get(
    "/",
    responses={
        status.HTTP_200_OK: {
            "description": "Health check successful",
            "model": HealthCheckSchema,
        },
    },
)
def health_checker() -> HealthCheckSchema:
    """
    ### Health Checker.

    This endpoint will return the current time and timezone of the server.
    """

    current_time = datetime.now(tz=UTC)
    current_timezone = str(current_time.tzinfo)
    time = current_time.isoformat()

    current_version = Settings.APP_VERSION

    return HealthCheckSchema(
        timezone=current_timezone,
        time=time,
        version=current_version,
    )
