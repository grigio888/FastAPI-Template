"""
Localization - Middleware - Gettext.

This module contains the gettext function to retrieve the translated text.
"""

from __future__ import annotations

from src.libs.locale.context import current_language


def translate(text_map: dict | str, **kwargs: dict) -> str:
    """
    Get the translated text.

    It retrieves the translated text from the given text map.

    If any arguments are passed, they will be formatted into the text.
    """

    if isinstance(text_map, str):
        return text_map.format(**kwargs)

    language = current_language.get()
    text = text_map.get(language.lower(), text_map.get("en_us", ""))

    return text.format(**kwargs)
