"""
Utilities for hashing.

This module contains utilities for hashing.
"""

from __future__ import annotations

import base64
import hashlib
import random
import string


def decode_b64(hashed: str) -> str:
    """
    Decode a base64 hash.

    This function will decode a base64 hash.
    """

    return base64.b64decode(hashed).decode()


def encode_b64(string: str) -> str:
    """
    Encode a base64 hash.

    This function will encode a base64 hash.
    """

    return base64.b64encode(string.encode()).decode()


def hash_sha512(string: str) -> str:
    """
    Hash a sensitive information.

    This function will hash a sensitive information using SHA-512.
    """

    return base64.b64encode(
        hashlib.sha512(
            string.encode(),
        ).digest(),
    ).decode()


def is_hash_valid(hashed_data: str) -> bool:
    """
    Check if a hashed data is valid.
    """

    return isinstance(hashed_data, str) and len(hashed_data) == 88


def compare_hash(to_compare: str, hashed_data: str) -> bool:
    """
    Compare a information agaisnt a hashed data.

    This function will compare a information against a hashed data.
    """

    return hash_sha512(to_compare) == hashed_data


def generate_random_string(
    size: int = 12,
    include_letters: bool = True,
    include_digits: bool = True,
    include_special: bool = False,
) -> str:
    """
    Generate a random string.
    """

    characters = ""

    if include_letters:
        characters += string.ascii_letters
    if include_digits:
        characters += string.digits
    if include_special:
        characters += string.punctuation

    phrase = "".join(random.choice(characters) for _ in range(size))  # noqa: S311

    return base64.b64encode(phrase.encode()).decode()
