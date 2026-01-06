"""
Fetch - Default.

Fetch a URL using aiohttp with the specified method and parameters.

---

This is default fetch implementation using aiohttp to make HTTP requests.
An abstraction over aiohttp that provides structured logging and error handling.
"""

from __future__ import annotations

import aiohttp

from src.libs.log import get_context as _
from src.libs.log import get_logger

log = get_logger(__name__)


async def default_fetch(
    url: str,
    method: str,
    **kwargs: dict,
) -> tuple:
    """
    Fetch a URL with the given method and kwargs.

    Args:
        url (str): The URL to fetch.
        method (str): HTTP method.
        timeout (int): Timeout for the request in seconds (default: 10).
        **kwargs (dict): Additional arguments for the request.

    Returns:
        tuple: (response, json, error)
            response (aiohttp.ClientResponse): The response object.
            json (dict): The parsed JSON response.
            error (Exception | None): The exception if one occurred.

    """
    log.debug(f"{_()}: [{method}] {url}")

    if not url.startswith(("http://", "https://")):
        log.error(f"{_()}: Invalid URL: {url}")
        return None, {}, ValueError(f"Invalid URL: {url}")

    async with aiohttp.ClientSession() as session:
        target_method = getattr(session, method.lower(), None)

        if target_method is None:
            log.error(f"{_()}: Invalid method: {method}")
            return None, {}, AttributeError(f"Invalid method: {method}")

        try:
            response = await target_method(url=url, **kwargs)
        except aiohttp.ClientError as e:
            log.exception(f"{_()}: Client error while fetching {url}.")
            return None, None, e
        except Exception as e:
            log.exception(f"{_()}: Unexpected error while fetching {url}.")
            return None, None, e

        try:
            json = await response.json()
            error = None
        except aiohttp.ContentTypeError as e:
            log.warning(f"{_()}: Response is not JSON: {url}")
            json = {}
            error = e
        except Exception as e:
            log.exception(f"{_()}: Error while parsing JSON response.")
            json = {}
            error = e  # type: ignore[assignment]

        log.info(f"{_()}: Response status: {response.status} for {url}")

        return response, json, error
