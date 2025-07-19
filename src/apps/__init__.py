"""
Version 1 of the API.

This module contains the version 1 of the API.

Modules:
- endpoints: Contains the endpoints for the API.
- models: Contains the models for the API.
- schemas: Contains the schemas for the API.
- services: Contains the services for the API.
- utils: Contains the utilities for the API.
"""

from fastapi import APIRouter

from src.apps.hc import endpoints as hc
from src.apps.todos import endpoints as todos
from src.apps.users import endpoints as users

# -- Export router
router = APIRouter()

router.include_router(hc.router)
router.include_router(todos.router)
router.include_router(users.router)
