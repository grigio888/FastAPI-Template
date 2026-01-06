"""
Database - Session.

This module creates and manages database sessions for the Backend.
"""

from collections.abc import Callable
from contextvars import ContextVar
from typing import Any

from sqlalchemy import create_engine
from sqlalchemy.orm import Session as SASession
from sqlalchemy.orm import sessionmaker

from src.settings import Settings

# Setting up the database URL
if Settings.DB_DIALECT == "sqlite":
    DATABASE_URL = f"sqlite:///{Settings.DB_NAME}.db"
else:
    DATABASE_URL = (
        f"{Settings.DB_DIALECT}://{Settings.DB_USER}:{Settings.DB_PASS}@{Settings.DB_HOST}"
        f"/{Settings.DB_NAME}"
    )

# Default engine
engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,
    pool_size=5,
    max_overflow=10,
    pool_timeout=10,
)

SessionFactory = sessionmaker(bind=engine, expire_on_commit=False, autoflush=False)

# Keep backwards compatibility for existing patches/tests
Session = SessionFactory
SessionLocal = SessionFactory

# Context variable to hold the session for each request
request_session: ContextVar[SASession | None] = ContextVar(
    "request_session",
    default=None,
)


def create_session() -> SASession:
    """Create and store a new session for the current request."""

    session = SessionFactory()
    request_session.set(session)
    return session


def get_session() -> SASession:
    """Return the request-scoped session, creating it if necessary."""

    session = request_session.get()

    if session is None:
        session = create_session()

    return session


def close_session() -> None:
    """Dispose of the request-scoped session."""

    session = request_session.get()

    if session is None:
        return

    try:
        if session.is_active:
            session.rollback()
    finally:
        session.close()
        request_session.set(None)


def single_pool(func: Callable) -> Callable:
    """Execute the wrapped function within a single shared transaction."""

    def wrapper(*args: Any, **kwargs: Any) -> Any:  # noqa: ANN401
        db_session = get_session()

        with db_session.begin():
            return func(*args, **kwargs)

    return wrapper
