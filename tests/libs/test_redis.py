"""
Test Redis Module.

This module tests the Redis client and decorators in src/libs/redis/.
"""

import asyncio
import unittest
from datetime import timedelta
from unittest.mock import MagicMock, patch

from fastapi import Request
from pydantic import BaseModel

from src.libs.redis import RedisClient
from src.libs.redis.decorators import cache_response


class TestRedisClient(unittest.TestCase):
    """Test Redis client functionality."""

    def setUp(self):
        """Set up test fixtures."""
        # Mock Redis client to avoid actual Redis connection
        with patch("src.libs.redis.Redis") as mock_redis:
            self.mock_redis_instance = MagicMock()
            mock_redis.return_value = self.mock_redis_instance
            self.redis_client = RedisClient()

    def test_redis_client_initialization(self):
        """Test Redis client initialization."""
        # Redis client should be initialized
        self.assertIsNotNone(self.redis_client.client)

    def test_get_existing_key(self):
        """Test getting an existing key from Redis."""
        # Mock Redis get method
        self.mock_redis_instance.get.return_value = b'{"key": "value"}'

        result = self.redis_client.get("test_key")

        self.assertEqual(result, {"key": "value"})
        self.mock_redis_instance.get.assert_called_once_with("test_key")

    def test_get_nonexistent_key(self):
        """Test getting a non-existent key from Redis."""
        # Mock Redis get method to return None
        self.mock_redis_instance.get.return_value = None

        result = self.redis_client.get("nonexistent_key")

        self.assertIsNone(result)
        self.mock_redis_instance.get.assert_called_once_with("nonexistent_key")

    def test_set_without_expiration(self):
        """Test setting a key without expiration."""
        test_value = {"name": "test", "value": 123}

        self.redis_client.set("test_key", test_value)

        self.mock_redis_instance.set.assert_called_once_with(
            "test_key",
            '{"name": "test", "value": 123}',
        )
        self.mock_redis_instance.expire.assert_not_called()

    def test_set_with_expiration(self):
        """Test setting a key with expiration."""
        test_value = {"name": "test", "value": 123}
        expire_time = 300

        self.redis_client.set("test_key", test_value, expire_time)

        self.mock_redis_instance.set.assert_called_once_with(
            "test_key",
            '{"name": "test", "value": 123}',
        )
        self.mock_redis_instance.expire.assert_called_once_with("test_key", expire_time)

    def test_set_with_timedelta_expiration(self):
        """Test setting a key with timedelta expiration."""
        test_value = {"name": "test", "value": 123}
        expire_time = timedelta(minutes=5)

        self.redis_client.set("test_key", test_value, expire_time)

        self.mock_redis_instance.expire.assert_called_once_with("test_key", expire_time)

    def test_reset_expiration_existing_key(self):
        """Test resetting expiration for existing key."""
        # Mock key exists
        self.mock_redis_instance.exists.return_value = True
        expire_time = 600

        self.redis_client.reset_expiration("test_key", expire_time)

        self.mock_redis_instance.exists.assert_called_once_with("test_key")
        self.mock_redis_instance.expire.assert_called_once_with("test_key", expire_time)

    def test_reset_expiration_nonexistent_key(self):
        """Test resetting expiration for non-existent key."""
        # Mock key doesn't exist
        self.mock_redis_instance.exists.return_value = False

        with self.assertRaises(ValueError) as context:
            self.redis_client.reset_expiration("nonexistent_key", 600)

        self.assertIn("Key does not exist", str(context.exception))
        self.mock_redis_instance.exists.assert_called_once_with("nonexistent_key")

    def test_has_key_existing(self):
        """Test checking if key exists (exists)."""
        self.mock_redis_instance.exists.return_value = True

        result = self.redis_client.has_key("test_key")

        self.assertTrue(result)
        self.mock_redis_instance.exists.assert_called_once_with("test_key")

    def test_has_key_nonexistent(self):
        """Test checking if key exists (doesn't exist)."""
        self.mock_redis_instance.exists.return_value = False

        result = self.redis_client.has_key("test_key")

        self.assertFalse(result)

    def test_search_keys(self):
        """Test searching for keys by pattern."""
        mock_keys = [b"test:1", b"test:2", b"test:3"]
        self.mock_redis_instance.scan_iter.return_value = mock_keys

        result = self.redis_client.search_keys("test:*")

        self.assertEqual(result, mock_keys)
        self.mock_redis_instance.scan_iter.assert_called_once_with(match="test:*")

    def test_search_values(self):
        """Test searching for values by pattern."""
        mock_keys = [b"test:1", b"test:2"]
        self.mock_redis_instance.scan_iter.return_value = mock_keys

        # Mock get method to return different values for different keys
        def mock_get(key):
            if key == "test:1":
                return b'{"id": 1, "name": "item1"}'
            if key == "test:2":
                return b'{"id": 2, "name": "item2"}'
            return None

        self.mock_redis_instance.get.side_effect = mock_get

        result = self.redis_client.search("test:*")

        expected = [
            {"id": 1, "name": "item1"},
            {"id": 2, "name": "item2"},
        ]
        self.assertEqual(result, expected)

    def test_search_with_pagination(self):
        """Test searching with pagination."""
        # Mock search method
        with patch.object(self.redis_client, "search") as mock_search:
            mock_search.return_value = [
                {"id": 1, "name": "item1"},
                {"id": 2, "name": "item2"},
                {"id": 3, "name": "item3"},
            ]

            # Run async test
            loop = asyncio.get_event_loop()
            result = loop.run_until_complete(
                self.redis_client.search_with_pagination("test:*", page=1, limit=2),
            )

            self.assertEqual(result.count, 3)
            self.assertEqual(len(result.items), 2)
            self.assertEqual(result.current_page, 1)
            self.assertEqual(result.next_page, 2)

    def test_delete_key(self):
        """Test deleting a key."""
        self.redis_client.delete("test_key")

        self.mock_redis_instance.delete.assert_called_once_with("test_key")

    def test_delete_pattern_without_exclusion(self):
        """Test deleting keys by pattern without exclusion."""
        mock_keys = [b"test:1", b"test:2", b"test:3"]
        self.mock_redis_instance.keys.return_value = mock_keys

        self.redis_client.delete_pattern("test:*")

        self.mock_redis_instance.keys.assert_called_once_with("test:*")
        # Should call delete for each key
        expected_calls = [unittest.mock.call(key) for key in mock_keys]
        self.mock_redis_instance.delete.assert_has_calls(expected_calls)

    def test_delete_pattern_with_exclusion(self):
        """Test deleting keys by pattern with exclusion."""
        mock_keys = [b"test:1", b"test:exclude:2", b"test:3"]
        self.mock_redis_instance.keys.return_value = mock_keys

        self.redis_client.delete_pattern("test:*", exclude_if_contains="exclude")

        # Should delete test:1 and test:3, but not test:exclude:2
        expected_calls = [
            unittest.mock.call(b"test:1"),
            unittest.mock.call(b"test:3"),
        ]
        self.mock_redis_instance.delete.assert_has_calls(expected_calls)
        self.assertEqual(self.mock_redis_instance.delete.call_count, 2)


