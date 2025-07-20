"""
Health Checker - Schema.

This module contains the schema for the health check responses.
"""

from datetime import datetime
from datetime import timezone as dt_timezone

from pydantic import BaseModel, Field


class HealthCheckSchema(BaseModel):
    """
    Health Check Schema.
    """

    timezone: str = Field(
        ...,
        description="The timezone of the server",
        examples=["UTC", "America/New_York"],
    )
    time: str = Field(
        ...,
        description="The current time in ISO 8601 format",
        examples=[datetime.now(tz=dt_timezone.utc).isoformat()],
    )
    version: str = Field(
        ...,
        description="The version of the application",
        examples=["0.0.1"],
    )
