"""
Fetch - Index.
"""

from __future__ import annotations

from src.libs.fetch.default import default_fetch
from src.libs.fetch.mock import mock_fetch


async def fetch(
    url: str,
    method: str = "GET",
    **kwargs: dict,
) -> tuple:
    """
    Fetch a URL with the given method and kwargs.

    Args:
        url (str): The URL to fetch.
        method (str): HTTP method (default: "GET").
        timeout (int): Timeout for the request in seconds (default: 10).
        **kwargs (dict): Additional arguments for the request.

    Returns:
        tuple: (response, json, error)
            response (aiohttp.ClientResponse): The response object.
            json (dict): The parsed JSON response.
            error (Exception | None): The exception if one occurred.

    """

    if mocked_data := kwargs.pop("mocked_data", None):
        return await mock_fetch(url, method, mocked_data=mocked_data)

    return await default_fetch(url, method, **kwargs)
