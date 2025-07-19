"""
Test Todo.

This module will test the Todo API.
"""

import unittest

from fastapi.testclient import TestClient

from src.main import app


class TestHealthCheckEndpoints(unittest.TestCase):
    """
    Test Health Check Endpoints.

    This class will test the Health Check Endpoints.
    """

    def setUp(self) -> None:
        """
        Set up test client and health check.

        This method will set up the test client and the health check for the tests.
        """
        self.client = TestClient(app)

    def test_health_check(self) -> None:
        """
        Test health check.

        This test will check if the health check endpoint is working.
        """

        response = self.client.get("/")

        assert response.status_code == 200, "Response status code is not 200"


if __name__ == "__main__":
    unittest.main()
