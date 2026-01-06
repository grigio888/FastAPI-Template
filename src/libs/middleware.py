"""
Index for middlewares.
"""

from src.libs.authentication.middleware import JWTMiddleware
from src.libs.cors.middleware import CORSMiddleware
from src.libs.database.middleware import DBMiddleware
from src.libs.locale.middleware import LocalizationMiddleware
from src.libs.log.middleware import LoggingMiddleware
from src.libs.profiling.middleware import ProfilingMiddleware

__all__ = [
    "CORSMiddleware",
    "DBMiddleware",
    "JWTMiddleware",
    "LocalizationMiddleware",
    "LoggingMiddleware",
    "ProfilingMiddleware",
]
