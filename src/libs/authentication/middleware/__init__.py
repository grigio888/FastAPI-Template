"""
Authentication - Middleware.

Module to authenticate requests using JWT tokens.

TODO: NEEDS TO BE REFACTORED
"""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from starlette.types import ASGIApp

import re
from collections.abc import Awaitable, Callable
from re import Pattern

from fastapi import HTTPException, Request, status
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware

from src.libs.authentication.messages import Messages
from src.libs.authentication.middleware.utils import (
    decode_jwt,
    deconstruct_auth_header,
    validate_token_info,
)
from src.libs.log import get_context as _
from src.libs.log import get_logger
from src.settings import Settings

log = get_logger()


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
        excluded_paths: list[str] = Settings.EXCLUDED_PATHS,
        is_testing: bool = False,
    ) -> None:
        """
        Initialize the middleware with the required parameters.
        """

        super().__init__(app)
        default_paths = [
            r"^\/$",
            r"^\/docs",
            r"^\/openapi.json",
            r"^\/redoc",
        ]
        self.excluded_paths: list[Pattern] = []
        self.is_testing = is_testing

        for path in [*excluded_paths, *default_paths]:
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
            return JSONResponse(
                status_code=status.HTTP_401_UNAUTHORIZED,
                content={
                    "detail": (
                        f"{Messages.ROUTE_PROTECTED}: "
                        f"{Messages.JWT_MISSING_AUTHORIZATION_HEADER}"
                    ),
                },
            )

        _schema, token = deconstruct_auth_header(auth_header)

        if self.is_testing:
            try:
                decode_jwt(token)

            except ValueError as error:
                message = str(error)
                log.exception(f"{_()}: Error validating token: {message}")

                return JSONResponse(
                    status_code=401,
                    content={
                        "detail": message,
                    },
                )

        try:
            validate_token_info(token)

        except HTTPException as error:
            message = error.detail
            log.exception(f"{_()}: Error validating token: {message}")

            return JSONResponse(
                status_code=error.status_code,
                content={
                    "detail": message,
                },
            )

        return await call_next(request)

    def _is_excluded_path(self, path: str) -> bool:
        """
        Check if the request path is in the list of excluded paths.
        """

        return any(re.search(skip, path) for skip in self.excluded_paths)
