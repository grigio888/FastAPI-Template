"""
Shiori Backend - Database Session.

This module will create a database session for the Shiori Backend.
"""

from contextvars import ContextVar

from decouple import config
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Load environment variables
DB_USER = config("DB_USER")
DB_PASS = config("DB_PASS")
DB_HOST = config("DB_HOST")
DB_NAME = config("DB_NAME")

# Setting up the database URL
DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}/{DB_NAME}"

# Default engine
engine = create_engine(DATABASE_URL, echo=True)

# Session
Session = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Context variable to hold the session for each request
request_session: ContextVar = ContextVar("request_session", default=None)


def get_session() -> sessionmaker:
    """
    Get the current session for the request.

    If no session exists, create one.
    """

    session = request_session.get()

    if session is None:
        session = Session()
        request_session.set(session)

    return session


def close_session() -> None:
    """
    Close the session for the current request.
    """

    session = request_session.get()

    if session is not None:
        session.close()
        request_session.set(None)
