"""
FastAPI main module.

This module contains:
- FastAPI app instance.
- Middlewares.
- Version routers.
"""

from fastapi import FastAPI

from src.apps import router as main_router
from src.libs.middleware import (
    CORSMiddleware,
    JWTMiddleware,
    LocalizationMiddleware,
    LoggingMiddleware,
)

app = FastAPI()

app.add_middleware(JWTMiddleware, is_testing=True)
app.add_middleware(CORSMiddleware)
app.add_middleware(LoggingMiddleware)
app.add_middleware(LocalizationMiddleware)

app.include_router(main_router)
