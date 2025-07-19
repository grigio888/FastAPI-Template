"""
Localization - Middleware - Context.

This module contains the context for the localization middleware.
Context is used to store the request language and other information.
"""

from contextvars import ContextVar

current_language: ContextVar[str] = ContextVar(
    "current_language",
    default="en_US",
)
