"""
Health Checker - Endpoints.

This module contains the endpoints for the Health Checker.
"""

from datetime import datetime, timezone

from decouple import config
from fastapi import APIRouter, status

from src.apps.hc.schemas import HealthCheckSchema

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

    current_time = datetime.now(tz=timezone.utc)
    current_timezone = str(current_time.tzinfo)
    time = current_time.isoformat()

    current_version = config("APP_VERSION", default="0.0.1")

    return HealthCheckSchema(
        timezone=current_timezone,
        time=time,
        version=current_version,
    )
