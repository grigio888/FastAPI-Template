"""
Seeds - Users.

This module contains the seed data for the Users.
"""

from faker import Faker

from src.apps.roles.models import RolesModel
from src.apps.users.enums import ColorEnum, ReadingModeEnum, ThemeEnum
from src.apps.users.models import UserPreferencesModel, UsersModel
from src.libs.authentication.middleware.hash import hash_sha512
from src.libs.database.session import get_session
from src.libs.log import get_context as _
from src.libs.log import get_logger

db = get_session()
log = get_logger()
fake = Faker()


def seed_users(number: int = 50) -> None:
    """
    Seed the users table with initial data.

    """

    log.debug(f"{_()}: Seeding users table with {number} users...")

    if number < 1:
        log.warning(
            f"{_()}: Number of users to seed must be at least 1. Defaulting to 50.",
        )
        number = 50

    users = [
        UsersModel(
            first_name="Site",
            last_name="Administrator",
            username="admin",
            email="admin@template.local",
            password=hash_sha512("Password123!"),
            bio="Administrator of Template",
            role_id=1,
            is_active=True,
        ),
    ] + [
        UsersModel(
            first_name=fake.first_name(),
            last_name=fake.last_name(),
            username=fake.user_name(),
            email=fake.email(
                safe=True,
                domain=fake.free_email_domain(),
            ),
            password=hash_sha512(
                fake.password(
                    length=12,
                    special_chars=True,
                    digits=True,
                    upper_case=True,
                    lower_case=True,
                ),
            ),
            bio=fake.text(max_nb_chars=400),
            role_id=fake.random_int(min=2, max=RolesModel.query().count()),
            is_active=fake.boolean(chance_of_getting_true=75),
        )
        for _ in range(number)
    ]

    db.add_all(users)
    db.commit()

    log.info(f"{_()}: Successfully seeded {number} users.")


def seed_preferences() -> None:
    """
    Seed preferences for all users.
    """

    log.debug(f"{_()}: Seeding preferences for all users...")

    users = UsersModel.query().all()

    for user in users:
        if not user.preferences:
            user.preferences = UserPreferencesModel(
                theme=ThemeEnum.dark.value,
                color=ColorEnum.purple.value,
                reading_mode=ReadingModeEnum.horizontal.value,
            )

    db.commit()

    log.info(f"{_()}: Successfully seeded preferences for all users.")


depends_on = ["roles"]
__all__ = ["seed_preferences", "seed_users"]
