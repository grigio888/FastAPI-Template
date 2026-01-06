"""
{{ cookiecutter.app_name.title() }} - Messages.

This module contains the messages used in the {{ cookiecutter.app_name.title() }} app.
"""

from __future__ import annotations

from typing import ClassVar

from src.libs.locale.translate import translate as i18n
from src.libs.locale.enums import LanguageEnum as LE  # noqa: N817
from src.libs.locale.utils import c_str


class Messages:
    """
    Messages.
    """

    class {{ cookiecutter.app_name.title() }}:
        """
        {{ cookiecutter.app_name.title() }} messages.
        """

        class Error:
            """
            Error messages.
            """

            NOT_FOUND: ClassVar[str] = c_str({
                LE.en_us: "XYZ not found.",
                LE.pt_br: "XYZ não encontrado.",
            })
