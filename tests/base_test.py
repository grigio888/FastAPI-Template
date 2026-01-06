"""
Base Test Case.

This module contain the BaseTestCase class that provides a base for testing.
"""

import unittest
from contextvars import ContextVar
from pathlib import Path
from unittest.mock import patch

from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from src.libs.authentication.middleware.utils import create_jwt
from src.main import app


class BaseTestCase(unittest.TestCase):
    """
    Test User API.

    This class will test the User API and Models.
    """

    def database_set_up(self) -> None:  # noqa: PLR0915
        """
        Set up test client, user, and SQLite database.

        This method will set up the test client, the user, and a SQLite database
        for the tests.
        """

        # Patch environment variables needed for Redis configuration
        patcher_redis_host = patch.dict(
            "os.environ",
            {
                "REDIS_HOST": "localhost",
                "REDIS_PORT": "6379",
                "REDIS_DB": "0",
                "SECRET_KEY": "test_secret_key",
                "ALGORITHM": "HS256",
                "EXCLUDED_PATHS": "",
                "AUTH_SERVICE_URL": "",
                "AUTH_VERIFY_ENDPOINT": "v1/token/validate",
                "ACCESS_UNIT": "hours",
                "ACCESS_VALUE": "1",
                "REFRESH_UNIT": "days",
                "REFRESH_VALUE": "1",
            },
        )
        self.addCleanup(patcher_redis_host.stop)
        patcher_redis_host.start()

        # Mock Redis client to avoid actual Redis connection during tests
        from unittest.mock import MagicMock

        mock_redis = MagicMock()
        mock_redis.search.return_value = [{"type": "access", "email": "admin@test.com"}]
        mock_redis.get.return_value = {"type": "access", "email": "admin@test.com"}
        mock_redis.set.return_value = None
        mock_redis.delete.return_value = None
        mock_redis.delete_pattern.return_value = None
        mock_redis.has_key.return_value = True

        patcher_redis_client = patch(
            "src.libs.authentication.middleware.utils.redis",
            mock_redis,
        )
        self.addCleanup(patcher_redis_client.stop)
        patcher_redis_client.start()

        patcher_redis_client_auth = patch("src.apps.auth.utils.redis", mock_redis)
        self.addCleanup(patcher_redis_client_auth.stop)
        patcher_redis_client_auth.start()

        patcher_redis_decorators = patch(
            "src.libs.authentication.decorators.redis",
            mock_redis,
        )
        self.addCleanup(patcher_redis_decorators.stop)
        patcher_redis_decorators.start()

        database_url = "sqlite:///test.db"

        # Patch the DATABASE_URL directly in the session module
        patcher_database_url = patch(
            "src.libs.database.session.DATABASE_URL",
            database_url,
        )
        self.addCleanup(patcher_database_url.stop)
        patcher_database_url.start()

        # Ensure we always start with a clean SQLite file-based database
        test_db_path = Path("test.db")
        if test_db_path.exists():
            test_db_path.unlink()

        # Create SQLite file-based database
        self.engine = create_engine(database_url)
        self.SessionLocal = sessionmaker(
            autocommit=False,
            autoflush=False,
            bind=self.engine,
        )

        # Patch engine and session factories used by the application
        patcher_engine = patch("src.libs.database.session.engine", self.engine)
        self.addCleanup(patcher_engine.stop)
        patcher_engine.start()

        patcher_session_factory = patch(
            "src.libs.database.session.SessionFactory",
            self.SessionLocal,
        )
        self.addCleanup(patcher_session_factory.stop)
        patcher_session_factory.start()

        patcher_session_alias = patch(
            "src.libs.database.session.Session",
            self.SessionLocal,
        )
        self.addCleanup(patcher_session_alias.stop)
        patcher_session_alias.start()

        patcher_session_local_alias = patch(
            "src.libs.database.session.SessionLocal",
            self.SessionLocal,
        )
        self.addCleanup(patcher_session_local_alias.stop)
        patcher_session_local_alias.start()

        patched_request_session = ContextVar("request_session", default=None)
        patcher_request_session = patch(
            "src.libs.database.session.request_session",
            patched_request_session,
        )
        self.addCleanup(patcher_request_session.stop)
        patcher_request_session.start()

        # Also patch the pagination module's db variable
        patcher_pagination_db = patch(
            "src.libs.database.pagination.db",
            self.SessionLocal(),
        )
        self.addCleanup(patcher_pagination_db.stop)
        patcher_pagination_db.start()

        from src.libs.database.base_model import BaseModel
        from src.libs.utilities.path import load_all_objects_from

        load_all_objects_from("models", "Model")
        BaseModel.metadata.create_all(self.engine)

        # Create a test admin user for authentication
        from src.apps.roles.models import PermissionsModel, RolesModel
        from src.apps.users.models import UsersModel
        from src.libs.authentication.middleware.hash import hash_sha512

        session = self.SessionLocal()

        # Seed minimal permissions and roles required for the test suites
        permissions_map = {}
        for permission_slug in ("admin", "user"):
            permission = (
                session.query(PermissionsModel)
                .filter_by(permission=permission_slug)
                .first()
            )
            if not permission:
                permission = PermissionsModel(permission=permission_slug)
                session.add(permission)
                session.flush()
            permissions_map[permission_slug] = permission

        admin_role = session.query(RolesModel).filter_by(slug="admin").first()
        if not admin_role:
            admin_role = RolesModel(
                slug="admin",
                title="Administrator",
                permissions=[permissions_map["admin"]],
            )
            session.add(admin_role)
            session.flush()

        user_role = session.query(RolesModel).filter_by(slug="user").first()
        if not user_role:
            user_role = RolesModel(
                slug="user",
                title="User",
                permissions=[permissions_map["user"]],
            )
            session.add(user_role)
            session.flush()

        session.commit()

        # Check if admin user already exists
        existing_admin = (
            session.query(UsersModel).filter_by(email="admin@test.com").first()
        )
        if not existing_admin:
            admin_user = UsersModel(
                first_name="Admin",
                last_name="Test",
                username="admin",
                email="admin@test.com",
                password=hash_sha512("AdminPassword123!"),
                role_id=admin_role.id,
                is_superuser=True,
            )
            session.add(admin_user)
            session.commit()
        session.close()

    def setUp(self) -> None:
        """
        Set up test client, user, and SQLite database.

        This method will set up the test client, the user, and a SQLite database for
        the tests.
        """
        self.database_set_up()

        self.client = TestClient(app)
        self.token = create_jwt({"sub": "admin@test.com"})
        self.client.headers.update({"Authorization": f"Bearer {self.token}"})

    def tearDown(self) -> None:
        """
        Clean up after tests.

        This method will remove the SQLite database file after tests.
        """
        super().tearDown()
        test_db = Path("test.db")
        if test_db.exists():
            test_db.unlink()


if __name__ == "__main__":
    unittest.main()
