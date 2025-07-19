"""
Constants.

This module contains the constants used in the application.
"""

from __future__ import annotations

from typing import ClassVar

from src.libs.locale.messages import MessagesMetaClass


class Messages(metaclass=MessagesMetaClass):
    """
    Messages.
    """

    JWT_ERROR_EXPIRED: ClassVar = {
        "en_us": "Token has expired.",
        "pt_br": "O token JWT expirou.",
    }
    JWT_ERROR_INVALID_ACCESS_TOKEN: ClassVar = {
        "en_us": "Incorrect access credentials.",
        "pt_br": "Credenciais de acesso incorretas.",
    }
    JWT_ERROR_INVALID_HEADER: ClassVar = {
        "en_us": "Invalid Authorization header.",
        "pt_br": "Cabeçalho de autorização inválido.",
    }

    TODO_NOT_FOUND: ClassVar = {
        "en_us": "Todo not found.",
        "pt_br": "Todo não encontrado.",
    }
    TODO_POST_ERROR: ClassVar = {
        "en_us": "Error creating todo.",
        "pt_br": "Erro ao criar todo.",
    }

    USER_NOT_FOUND: ClassVar = {
        "en_us": "User not found.",
        "pt_br": "Usuário não encontrado.",
    }
    USER_POST_ERROR: ClassVar = {
        "en_us": "Error creating user.",
        "pt_br": "Erro ao criar usuário.",
    }
    USER_POST_ERROR_EMAIL_EXISTS: ClassVar = {
        "en_us": "Email already exists.",
        "pt_br": "Email já existe.",
    }
    USER_POST_ERROR_PASSWORD_TO_WEAK: ClassVar = {
        "en_us": (
            "Password is too weak. It must be at least 6 characters long and "
            "contain at least one letter and one number."
        ),
        "pt_br": (
            "A senha é muito fraca. Deve ter pelo menos 6 caracteres e conter "
            "pelo menos uma letra e um número."
        ),
    }
