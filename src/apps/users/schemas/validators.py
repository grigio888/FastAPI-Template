"""
Users - Schemas - Validators.
"""

import re

from fastapi import HTTPException, status

from src.libs.authentication.middleware.hash import hash_sha512
from src.libs.log import get_context as _
from src.libs.log import get_logger
from src.messages import Messages

log = get_logger()


def validate_email(email: str) -> str:
    """
    Validate the email.

    This function checks if the email is in a valid format.
    """

    email_regex = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"

    if not re.match(email_regex, email):
        message = Messages.USER_POST_ERROR_EMAIL_INVALID
        log.error(f"{_()}: {message}")

        raise HTTPException(
            status_code=status.HTTP_406_NOT_ACCEPTABLE,
            detail=message,
        )

    return email


def validate_password(password: str) -> str:
    """
    Validate the password.

    This function checks if the password meets the required criteria.
    """

    password_regex = r"^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d]{6,}$"

    if not re.match(password_regex, password):
        message = Messages.USER_POST_ERROR_PASSWORD_TO_WEAK
        log.error(f"{_()}: {message}")

        raise HTTPException(
            status_code=status.HTTP_406_NOT_ACCEPTABLE,
            detail=message,
        )

    return hash_sha512(password)
