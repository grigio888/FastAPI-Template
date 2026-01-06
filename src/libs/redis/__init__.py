"""
Redis - Initializer.

This module contains the Redis client.
"""

from __future__ import annotations

import json
from typing import TYPE_CHECKING

from redis import Redis  # type: ignore[import-untyped]

from src.libs.pagination import paginate
from src.libs.pagination.schema import PaginatedSchema
from src.settings import Settings

if TYPE_CHECKING:
    from datetime import timedelta


class RedisClient:
    """
    Redis Client.
    """

    def __init__(
        self,
        host: str = Settings.REDIS_HOST,
        port: int = Settings.REDIS_PORT,
        db: int = Settings.REDIS_DB,
    ) -> None:
        """
        Initialize the Redis client.
        """

        self.client = Redis(
            host=host,
            port=port,
            db=db,
        )

    def get(self, key: str) -> dict | None:
        """
        Get the value of a key from Redis.
        """

        data = self.client.get(key)
        return json.loads(data) if data else None

    def set(
        self,
        key: str,
        value: dict,
        expire: int | timedelta | None = None,
    ) -> None:
        """
        Set the value of a key in Redis.

        It can also set an expiration time for the key.
        """

        self.client.set(key, json.dumps(value, default=str))

        if expire:
            self.client.expire(key, expire)

    def reset_expiration(
        self,
        key: str,
        expire: int | timedelta,
    ) -> None:
        """
        Reset the expiration time of a key in Redis.
        """

        if not self.client.exists(key):
            raise ValueError("Key does not exist")

        self.client.expire(key, expire)

    def has_key(self, key: str) -> bool:
        """
        Check if a key exists in Redis.
        """

        return self.client.exists(key)

    def search_keys(self, pattern: str) -> list[dict]:
        """
        Search for keys in Redis and return values that match the given pattern.
        """

        return self.client.scan_iter(match=pattern)

    def search(self, pattern: str) -> list[dict]:
        """
        Search for keys in Redis and return values that match the given pattern.
        """
        matched_values = []

        for key in self.client.scan_iter(match=pattern):
            data = self.get(key.decode("utf-8"))

            if data:
                matched_values.append(data)

        return matched_values

    async def search_with_pagination(
        self,
        pattern: str,
        page: int = 1,
        limit: int = 10,
    ) -> PaginatedSchema:
        """
        Search for keys in Redis with pagination and return values that match it.
        """

        matched_values = self.search(pattern)

        return await paginate(data=matched_values, page=page, page_size=limit)

    def delete(self, key: str) -> None:
        """
        Delete a key from Redis.
        """

        self.client.delete(key)

    def delete_pattern(
        self,
        pattern: str,
        exclude_if_contains: str | None = None,
    ) -> None:
        """
        Delete all keys that match a pattern.
        """

        keys = self.client.keys(pattern)

        for key in keys:
            if exclude_if_contains and exclude_if_contains in str(key):
                continue

            self.client.delete(key)
