"""
Test Middleware Index Module.

This module tests the middleware index in src/libs/middleware.py.
"""

import unittest

from src.libs import middleware


class TestMiddlewareIndex(unittest.TestCase):
    """Test middleware index functionality."""

    def test_middleware_imports_available(self) -> None:
        """Test that all middleware imports are available."""
        expected_middlewares = [
            "DBMiddleware",
            "CORSMiddleware",
            "JWTMiddleware",
            "LocalizationMiddleware",
            "LoggingMiddleware",
        ]

        for middleware_name in expected_middlewares:
            with self.subTest(middleware=middleware_name):
                assert hasattr(middleware, middleware_name)

    def test_all_list_defined(self) -> None:
        """Test that __all__ list is properly defined."""
        assert hasattr(middleware, "__all__")
        assert isinstance(middleware.__all__, list)

        expected_count = 5  # Number of middlewares
        assert len(middleware.__all__) == expected_count

    def test_all_list_contains_expected_middlewares(self) -> None:
        """Test that __all__ contains all expected middleware names."""
        expected_middlewares = {
            "DBMiddleware",
            "CORSMiddleware",
            "JWTMiddleware",
            "LocalizationMiddleware",
            "LoggingMiddleware",
        }

        actual_middlewares = set(middleware.__all__)
        assert actual_middlewares == expected_middlewares


if __name__ == "__main__":
    unittest.main()
