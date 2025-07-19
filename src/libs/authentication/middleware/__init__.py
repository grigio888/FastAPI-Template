"""
JWT - Middleware.

Module to authenticate requests using JWT tokens.

TODO: NEEDS TO BE REFACTORED
"""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from fastapi.responses import JSONResponse
    from starlette.types import ASGIApp

import re
from collections.abc import Awaitable
from re import Pattern
from typing import Callable

from fastapi import HTTPException, Request
from starlette.middleware.base import BaseHTTPMiddleware

from src.libs.authentication.middleware.utils import (
    EXCLUDED_PATHS,
    is_service_up,
    validate_token,
    validate_token_against_service,
)
from src.libs.log import get_logger


class JWTMiddleware(BaseHTTPMiddleware):
    """
    # Authentication Middleware.

    Middleware to authenticate requests using JWT tokens. This middleware checks the
    Authorization header for a JWT token and validates it against the database.

    ## Requirements:

    ### ENV variables:
        - SECRET_KEY: Secret key to sign JWT tokens
        - ALGORITHM: Algorithm to use for JWT tokens (default: HS256)
        - EXCLUDED_PATHS: Comma-separated list of paths to exclude from authentication
            (default: "")
    """

    def __init__(
        self,
        app: ASGIApp,
        excluded_paths: list[str] = EXCLUDED_PATHS,
        is_testing: bool | None = None,
    ) -> None:
        """
        Initialize the middleware with the required parameters.
        """

        super().__init__(app)
        self.excluded_paths: list[Pattern] = []
        self.is_testing = is_testing or False
        self.logger = get_logger()

        for path in excluded_paths:
            try:
                self.excluded_paths.append(re.compile(path))

            except re.error:
                self.excluded_paths.append(re.compile(re.escape(path)))

    async def dispatch(
        self,
        request: Request,
        call_next: Callable[[Request], Awaitable[JSONResponse]],
    ) -> JSONResponse:
        """
        Dispatch method to authenticate requests using JWT tokens.
        """

        path = request.url.path

        if self._is_excluded_path(path):
            return await call_next(request)

        auth_header = request.headers.get("Authorization")

        if not auth_header:
            raise HTTPException(
                status_code=401,
                detail="Authorization header missing",
            )

        if self.is_testing:
            validate_token(auth_header)
            return await call_next(request)

        if not await is_service_up():
            raise HTTPException(
                status_code=503,
                detail=(
                    "Authentication service is down. "
                    "Did you forget to start it or misconfig AUTH_SERVICE_URL?",
                ),
            )

        await validate_token_against_service(auth_header)
        return await call_next(request)

    def _is_excluded_path(self, path: str) -> bool:
        """
        Check if the request path is in the list of excluded paths.
        """

        return any(re.search(skip, path) for skip in self.excluded_paths)
