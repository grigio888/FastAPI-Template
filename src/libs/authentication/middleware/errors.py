"""
Authentication - Middleware - Custom Exceptions.
"""

from jwt import ExpiredSignatureError as PyJWTExpiredSignatureError
from jwt import InvalidSignatureError as PyJWTInvalidSignatureError
from jwt import PyJWTError as PyJWTError_


class ExpiredSignatureError(PyJWTExpiredSignatureError):
    """
    Exception raised when a JWT token has expired.
    """

    def __init__(self, message: str = "Token has expired") -> None:
        """Initialize the ExpiredSignatureError."""
        self.message = message
        super().__init__(self.message)


class InvalidSignatureError(PyJWTInvalidSignatureError):
    """
    Exception raised when a JWT token has an invalid signature.
    """

    def __init__(self, message: str = "Incorrect access credentials.") -> None:
        """Initialize the InvalidSignatureError."""
        self.message = message
        super().__init__(self.message)


class PyJWTError(PyJWTError_):
    """
    Exception raised when a PyJWT error occurs.
    """

    def __init__(self, message: str = "PyJWT error") -> None:
        """Initialize the PyJWTError."""
        self.message = message
        super().__init__(self.message)


class TokenRevokedError(Exception):
    """
    Exception raised when a token has been revoked.
    """

    def __init__(self, message: str = "Token has been revoked") -> None:
        """Initialize the TokenRevokedError."""
        self.message = message
        super().__init__(self.message)
