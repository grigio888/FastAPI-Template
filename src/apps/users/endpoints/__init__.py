"""
Users - Endpoints - Index.
"""

from fastapi import APIRouter

from src.apps.users.endpoints import (
    users,
)

# -- Export router
router = APIRouter(prefix="/users", tags=["Users"])

router.include_router(users.router)
