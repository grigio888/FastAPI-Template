"""
Messages.

This module contains the messages used in the application.
"""

from __future__ import annotations

from typing import ClassVar

from src.libs.locale.enums import LanguageEnum as LE  # noqa: N817
from src.libs.locale.translate import translate as i18n
from src.libs.locale.utils import c_str


class Messages:
    """
    Messages.
    """

    class Roles:
        """
        Role messages.
        """

        class Error:
            """
            Error messages.
            """

            ALREADY_EXISTS: ClassVar[str] = c_str({
                LE.en_us: "Role already exists.",
                LE.pt_br: "Designação já existe.",
            })

            NOT_FOUND: ClassVar[str] = c_str({
                LE.en_us: "Role not found.",
                LE.pt_br: "Designação não encontrado.",
            })
            NOT_CREATED: ClassVar[str] = c_str({
                LE.en_us: "Role not created.",
                LE.pt_br: "Designação não criada.",
            })
            NOT_DELETED: ClassVar[str] = c_str({
                LE.en_us: "Role not deleted.",
                LE.pt_br: "Designação não deletada.",
            })

    class Permissions:
        """
        Permission messages.
        """

        class Error:
            """
            Error messages.
            """

            NOT_FOUND: ClassVar[str] = c_str({
                LE.en_us: "Permission not found.",
                LE.pt_br: "Permissão não encontrada.",
            })

            NOT_PERMITTED: ClassVar[str] = c_str({
                LE.en_us: "Permission denied.",
                LE.pt_br: "Permissão negada.",
            })

            ONLY_USERS: ClassVar[str] = c_str({
                LE.en_us: "Only users or above can perform this action.",
                LE.pt_br: "Apenas usuários ou superiores podem realizar esta ação.",
            })

            ONLY_USERS_OR_MODERATORS: ClassVar[str] = c_str({
                LE.en_us: "Only users or moderators can perform this action.",
                LE.pt_br: (
                    "Apenas usuários ou moderadores podem realizar esta ação."
                ),
            })

            ONLY_MODERATORS: ClassVar[str] = c_str({
                LE.en_us: "Only moderators or above can perform this action.",
                LE.pt_br: (
                    "Apenas moderadores ou superiores podem realizar esta ação."
                ),
            })

            ONLY_ADMIN: ClassVar[str] = c_str({
                LE.en_us: "Only admins can perform this action.",
                LE.pt_br: "Apenas administradores podem realizar esta ação.",
            })
