"""
Locale - Middleware.

This middleware logs all application activities with structured logging.
"""

from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.types import ASGIApp

from src.libs.locale.context import current_language
from src.libs.locale.enums import LanguageEnum


class LocalizationMiddleware(BaseHTTPMiddleware):
    """
    Middleware to fetch the request language.

    It fetches the request language from the request headers and sets it in the context.
    """

    def __init__(
        self,
        app: ASGIApp,
    ) -> None:
        """
        Initialize the middleware.

        Args:
            app: ASGI application.

        """

        super().__init__(app)
        self.app = app

        self._default_language = LanguageEnum.en_us
        self._supported_languages = [
            LanguageEnum.en_us,
            LanguageEnum.pt_br,
        ]

    async def dispatch(
        self,
        request: Request,
        call_next: ASGIApp,
    ) -> Response:
        """
        Dispatch the request.

        Args:
            request: Request object.
            call_next: Next ASGI application.

        Returns:
            Response object.

        """
        # Identify language
        try:
            language = request.headers.get("accept-language", self._default_language)
            language = language.split(",")[0].lower().replace("-", "_")
            language = LanguageEnum(language)
        except (ValueError, AttributeError):
            language = self._default_language

        current_language.set(language)

        if language not in self._supported_languages:
            current_language.set(self._default_language)

        return await call_next(request)
