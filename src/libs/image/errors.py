"""
Image - Errors.

This module defines custom exceptions for image handling errors.
"""

from __future__ import annotations


class InvalidImageError(Exception):
    """Exception raised for invalid image format."""

    def __init__(self, message: str = "Invalid image format.") -> None:
        """Initialize the exception."""

        super().__init__(message)


class ImageTooLargeError(Exception):
    """Exception raised for image size exceeding limit."""

    def __init__(
        self,
        message: str = "Image size exceeds the limit.",
        size: int | None = None,
    ) -> None:
        """Initialize the exception."""

        if size:
            message = f"{message} Size: {size} MB."

        super().__init__(message)
