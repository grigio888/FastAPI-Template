"""
Test Fetch Module.

This module tests the fetch utilities in src/libs/fetch/.
"""

import asyncio
import unittest
from unittest.mock import AsyncMock, MagicMock, patch

import aiohttp

from src.libs.fetch.default import default_fetch
from src.libs.fetch.mock import mock_fetch


class TestFetchModule(unittest.TestCase):
    """Test fetch module functionality."""

    def test_mock_fetch_successful_response(self):
        """Test mock_fetch with successful response."""
        mocked_data = {
            "response": {"status": 200},
            "json": {"message": "success", "data": [1, 2, 3]},
            "error": None,
        }

        # Run async test
        loop = asyncio.get_event_loop()
        response, json_data, error = loop.run_until_complete(
            mock_fetch("http://example.com", "GET", mocked_data),
        )

        self.assertEqual(response.url, "http://example.com")
        self.assertEqual(response.method, "GET")
        self.assertEqual(response.status, 200)
        self.assertEqual(json_data, {"message": "success", "data": [1, 2, 3]})
        self.assertIsNone(error)

    def test_mock_fetch_error_response(self):
        """Test mock_fetch with error response."""
        test_error = aiohttp.ContentTypeError(
            MagicMock(),
            (),
            message="Not JSON",
        )

        mocked_data = {
            "response": {"status": 400},
            "json": {"error": "Bad request"},
            "error": test_error,
        }

        # Run async test
        loop = asyncio.get_event_loop()
        response, json_data, error = loop.run_until_complete(
            mock_fetch("http://example.com/error", "POST", mocked_data),
        )

        self.assertEqual(response.url, "http://example.com/error")
        self.assertEqual(response.method, "POST")
        self.assertEqual(response.status, 400)
        self.assertIsNone(json_data)
        self.assertEqual(error, test_error)

    def test_mock_fetch_default_values(self):
        """Test mock_fetch with minimal mocked data."""
        mocked_data = {}

        # Run async test
        loop = asyncio.get_event_loop()
        response, json_data, error = loop.run_until_complete(
            mock_fetch("http://example.com", "GET", mocked_data),
        )

        self.assertEqual(response.status, 200)  # Default status
        self.assertEqual(json_data, {})  # Default empty dict
        self.assertIsNone(error)

    def test_mock_response_json_method(self):
        """Test MockResponse.json() method."""
        mocked_data = {
            "json": {"test": "data"},
        }

        # Run async test
        loop = asyncio.get_event_loop()
        response, _, _ = loop.run_until_complete(
            mock_fetch("http://example.com", "GET", mocked_data),
        )

        # Test that json() method works
        json_result = loop.run_until_complete(response.json())
        self.assertEqual(json_result, {"test": "data"})

    def test_mock_response_json_method_with_exception(self):
        """Test MockResponse.json() method raises exception."""
        test_error = aiohttp.ContentTypeError(
            MagicMock(),
            (),
            message="Not JSON",
        )

        mocked_data = {
            "json": test_error,
        }

        # Run async test
        loop = asyncio.get_event_loop()
        response, _, _ = loop.run_until_complete(
            mock_fetch("http://example.com", "GET", mocked_data),
        )

        # Test that json() method raises the exception
        with self.assertRaises(aiohttp.ContentTypeError):
            loop.run_until_complete(response.json())

    @patch("aiohttp.ClientSession")
    def test_default_fetch_successful_request(self, mock_session_class):
        """Test default_fetch with successful request."""
        # Mock the session and response
        mock_response = AsyncMock()
        mock_response.status = 200
        mock_response.json.return_value = {"success": True}

        mock_method = AsyncMock(return_value=mock_response)

        mock_session = AsyncMock()
        mock_session.get = mock_method
        mock_session.__aenter__.return_value = mock_session
        mock_session.__aexit__.return_value = None

        mock_session_class.return_value = mock_session

        # Run async test
        loop = asyncio.get_event_loop()
        response, json_data, error = loop.run_until_complete(
            default_fetch("http://example.com", "GET"),
        )

        self.assertEqual(response, mock_response)
        self.assertEqual(json_data, {"success": True})
        self.assertIsNone(error)

        # Verify session was used correctly
        mock_session_class.assert_called_once()
        mock_method.assert_called_once_with(url="http://example.com")

    @patch("aiohttp.ClientSession")
    def test_default_fetch_with_kwargs(self, mock_session_class):
        """Test default_fetch with additional kwargs."""
        mock_response = AsyncMock()
        mock_response.status = 201
        mock_response.json.return_value = {"created": True}

        mock_method = AsyncMock(return_value=mock_response)

        mock_session = AsyncMock()
        mock_session.post = mock_method
        mock_session.__aenter__.return_value = mock_session
        mock_session.__aexit__.return_value = None

        mock_session_class.return_value = mock_session

        # Run async test with kwargs
        loop = asyncio.get_event_loop()
        response, json_data, error = loop.run_until_complete(
            default_fetch(
                "https://api.example.com/users",
                "POST",
                headers={"Content-Type": "application/json"},
                json={"name": "test"},
            ),
        )

        self.assertEqual(response, mock_response)
        self.assertEqual(json_data, {"created": True})
        self.assertIsNone(error)

        # Verify kwargs were passed
        mock_method.assert_called_once_with(
            url="https://api.example.com/users",
            headers={"Content-Type": "application/json"},
            json={"name": "test"},
        )

    def test_default_fetch_invalid_url(self):
        """Test default_fetch with invalid URL."""
        # Run async test
        loop = asyncio.get_event_loop()
        response, json_data, error = loop.run_until_complete(
            default_fetch("invalid-url", "GET"),
        )

        self.assertIsNone(response)
        self.assertEqual(json_data, {})
        self.assertIsInstance(error, ValueError)
        self.assertIn("Invalid URL", str(error))

    @patch("aiohttp.ClientSession")
    def test_default_fetch_invalid_method(self, mock_session_class):
        """Test default_fetch with invalid HTTP method."""
        mock_session = AsyncMock()
        # Mock session doesn't have the invalid method
        mock_session.invalid_method = None
        mock_session.__aenter__.return_value = mock_session
        mock_session.__aexit__.return_value = None

        mock_session_class.return_value = mock_session

        # Run async test
        loop = asyncio.get_event_loop()
        response, json_data, error = loop.run_until_complete(
            default_fetch("http://example.com", "INVALID_METHOD"),
        )

        self.assertIsNone(response)
        self.assertEqual(json_data, {})
        self.assertIsInstance(error, AttributeError)
        self.assertIn("Invalid method", str(error))

    @patch("aiohttp.ClientSession")
    def test_default_fetch_client_error(self, mock_session_class):
        """Test default_fetch with aiohttp ClientError."""
        mock_method = AsyncMock(side_effect=aiohttp.ClientError("Connection failed"))

        mock_session = AsyncMock()
        mock_session.get = mock_method
        mock_session.__aenter__.return_value = mock_session
        mock_session.__aexit__.return_value = None

        mock_session_class.return_value = mock_session

        # Run async test
        loop = asyncio.get_event_loop()
        response, json_data, error = loop.run_until_complete(
            default_fetch("http://example.com", "GET"),
        )

        self.assertIsNone(response)
        self.assertIsNone(json_data)
        self.assertIsInstance(error, aiohttp.ClientError)

    @patch("aiohttp.ClientSession")
    def test_default_fetch_json_parse_error(self, mock_session_class):
        """Test default_fetch with JSON parsing error."""
        mock_response = AsyncMock()
        mock_response.status = 200
        mock_response.json.side_effect = aiohttp.ContentTypeError(
            MagicMock(),
            (),
            message="Not JSON",
        )

        mock_method = AsyncMock(return_value=mock_response)

        mock_session = AsyncMock()
        mock_session.get = mock_method
        mock_session.__aenter__.return_value = mock_session
        mock_session.__aexit__.return_value = None

        mock_session_class.return_value = mock_session

        # Run async test
        loop = asyncio.get_event_loop()
        response, json_data, error = loop.run_until_complete(
            default_fetch("http://example.com", "GET"),
        )

        self.assertEqual(response, mock_response)
        self.assertEqual(json_data, {})
        self.assertIsInstance(error, aiohttp.ContentTypeError)

    @patch("aiohttp.ClientSession")
    def test_default_fetch_unexpected_error(self, mock_session_class):
        """Test default_fetch with unexpected error."""
        mock_method = AsyncMock(side_effect=RuntimeError("Unexpected error"))

        mock_session = AsyncMock()
        mock_session.get = mock_method
        mock_session.__aenter__.return_value = mock_session
        mock_session.__aexit__.return_value = None

        mock_session_class.return_value = mock_session

        # Run async test
        loop = asyncio.get_event_loop()
        response, json_data, error = loop.run_until_complete(
            default_fetch("http://example.com", "GET"),
        )

        self.assertIsNone(response)
        self.assertIsNone(json_data)
        self.assertIsInstance(error, RuntimeError)


if __name__ == "__main__":
    unittest.main()
