"""
Logger - Middleware.

This middleware logs all application activities with structured logging.
"""

import asyncio

from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.types import ASGIApp

from src.libs.log import get_logger, setup_logging
from template.src.libs.utilities.misc import (
    refresh_log_threshold,
    should_log,
)
from src.settings import Settings


class LoggingMiddleware(BaseHTTPMiddleware):
    """
    Middleware to log all application activities with structured logging.

    Requires ENV variables:
        - LOG_LEVEL: Logging level (default: INFO)
        - LOG_FORMAT: Logging format (
                default: "[%(asctime)s - %(name)s %(levelname)s] %(message)s"
            )
        - LOG_NAME: Logger name (default: "default_logger")
    """

    def __init__(
        self,
        app: ASGIApp,
        level: str = Settings.LOG_LEVEL,
        log_format: str = Settings.LOG_FORMAT,
        name: str = Settings.LOG_NAME,
    ) -> None:
        """
        Initialize the LoggingMiddleware.

        :param app: ASGI application.
        :param level: Logging level.
        :param format: Logging format.
        :param name: Logger name.
        """

        super().__init__(app)

        setup_logging(level, log_format, name)
        self.logger = get_logger(name)

    async def dispatch(self, request: Request, call_next: ASGIApp) -> Response:
        """
        Log request and response details.

        :param request: Incoming request.
        :param call_next: Function to call the next middleware or route handler.
        """

        if (
            request.headers.get("connection")
            and request.headers.get("connection").lower() == "keep-alive"
        ):
            if not should_log():
                return await call_next(request)

            refresh_log_threshold()

        asyncio.create_task(self.log_request(request))

        try:
            response = await call_next(request)
        except Exception as e:
            asyncio.create_task(self.log_exception(e))
            raise

        asyncio.create_task(self.log_response(request, response))

        return response

    async def log_request(self, request: Request) -> None:
        """
        Log request details, including the body if available.

        :param request: Incoming request.
        """

        self.logger.info(f"Request: {request.method} {request.url}")
        self.logger.debug(f"Headers: {dict(request.headers)}")

    async def log_exception(self, exception: Exception) -> None:
        """
        Log exception details.

        :param exception: Exception that occurred.
        """

        self.logger.error(f"Exception occurred: {exception}", exc_info=True)

    async def log_response(self, request: Request, response: Response) -> None:
        """
        Log response details.

        :param request: Incoming request.
        :param response: Outgoing response.
        """

        self.dynamic_log(
            response.status_code,
            f"Response: {response.status_code} for {request.method} {request.url}",
        )

    def dynamic_log(self, status_code: int, message: str) -> None:
        """
        Log messages dynamically based on the status code.

        :param status_code: HTTP status code of the response.
        :param message: Log message.
        """

        if status_code >= 500:
            self.logger.error(message)
        elif status_code >= 400:
            self.logger.warning(message)
        else:
            self.logger.info(message)
