"""
Test Todo.

This module will test the Todo API.
"""

import unittest
from contextvars import ContextVar
from pathlib import Path
from unittest.mock import patch

from alembic import command
from alembic.config import Config
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from src.apps.todos.schemas import TodoDataSchema
from src.libs.authentication.middleware.utils import create_jwt
from src.main import app


class TestTodoAPI(unittest.TestCase):
    """
    Test Todo API.

    This class will test the Todo API.
    """

    def database_set_up(self) -> None:
        """
        Set up test client, todo, and SQLite database.

        This method will set up the test client, the todo, and a SQLite database
        for the tests.
        """

        database_url = "sqlite:///test.db"

        # Patch the DATABASE_URL directly in the session module
        patcher_database_url = patch(
            "src.libs.database.session.DATABASE_URL",
            database_url,
        )
        self.addCleanup(patcher_database_url.stop)
        patcher_database_url.start()

        # Create SQLite file-based database
        self.engine = create_engine(database_url)
        self.SessionLocal = sessionmaker(
            autocommit=False,
            autoflush=False,
            bind=self.engine,
        )

        # Patch the session creation
        patcher_session = patch("src.libs.database.session.Session", self.SessionLocal)
        self.addCleanup(patcher_session.stop)
        patcher_session.start()

        # Patch the request_session ContextVar
        patched_request_session = ContextVar(
            "request_session",
            default=self.SessionLocal(),  # noqa: B039
        )
        patcher_request_session = patch(
            "src.libs.database.session.request_session",
            patched_request_session,
        )
        self.addCleanup(patcher_request_session.stop)
        patcher_request_session.start()

        # Use the session's engine for Alembic migrations
        alembic_cfg = Config("alembic.ini")
        command.upgrade(alembic_cfg, "head")

    def setUp(self) -> None:
        """
        Set up test client, todo, and SQLite database.

        This method will set up the test client, the todo, and a SQLite database for
        the tests.
        """
        self.database_set_up()

        self.client = TestClient(app)

        self.todo = TodoDataSchema(
            name="Test Todo",
            percentage=50.0,
            description="This is a test todo",
        )

        self.token = create_jwt({"sub": "test"})
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

    def test_create_todo(self) -> None:
        """
        Test create todo.

        This test will create a todo and then try to get it.
        """

        response = self.client.post("/todos/", json=self.todo.model_dump())

        assert response.status_code == 201, "Response status code is not 201"

        for key, value in response.json().items():
            if key == "id":
                assert value == 1, "Response ID is not 1"
                continue

            current_value = getattr(self.todo, key, None)

            assert current_value == value, f"Response {key} is not the same as the todo"

    def test_list_todos(self) -> None:
        """
        Test list todos.

        This test will create 20 todos and then try to get them.
        """

        for _ in range(1, 21):
            todo = TodoDataSchema(**self.todo.model_dump())
            self.client.post("/todos/", json=todo.model_dump())

        response = self.client.get("/todos/?page=1&limit=10")

        assert response.status_code == 200, "Response status code is not 200"
        assert len(response.json()["items"]) == 10, "Response items length is not 10"
        assert response.json()["total_pages"] == 2, "Response total pages is not 2"
        assert response.json()["current_page"] == 1, "Response current page is not 1"

    def test_list_todos_second_page(self) -> None:
        """
        Test list todos second page.

        This test will create 20 todos and then try to get the second page with
        10 items.
        """

        for _ in range(1, 31):
            todo = TodoDataSchema(**self.todo.model_dump())
            self.client.post("/todos/", json=todo.model_dump())

        response = self.client.get("/todos/?page=2&limit=10")

        assert response.status_code == 200, "Response status code is not 200"
        assert len(response.json()["items"]) == 10, "Response items length is not 10"
        assert response.json()["total_pages"] == 3, (
            f"Response total pages is not 3, is {response.json()['total_pages']}"
        )
        assert response.json()["current_page"] == 2, "Response current page is not 2"

    def test_get_todo(self) -> None:
        """
        Test get todo.

        This test will create a todo and then try to get it.
        """

        self.client.post("/todos/", json=self.todo.model_dump())

        response = self.client.get("/todos/1")

        assert response.status_code == 200, "Response status code is not 200"

        for key, value in response.json().items():
            if key == "id":
                if value != 1:
                    # The first todo should have id 1
                    assert value == 1, "Response ID is not 1"
                continue

            current_value = getattr(self.todo, key, None)

            if current_value != value:
                assert current_value == value, (
                    f"Response {key} is not the same as the todo"
                )

    def test_update_todo(self) -> None:
        """
        Test update todo.

        This test will create a todo, update it and then try to get it.
        """

        self.client.post("/todos/", json=self.todo.model_dump())

        updated_todo = TodoDataSchema(**self.todo.model_dump())
        updated_todo.name = "Updated Test Todo"
        response = self.client.put(
            "/todos/1",
            json=updated_todo.model_dump(),
        )

        assert response.status_code == 200, "Response status code is not 200"
        assert response.json()["name"] == "Updated Test Todo", (
            "Response name is not the same as the updated todo"
        )

    def test_delete_todo(self) -> None:
        """
        Test delete todo.

        This test will create a todo, delete it and then try to get it.
        """

        self.client.post("/todos/", json=self.todo.model_dump())

        response = self.client.delete("/todos/1")

        assert response.status_code == 204, "Response status code is not 204"

        response = self.client.get("/todos/1")

        assert response.status_code == 404, "Response status code is not 404"

    def test_get_todo_not_found(self) -> None:
        """
        Test get todo when the todo does not exist.
        """
        response = self.client.get("/todos/999")  # Non-existent ID
        assert response.status_code == 404, "Response status code is not 404"

    def test_update_todo_not_found(self) -> None:
        """
        Test update todo when the todo does not exist.
        """
        updated_todo = TodoDataSchema(**self.todo.model_dump())
        updated_todo.name = "Updated Test Todo"
        response = self.client.put(
            "/todos/999",  # Non-existent ID
            json=updated_todo.model_dump(),
        )
        assert response.status_code == 404, "Response status code is not 404"

    def test_delete_todo_not_found(self) -> None:
        """
        Test delete todo when the todo does not exist.
        """
        response = self.client.delete("/todos/999")  # Non-existent ID
        assert response.status_code == 404, "Response status code is not 404"

    def test_create_todo_empty_list(self) -> None:
        """
        Test create todo when the todos list is empty.
        """

        response = self.client.post("/todos/", json=self.todo.model_dump())
        assert response.status_code == 201, "Response status code is not 201"
        assert response.json()["id"] == 1, "Response ID is not 1"


if __name__ == "__main__":
    unittest.main()
