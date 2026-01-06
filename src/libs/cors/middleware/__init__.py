"""
CORS - Middleware.

Custom CORSMiddleware that fetches configuration from environment variables.
"""

from fastapi.middleware.cors import CORSMiddleware as FastAPICORSMiddleware
from starlette.types import ASGIApp

from src.settings import Settings


class CORSMiddleware(FastAPICORSMiddleware):
    """
    Custom CORSMiddleware that fetches configuration from environment variables.

    ENV variables:
        - ALLOWED_ORIGINS: Comma-separated list of allowed origins (default: "*")
        - ALLOWED_METHODS: Comma-separated list of allowed HTTP methods (default: "*")
        - ALLOWED_HEADERS: Comma-separated list of allowed HTTP headers (default: "*")
        - ALLOW_CREDENTIALS: Boolean to allow credentials (default: True)
    """

    def __init__(self, app: ASGIApp) -> None:
        """
        Initialize the CORSMiddleware.
        """
        # Fetch environment variables
        configs: dict[str, list[str] | bool] = {
            "allow_origins": Settings.CORS_ALLOWED_ORIGINS,
            "allow_methods": Settings.CORS_ALLOWED_METHODS,
            "allow_headers": Settings.CORS_ALLOWED_HEADERS,
            "allow_credentials": Settings.CORS_ALLOWED_CREDENTIALS,
        }

        # Initialize the parent CORSMiddleware
        super().__init__(app=app, **configs)
