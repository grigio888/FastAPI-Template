"""
Middleware - CORS.

Custom CORSMiddleware that fetches configuration from environment variables.
"""

from decouple import config
from fastapi.middleware.cors import CORSMiddleware as FastAPICORSMiddleware
from starlette.types import ASGIApp


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
        configs: dict[str, str] = {
            "allow_origins": config(
                "ALLOWED_ORIGINS",
                default="*",
                cast=lambda x: [origin.strip() for origin in x.split(",")],
            ),
            "allow_methods": config(
                "ALLOWED_METHODS",
                default="*",
                cast=lambda x: [method.strip() for method in x.split(",")],
            ),
            "allow_headers": config(
                "ALLOWED_HEADERS",
                default="*",
                cast=lambda x: [header.strip() for header in x.split(",")],
            ),
            "allow_credentials": config("ALLOW_CREDENTIALS", default=True, cast=bool),
        }

        # Initialize the parent CORSMiddleware
        super().__init__(app=app, **configs)
