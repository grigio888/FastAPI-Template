"""
FastAPI main module.

This module contains:
- FastAPI app instance.
- Middlewares.
- Version routers.
"""

from fastapi import FastAPI

from src.apps import router as main_router
from src.libs.admin import Admin
from src.libs.admin.config import AdminConfig
from src.libs.middleware import (
    CORSMiddleware,
    DBMiddleware,
    LocalizationMiddleware,
    LoggingMiddleware,
    ProfilingMiddleware,
)

app = FastAPI()

app.add_middleware(ProfilingMiddleware)
app.add_middleware(DBMiddleware)
# app.add_middleware(JWTMiddleware, is_testing=True)  # noqa: ERA001
app.add_middleware(CORSMiddleware)
app.add_middleware(LoggingMiddleware)
app.add_middleware(LocalizationMiddleware)

app.include_router(main_router)

admin = Admin(app, **AdminConfig.as_dict())