class TestCacheDecorator(unittest.TestCase):
    """Test cache response decorator."""

    def setUp(self):
        """Set up test fixtures."""
        # Mock RedisClient
        self.mock_redis_client = MagicMock()

    @patch("src.libs.redis.decorators.redis_client")
    def test_cache_response_miss_then_hit(self, mock_redis):
        """Test cache response decorator with cache miss then hit."""
        mock_redis.get.side_effect = [
            None,
            {"result": "cached"},
        ]  # First miss, then hit

        @cache_response(expire=60, custom_key="test")
        async def test_function():
            return {"result": "fresh"}

        # First call - cache miss
        loop = asyncio.get_event_loop()
        result1 = loop.run_until_complete(test_function())

        self.assertEqual(result1, {"result": "fresh"})
        mock_redis.set.assert_called_once()

        # Second call - cache hit
        mock_redis.reset_mock()
        result2 = loop.run_until_complete(test_function())

        self.assertEqual(result2, {"result": "cached"})
        mock_redis.set.assert_not_called()  # Should not set on cache hit

    @patch("src.libs.redis.decorators.redis_client")
    def test_cache_response_with_request_object(self, mock_redis):
        """Test cache response decorator with FastAPI Request object."""
        mock_redis.get.return_value = None

        # Mock request object
        mock_request = MagicMock(spec=Request)
        mock_request.url.path = "/api/users"
        mock_request.url.query = "page=1&limit=10"

        @cache_response(expire=30)
        async def test_function(request: Request):
            return {"users": []}

        loop = asyncio.get_event_loop()
        result = loop.run_until_complete(test_function(request=mock_request))

        self.assertEqual(result, {"users": []})
        mock_redis.get.assert_called_once()
        mock_redis.set.assert_called_once()

    @patch("src.libs.redis.decorators.redis_client")
    def test_cache_response_with_pydantic_model(self, mock_redis):
        """Test cache response decorator with Pydantic model response."""
        mock_redis.get.return_value = None

        class TestModel(BaseModel):
            name: str
            value: int

        @cache_response(expire=60)
        async def test_function():
            return TestModel(name="test", value=123)

        loop = asyncio.get_event_loop()
        result = loop.run_until_complete(test_function())

        self.assertIsInstance(result, TestModel)
        self.assertEqual(result.name, "test")
        self.assertEqual(result.value, 123)

        # Verify model_dump was called for caching
        mock_redis.set.assert_called_once()
        set_call_args = mock_redis.set.call_args[0]
        cached_data = set_call_args[1]  # Second argument is the data
        self.assertEqual(cached_data, {"name": "test", "value": 123})

    @patch("src.libs.redis.decorators.redis_client")
    def test_cache_response_sync_function(self, mock_redis):
        """Test cache response decorator with synchronous function."""
        mock_redis.get.return_value = None

        @cache_response(expire=60)
        def sync_function():
            return {"sync": True}

        # Note: We still need to run this in async context since decorator is async
        loop = asyncio.get_event_loop()
        result = loop.run_until_complete(sync_function())

        self.assertEqual(result, {"sync": True})
        mock_redis.set.assert_called_once()

    @patch("src.libs.redis.decorators.redis_client")
    def test_cache_response_custom_key(self, mock_redis):
        """Test cache response decorator with custom key."""
        mock_redis.get.return_value = None

        @cache_response(expire=60, custom_key="custom_prefix")
        async def test_function():
            return {"custom": "key"}

        loop = asyncio.get_event_loop()
        result = loop.run_until_complete(test_function())

        # Verify custom key prefix was used
        get_call_args = mock_redis.get.call_args[0]
        cache_key = get_call_args[0]
        assert cache_key.startswith("custom_prefix:")


if __name__ == "__main__":
    unittest.main()
