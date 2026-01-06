"""
Test Authentication JWT Utilities.

This module tests the JWT utilities in the authentication middleware.
"""

import unittest
from datetime import UTC, datetime, timedelta
from unittest.mock import patch

import jwt
from fastapi import HTTPException

from src.libs.authentication.middleware.utils import (
    create_jwt,
    decode_jwt,
    deconstruct_auth_header,
    validate_token_info,
)


class TestAuthenticationJWT(unittest.TestCase):
    """Test Authentication JWT utilities."""

    def setUp(self):
        """Set up test fixtures."""
        self.test_secret = "test_secret_key"
        self.test_algorithm = "HS256"

    @patch("src.libs.authentication.middleware.utils.SECRET_KEY", "test_secret")
    @patch("src.libs.authentication.middleware.utils.ALGORITHM", "HS256")
    def test_create_jwt_default_expiry(self):
        """Test creating JWT with default expiry."""
        data = {"sub": "test_user", "role": "admin"}
        token = create_jwt(data)

        # Should return a string token
        self.assertIsInstance(token, str)
        # Should contain dots (JWT format)
        self.assertIn(".", token)

    @patch("src.libs.authentication.middleware.utils.SECRET_KEY", "test_secret")
    @patch("src.libs.authentication.middleware.utils.ALGORITHM", "HS256")
    def test_create_jwt_custom_expiry(self):
        """Test creating JWT with custom expiry."""
        data = {"sub": "test_user"}
        expires_delta = timedelta(hours=1)
        token = create_jwt(data, expires_delta)

        # Should return a string token
        self.assertIsInstance(token, str)

        # Decode to verify expiry
        decoded = jwt.decode(token, "test_secret", algorithms=["HS256"])
        exp_time = datetime.fromtimestamp(decoded["exp"], tz=UTC)
        expected_time = datetime.now(UTC) + expires_delta

        # Should be approximately the expected time (within 1 minute)
        self.assertLess(abs((exp_time - expected_time).total_seconds()), 60)

    @patch("src.libs.authentication.middleware.utils.SECRET_KEY", "test_secret")
    @patch("src.libs.authentication.middleware.utils.ALGORITHM", "HS256")
    def test_decode_jwt_valid(self):
        """Test decoding a valid JWT."""
        data = {"sub": "test_user", "role": "admin"}
        token = create_jwt(data)

        decoded = decode_jwt(token)

        # Should contain original data
        self.assertEqual(decoded["sub"], "test_user")
        self.assertEqual(decoded["role"], "admin")
        # Should have expiry
        self.assertIn("exp", decoded)

    @patch("src.libs.authentication.middleware.utils.SECRET_KEY", "test_secret")
    @patch("src.libs.authentication.middleware.utils.ALGORITHM", "HS256")
    def test_decode_jwt_expired(self):
        """Test decoding an expired JWT."""
        data = {"sub": "test_user"}
        # Create token that expires immediately
        expired_token = create_jwt(data, timedelta(seconds=-1))

        with self.assertRaises(ValueError) as context:
            decode_jwt(expired_token)

        self.assertIn("expired", str(context.exception).lower())

    @patch("src.libs.authentication.middleware.utils.SECRET_KEY", "test_secret")
    @patch("src.libs.authentication.middleware.utils.ALGORITHM", "HS256")
    def test_decode_jwt_invalid_token(self):
        """Test decoding an invalid JWT."""
        invalid_token = "invalid.token.here"

        with self.assertRaises(ValueError) as context:
            decode_jwt(invalid_token)

        # Check that an error is raised (message may vary)
        self.assertIsInstance(context.exception, ValueError)

    def test_deconstruct_auth_header_valid(self):
        """Test deconstructing a valid authorization header."""
        auth_header = "Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9"

        schema, token = deconstruct_auth_header(auth_header)

        self.assertEqual(schema, "Bearer")
        self.assertEqual(token, "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9")

    def test_deconstruct_auth_header_invalid_format(self):
        """Test deconstructing an invalid authorization header."""
        invalid_headers = [
            "Bearer",  # Missing token
            "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9",  # Missing schema
            "",  # Empty string
            "Bearer  ",  # Empty token
        ]

        for header in invalid_headers:
            with self.subTest(header=header):
                with self.assertRaises(HTTPException) as context:
                    deconstruct_auth_header(header)
                self.assertEqual(context.exception.status_code, 401)

    def test_deconstruct_auth_header_none(self):
        """Test deconstructing None authorization header."""
        with self.assertRaises(HTTPException) as context:
            deconstruct_auth_header(None)
        self.assertEqual(context.exception.status_code, 401)

    @patch("src.libs.authentication.middleware.utils.SECRET_KEY", "test_secret")
    @patch("src.libs.authentication.middleware.utils.ALGORITHM", "HS256")
    @patch("src.libs.authentication.middleware.utils.redis")
    def test_validate_token_info_valid(self, mock_redis):
        """Test validating a valid token info."""
        # Mock redis search to return a valid token
        mock_redis.search.return_value = [{"type": "access"}]

        data = {"sub": "test_user"}
        token = create_jwt(data)

        result = validate_token_info(token, "access")

        # Should return the decoded token data
        self.assertEqual(result["sub"], "test_user")

    @patch("src.libs.authentication.middleware.utils.SECRET_KEY", "test_secret")
    @patch("src.libs.authentication.middleware.utils.ALGORITHM", "HS256")
    def test_validate_token_info_invalid(self):
        """Test validating an invalid token info."""
        invalid_token = "invalid.token.here"

        with self.assertRaises(HTTPException) as context:
            validate_token_info(invalid_token)
        self.assertEqual(context.exception.status_code, 401)


if __name__ == "__main__":
    unittest.main()
