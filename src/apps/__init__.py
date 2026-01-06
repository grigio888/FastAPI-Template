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

from src.libs.utilities.path import load_all_objects_from

# -- Export router
router = APIRouter()

apps_routers = load_all_objects_from(
    module_name="endpoints",
    type_of="router",
    as_list=True,
    order=[lambda x: x.tags[0] if x.tags else "", False],
)

if apps_routers:
    for item in apps_routers:
        router.include_router(item)
