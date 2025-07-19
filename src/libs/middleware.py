"""
Index for middlewares.
"""

from src.libs.authentication.middleware import JWTMiddleware
from src.libs.cors.middleware import CORSMiddleware
from src.libs.locale.middleware import LocalizationMiddleware
from src.libs.log.middleware import LoggingMiddleware

__all__ = [
    "CORSMiddleware",
    "JWTMiddleware",
    "LocalizationMiddleware",
    "LoggingMiddleware",
]
