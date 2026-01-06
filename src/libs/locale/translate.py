"""
Locale - Middleware - Gettext.

This module contains the gettext function to retrieve the translated text.
"""

from __future__ import annotations

from src.libs.locale.context import current_language
from src.libs.locale.enums import LanguageEnum


def translate(
    text_map: dict[LanguageEnum, str] | str,
    **kwargs: dict[str, str],
) -> str:
    """
    Get the translated text.

    It retrieves the translated text from the given text map.

    If any arguments are passed, they will be formatted into the text.

    ---

    Usage:
    ```
    text = translate(
        {
            LanguageEnum.en_us: "Hello, {name}!",
            LanguageEnum.pt_br: "Olá, {name}!",
        },
        name="John",
    )

    print(text)  # Hello, John!
    ```
    """

    if isinstance(text_map, str):
        return text_map.format(**kwargs)

    language = current_language.get()
    text = text_map.get(
        language,
        text_map.get(LanguageEnum.en_us, ""),
    )

    return text.format(**kwargs)
