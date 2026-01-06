"""
Seeds - Roles.

This module contains the seed data for the Roles.
"""

from faker import Faker

from src.apps.roles.models import PermissionsModel, RolesModel
from src.libs.database.session import get_session
from src.libs.log import get_context as _
from src.libs.log import get_logger

db = get_session()
log = get_logger()
fake = Faker()


permissions = [
    "admin",
    "moderator",
    "user",
]
roles = [
    {
        "slug": "admin",
        "title": "Admin",
        "permissions": [
            "admin",
        ],
    },
    {
        "slug": "user",
        "title": "Usuário",
        "permissions": [
            "user",
        ],
    },
]


def seed_permissions() -> None:
    """
    Seed the permissions table with initial data.
    """

    log.debug(
        f"{_()}: Seeding permissions table with {len(permissions)} permissions...",
    )

    perm_models = [
        PermissionsModel(permission=permission) for permission in permissions
    ]

    db.add_all(perm_models)
    db.commit()

    log.info(f"{_()}: Successfully seeded permissions table.")


def seed_roles() -> None:
    """
    Seed the roles table with initial data.

    """

    log.debug(f"{_()}: Seeding roles table with {len(roles)} roles...")

    role_models = [
        RolesModel(
            slug=role["slug"],
            title=role["title"],
            permissions=PermissionsModel.query()
            .filter(
                PermissionsModel.permission.in_(role["permissions"]),
            )
            .all(),
        )
        for role in roles
    ]

    db.add_all(role_models)
    db.commit()

    log.info(f"{_()}: Successfully seeded {len(role_models)} roles.")


depends_on = None
__all__ = ["seed_permissions", "seed_roles"]
