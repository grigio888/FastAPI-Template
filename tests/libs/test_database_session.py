"""
Database session behaviour tests.
"""

import pytest
from sqlalchemy.exc import IntegrityError

from tests.base_test import BaseTestCase


class TestDatabaseSession(BaseTestCase):
    """Validate session cleanup after failures."""

    def test_session_recovers_after_integrity_error(self) -> None:
        """
        Test that the database session recovers after an IntegrityError.
        """

        from src.apps.roles.models import RolesModel
        from src.apps.users.models import UsersModel

        role = RolesModel(slug="test-role", title="Test Role")
        role.save()

        user = UsersModel(
            first_name="Integrity",
            last_name="Check",
            username="integrity-check",
            email="integrity@example.com",
            password="pass",  # noqa: S106
            role_id=role.id,
        )
        user.save()

        duplicate = UsersModel(
            first_name="Integrity",
            last_name="Clone",
            username="integrity-clone",
            email="integrity@example.com",
            password="pass",  # noqa: S106
            role_id=role.id,
        )

        with pytest.raises(IntegrityError):
            duplicate.save()

        assert (
            UsersModel.query().filter_by(email="integrity@example.com").first().id
            == user.id
        )
