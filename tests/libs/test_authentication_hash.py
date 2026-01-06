"""
Test Authentication Hash Utilities.

This module tests the hash utilities in the authentication middleware.
"""

import unittest

from src.libs.authentication.middleware.hash import (
    compare_hash,
    decode_b64,
    encode_b64,
    generate_random_string,
    hash_sha512,
)


class TestAuthenticationHash(unittest.TestCase):
    """Test Authentication Hash utilities."""

    def test_encode_b64(self):
        """Test base64 encoding."""
        test_string = "test_string"
        encoded = encode_b64(test_string)

        # Should return a valid base64 string
        self.assertIsInstance(encoded, str)
        # Should be different from original
        self.assertNotEqual(encoded, test_string)

    def test_decode_b64(self):
        """Test base64 decoding."""
        test_string = "test_string"
        encoded = encode_b64(test_string)
        decoded = decode_b64(encoded)

        # Should decode back to original string
        self.assertEqual(decoded, test_string)

    def test_encode_decode_roundtrip(self):
        """Test that encoding then decoding returns the original."""
        test_strings = ["hello", "world", "test with spaces", "123", ""]

        for test_string in test_strings:
            with self.subTest(test_string=test_string):
                encoded = encode_b64(test_string)
                decoded = decode_b64(encoded)
                self.assertEqual(decoded, test_string)

    def test_hash_sha512(self):
        """Test SHA-512 hashing."""
        test_string = "password123"
        hashed = hash_sha512(test_string)

        # Should return a valid hash string
        self.assertIsInstance(hashed, str)
        # Should be different from original
        self.assertNotEqual(hashed, test_string)
        # Should be consistent
        self.assertEqual(hashed, hash_sha512(test_string))

    def test_hash_sha512_different_inputs(self):
        """Test that different inputs produce different hashes."""
        hash1 = hash_sha512("password1")
        hash2 = hash_sha512("password2")

        self.assertNotEqual(hash1, hash2)

    def test_compare_hash_valid(self):
        """Test comparing a string against its hash."""
        test_string = "mypassword"
        hashed = hash_sha512(test_string)

        # Should return True for correct comparison
        self.assertTrue(compare_hash(test_string, hashed))

    def test_compare_hash_invalid(self):
        """Test comparing a string against a different hash."""
        test_string = "mypassword"
        wrong_string = "wrongpassword"
        hashed = hash_sha512(test_string)

        # Should return False for incorrect comparison
        self.assertFalse(compare_hash(wrong_string, hashed))

    def test_generate_random_string_default(self):
        """Test generating random string with default parameters."""
        random_str = generate_random_string()

        # Should return a string
        self.assertIsInstance(random_str, str)
        # Should not be empty
        self.assertGreater(len(random_str), 0)

    def test_generate_random_string_different_sizes(self):
        """Test generating random strings with different sizes."""
        sizes = [5, 10, 20, 50]

        for size in sizes:
            with self.subTest(size=size):
                random_str = generate_random_string(size=size)
                self.assertIsInstance(random_str, str)
                # Since it's base64 encoded, length will be different
                self.assertGreater(len(random_str), 0)

    def test_generate_random_string_character_options(self):
        """Test generating random strings with different character options."""
        # Only letters
        letters_only = generate_random_string(
            size=10,
            include_letters=True,
            include_digits=False,
            include_special=False,
        )
        self.assertIsInstance(letters_only, str)

        # Only digits
        digits_only = generate_random_string(
            size=10,
            include_letters=False,
            include_digits=True,
            include_special=False,
        )
        self.assertIsInstance(digits_only, str)

        # All character types
        all_chars = generate_random_string(
            size=10,
            include_letters=True,
            include_digits=True,
            include_special=True,
        )
        self.assertIsInstance(all_chars, str)

    def test_generate_random_string_uniqueness(self):
        """Test that generated random strings are unique."""
        strings = [generate_random_string() for _ in range(10)]

        # All strings should be unique
        self.assertEqual(len(strings), len(set(strings)))


if __name__ == "__main__":
    unittest.main()
