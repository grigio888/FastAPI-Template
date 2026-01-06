"""
Constants.

This module contains the constants used in the application.
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

    class Users:
        """
        User messages.
        """

        class Success:
            """
            Success messages.
            """

            CREATED: ClassVar[str] = c_str(
                {
                    LE.en_us: "User created successfully.",
                    LE.pt_br: "Usuário criado com sucesso.",
                }
            )
            UPDATED: ClassVar[str] = c_str(
                {
                    LE.en_us: "User updated successfully.",
                    LE.pt_br: "Usuário atualizado com sucesso.",
                }
            )
            DELETED: ClassVar[str] = c_str(
                {
                    LE.en_us: "User deleted successfully.",
                    LE.pt_br: "Usuário deletado com sucesso.",
                }
            )

            EMAIL_VERIFIED: ClassVar[str] = c_str(
                {
                    LE.en_us: "Email verified successfully.",
                    LE.pt_br: "Email verificado com sucesso.",
                }
            )

        class Error:
            """
            Error messages.
            """

            NOT_AUTHORIZED: ClassVar[str] = c_str(
                {
                    LE.en_us: "You don't have permission to access this.",
                    LE.pt_br: "Você não tem permissão para acessar isso.",
                }
            )
            NOT_CREATED: ClassVar[str] = c_str(
                {
                    LE.en_us: "Error creating user.",
                    LE.pt_br: "Erro ao criar usuário.",
                }
            )
            NOT_FOUND: ClassVar[str] = c_str(
                {
                    LE.en_us: "User not found.",
                    LE.pt_br: "Usuário não encontrado.",
                }
            )
            NO_DATA_PROVIDED: ClassVar[str] = c_str(
                {
                    LE.en_us: "No data provided.",
                    LE.pt_br: "Nenhum dado fornecido.",
                }
            )

            INACTIVE_USER: ClassVar[str] = c_str(
                {
                    LE.en_us: (
                        "User account is inactive. Activate it through your email."
                    ),
                    LE.pt_br: (
                        "A conta do usuário está inativa. Ative-a através do seu email."
                    ),
                }
            )
            INVALID_IMAGE_TYPE: ClassVar[str] = c_str(
                {
                    LE.en_us: "Invalid image type.",
                    LE.pt_br: "Tipo de imagem inválido.",
                }
            )
            INVALID_VERIFICATION_TOKEN: ClassVar[str] = c_str(
                {
                    LE.en_us: "Invalid verification token.",
                    LE.pt_br: "Token de verificação inválido.",
                }
            )

            ERROR_CREATING: ClassVar[str] = c_str(
                {
                    LE.en_us: "Error creating user.",
                    LE.pt_br: "Erro ao criar usuário.",
                }
            )
            EMAIL_INVALID: ClassVar[str] = c_str(
                {
                    LE.en_us: "Email is invalid.",
                    LE.pt_br: "Email inválido.",
                }
            )
            EMAIL_ALREADY_EXISTS: ClassVar[str] = c_str(
                {
                    LE.en_us: "Email already exists.",
                    LE.pt_br: "Email já existe.",
                }
            )

            PASSWORD_TOO_WEAK: ClassVar[str] = c_str(
                {
                    LE.en_us: (
                        "Password is too weak. It must be at least 6 characters long "
                        "and contain at least one letter and one number."
                    ),
                    LE.pt_br: (
                        "A senha é muito fraca. Deve ter pelo menos 6 caracteres e "
                        "conter pelo menos uma letra e um número."
                    ),
                }
            )

            USERNAME_ALREADY_EXISTS: ClassVar[str] = c_str(
                {
                    LE.en_us: "Username already exists.",
                    LE.pt_br: "Nome de usuário já existe.",
                }
            )
