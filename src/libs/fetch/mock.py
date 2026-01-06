"""
Fetch - Mock.

This module provides a mock implementation of the fetch function for testing purposes.

---

This module provides a mock implementation of the fetch function for testing purposes.
Whenever is passed mocked_data to the fetch function, this mock_fetch will be used to
simulate HTTP requests and responses.
"""

from __future__ import annotations

from src.libs.log import get_logger

log = get_logger(__name__)


async def mock_fetch(
    url: str,
    method: str,
    mocked_data: dict,
) -> tuple:
    """
    Mock a Fetch request with the provided data.

    This method is used to mock a fetch request based on the mocked data.
    Mocked data should follow this structure:

    mocked_data: dict[str, dict | None | Exception] = {
        "response": {
            "status": 500,
        },
        "json": {"error": "Internal error"},
        "error": aiohttp.ContentTypeError(...) or any Exception
    }

    Returns:
        tuple: (MockResponse, json, error)

    """

    class MockResponse:
        """
        A mock aiohttp.ClientResponse-like object.
        """

        def __init__(
            self,
            url: str,
            method: str,
            status: int = 200,
            json_data: dict | None = None,
        ) -> None:
            """Mock constructor."""
            self.url = url
            self.method = method
            self.status = status
            self._json_data = json_data or {}

        async def json(self) -> dict:
            if isinstance(self._json_data, Exception):
                raise self._json_data
            return self._json_data

    response_data = mocked_data.get("response", {})
    json_data = mocked_data.get("json", {})
    error = mocked_data.get("error")

    # Create mock response
    mock_response = MockResponse(
        url=url,
        method=method,
        status=response_data.get("status", 200),
        json_data=json_data,
    )

    # Simulate an error response (e.g., .json() raises ContentTypeError)
    if isinstance(error, Exception):
        return mock_response, None, error

    return mock_response, json_data, None
