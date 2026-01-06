"""
Locale - Context.

This module contains the context for the localization middleware.
Context is used to store the request language and other information.
"""

from contextvars import ContextVar

from src.libs.locale.enums import LanguageEnum

current_language: ContextVar[LanguageEnum] = ContextVar(
    "current_language",
    default=LanguageEnum.en_us,
)
