"""
Database - Middleware.

Module to manage database sessions for each request.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from fastapi import Request, Response
    from starlette.types import ASGIApp

from collections.abc import Awaitable, Callable

from sqlalchemy.exc import SQLAlchemyError
from starlette.middleware.base import BaseHTTPMiddleware

from src.libs.database.session import close_session, create_session
from src.libs.log import get_context as _
from src.libs.log import get_logger

log = get_logger()


class DBMiddleware(BaseHTTPMiddleware):
    """Ensure each request uses a clean database session."""

    def __init__(self, app: ASGIApp) -> None:
        """Initialize the middleware."""

        super().__init__(app)

    async def dispatch(
        self,
        request: Request,
        call_next: Callable[[Request], Awaitable[Response]],
    ) -> Response:
        """
        Dispatch the request, ensuring a clean DB session.
        """

        session = create_session()
        request.state.db = session

        try:
            response = await call_next(request)

            if session.is_active:
                try:
                    session.commit()

                except SQLAlchemyError:
                    session.rollback()
                    log.exception(f"{_()}: Commit failed; session rolled back.")
                    raise

            return response  # noqa: TRY300

        except Exception:
            if session.is_active:
                session.rollback()

            log.exception(
                f"{_()}: Unhandled error; session rolled back before propagating.",
            )

            raise

        finally:
            if hasattr(request.state, "db"):
                delattr(request.state, "db")

            close_session()
