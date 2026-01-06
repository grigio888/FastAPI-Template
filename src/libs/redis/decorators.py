"""
Redis - Decorators.
"""

from __future__ import annotations

import hashlib
import inspect
from collections.abc import Callable
from datetime import timedelta
from functools import wraps

from fastapi import Request
from pydantic import BaseModel

from src.libs.redis import RedisClient

redis_client = RedisClient(
    db=10,  # Use a different DB for page caching purposes
)


def cache_response(
    expire: int | timedelta = 60,
    custom_key: str = "cache",
) -> Callable:
    """
    # Cache FastAPI requst into redis.

    ## Usage:
    ```
    @router.get(
        path="/{user_identifier}",
        responses=...
    )
    @cache_response(expire=30)
    async def get_user(user_identifier: str) -> UserSiteSchema:
        ...
    ```

    If wanted to create a personalized key, you can pass a key builder.

    ```
    @router.get(
        path="/{user_identifier}",
        responses=...
    )
    @cache_response(expire=30, custom_key='custom_key')
    async def get_user(user_identifier: str) -> UserSiteSchema:
        ...
    ```
    """

    def decorator(func: Callable) -> Callable:
        @wraps(func)
        async def wrapper(*args: list, **kwargs: dict) -> Request:
            request: Request = kwargs.get("request") or (
                args[0] if args and isinstance(args[0], Request) else None
            )

            raw_key = (
                f"{request.url.path}?{request.url.query}"
                if request
                else str(args) + str(kwargs)
            )
            key = custom_key + ":" + hashlib.sha256(raw_key.encode()).hexdigest()

            cached = redis_client.get(key)
            if cached:
                return cached

            # Parse the request and cache its result
            if inspect.iscoroutinefunction(func):
                response = await func(*args, **kwargs)
            else:
                response = func(*args, **kwargs)

            if isinstance(response, BaseModel):
                redis_client.set(key, response.model_dump(), expire)
            else:
                redis_client.set(key, response, expire)

            return response

        return wrapper

    return decorator
