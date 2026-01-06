"""
Roles - Enums.
"""

from enum import Enum


class RolesEnum(str, Enum):
    """
    Theme enum.
    """

    ADMIN = "admin"
    USER = "user"
    MODERATOR = "moderator"


class PermissionsEnum(str, Enum):
    """
    Permissions enum.
    """

    ADMIN = "admin"
    USER = "user"