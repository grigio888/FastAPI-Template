"""
Authentication - Messages.

This module contains the messages used in the authentication app.
"""

from __future__ import annotations

from typing import ClassVar

from src.libs.locale.enums import LanguageEnum as LE  # noqa: N817
from src.libs.locale.messages import MessagesMetaClass
from src.libs.locale.translate import translate as i18n
from src.libs.locale.utils import c_str


class Messages(metaclass=MessagesMetaClass):
    """
    Messages.
    """

    JWT_GENERATED: ClassVar[str] = c_str({
        LE.en_us: "Tokens generated successfully.",
        LE.pt_br: "Tokens gerados com sucesso.",
    })
    JWT_REFRESHED: ClassVar[str] = c_str({
        LE.en_us: "Tokens refreshed successfully.",
        LE.pt_br: "Tokens atualizados com sucesso.",
    })
    JWT_REVOKED: ClassVar[str] = c_str({
        LE.en_us: "Tokens revoked successfully.",
        LE.pt_br: "Tokens revogados com sucesso.",
    })

    JWT_INVALID: ClassVar[str] = c_str({
        LE.en_us: "Invalid token.",
        LE.pt_br: "Token inválido.",
    })
    JWT_INVALID_ACCESS_TOKEN: ClassVar[str] = c_str({
        LE.en_us: "Invalid access token.",
        LE.pt_br: "Token de acesso inválido.",
    })
    JWT_INVALID_REFRESH_TOKEN: ClassVar[str] = c_str({
        LE.en_us: "Invalid refresh token.",
        LE.pt_br: "Token de atualização inválido.",
    })
    JWT_INVALID_HEADER: ClassVar[str] = c_str({
        LE.en_us: "Invalid token header.",
        LE.pt_br: "Cabeçalho de token inválido.",
    })
    JWT_INVALID_TYPE: ClassVar[str] = c_str({
        LE.en_us: "Invalid token type.",
        LE.pt_br: "Tipo de token inválido.",
    })
    JWT_INVALID_STRUCTURE: ClassVar[str] = c_str({
        LE.en_us: "Invalid token structure.",
        LE.pt_br: "Estrutura do token inválida.",
    })
    JWT_MISSING_AUTHORIZATION_HEADER: ClassVar[str] = c_str({
        LE.en_us: "Missing Authorization header.",
        LE.pt_br: "Cabeçalho de autorização ausente.",
    })
    JWT_EXPIRED: ClassVar[str] = c_str({
        LE.en_us: "Token has expired.",
        LE.pt_br: "Token expirado.",
    })
    JWT_ALREADY_REVOKED: ClassVar[str] = c_str({
        LE.en_us: "Token has already been revoked.",
        LE.pt_br: "Token já foi revogado.",
    })
    JWT_NOT_REVOKED: ClassVar[str] = c_str({
        LE.en_us: "Token not revoked.",
        LE.pt_br: "Token não revogado.",
    })

    ROUTE_PROTECTED: ClassVar[str] = c_str({
        LE.en_us: "This route is protected and requires authentication",
        LE.pt_br: "Esta rota é protegida e requer autenticação",
    })

    INVALID_CREDENTIALS: ClassVar[str] = c_str({
        LE.en_us: "Invalid credentials.",
        LE.pt_br: "Credenciais inválidas.",
    })
    INVALID_EMAIL: ClassVar[str] = c_str({
        LE.en_us: "Email is invalid.",
        LE.pt_br: "Email inválido.",
    })

    NOT_BASIC_TOKEN: ClassVar[str] = c_str({
        LE.en_us: "Authorization header must be a Basic token.",
        LE.pt_br: "O cabeçalho de autorização deve ser um token Basic.",
    })

    GENERIC_ERROR: ClassVar[str] = c_str({
        LE.en_us: "An error occurred. Please try again later.",
        LE.pt_br: "Ocorreu um erro. Por favor, tente novamente mais tarde.",
    })
