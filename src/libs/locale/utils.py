"""
Locale - Messages - Metaclass.

This module contains the metaclass for the messages.
"""

from typing import cast


def c_str(obj: object) -> str:
    """
    Cast an object to a string.

    This function is used to cast an object to a string type.
    """

    return cast(str, obj)
