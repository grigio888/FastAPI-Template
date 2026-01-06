"""
Profiling - Middleware.

Measure and report request processing time.
"""

from __future__ import annotations

import time
from typing import TYPE_CHECKING

if TYPE_CHECKING:  # pragma: no cover - type hints only
    from fastapi import Request, Response
    from starlette.types import ASGIApp

from collections.abc import Awaitable, Callable

from starlette.middleware.base import BaseHTTPMiddleware

from src.libs.log import get_logger

log = get_logger()


class ProfilingMiddleware(BaseHTTPMiddleware):
    """
    # Profile Middleware.

    Profile each request and emit duration details.
    """

    def __init__(
        self,
        app: ASGIApp,
        header_name: str = "X-Process-Time",
    ) -> None:
        """
        # Initialize the profiling middleware.

        Args:
            app (ASGIApp): The ASGI application.
            header_name (str): The name of the header to store the processing time.

        """

        super().__init__(app)
        self.header_name = header_name

    async def dispatch(
        self,
        request: Request,
        call_next: Callable[[Request], Awaitable[Response]],
    ) -> Response:
        """
        # Dispatch the request and measure processing time.

        Args:
            request (Request): The incoming request.
            call_next (Callable[[Request], Awaitable[Response]]):
                The next middleware or route handler.

        Returns:
            Response: The response from the next middleware or route handler.

        """

        start_time = time.perf_counter()

        try:
            response = await call_next(request)

        except Exception:
            duration = time.perf_counter() - start_time

            log.exception(
                f"Request {request.method} {request.url.path} "
                f"failed after {duration:.6f}s",
            )

            raise

        duration = time.perf_counter() - start_time
        response.headers[self.header_name] = f"{duration:.6f}s"

        log.info(
            f"Request {request.method} {request.url.path} completed in {duration:.6f}s",
        )

        return response
