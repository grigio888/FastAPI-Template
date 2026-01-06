"""
Test User.

This module will test the User API and Models.
"""

import unittest

from src.apps.users.schemas import UserDataSchema, UserUpdateDataSchema
from tests.base_test import BaseTestCase


class TestUserAPI(BaseTestCase):
    """
    Test User API.

    This class will test the User API and Models.
    """

    def setUp(self) -> None:
        """
        Set up test client, user, and SQLite database.

        This method will set up the test client, the user, and a SQLite database for
        the tests.
        """
        super().setUp()

        self.user = UserDataSchema(
            first_name="John",
            last_name="Doe",
            username="johndoe",
            email="john.doe@example.com",
            password="Password123!",  # noqa: S106
        )

    def tearDown(self) -> None:
        """
        Clean up after tests.

        This method will remove the SQLite database file after tests.
        """
        super().tearDown()

    def test_create_user(self) -> None:
        """
        Test create user.

        This test will create a user and verify the response.
        """

        response = self.client.post("/users/create", json=self.user.model_dump())

        assert response.status_code == 201, "Response status code is not 201"

        response_data = response.json()
        assert "id" in response_data, "Response should contain an ID"
        assert response_data["id"] > 0, "Response ID should be positive"
        assert response_data["first_name"] == self.user.first_name, (
            "First name mismatch"
        )
        assert response_data["last_name"] == self.user.last_name, "Last name mismatch"
        assert response_data["username"] == self.user.username, "Username mismatch"
        assert response_data["email"] == self.user.email, "Email mismatch"
        assert response_data["is_active"] is True, "User should be active by default"
        assert response_data["is_superuser"] is False, (
            "User should not be superuser by default"
        )
        assert "password" not in response_data, "Password should not be in response"

    def test_create_user_duplicate_email(self) -> None:
        """
        Test create user with duplicate email.

        This test will try to create two users with the same email.
        """

        # Create first user
        response = self.client.post("/users/create", json=self.user.model_dump())
        assert response.status_code == 201, "First user creation failed"

        # Try to create second user with same email
        duplicate_user = UserDataSchema(
            first_name="Jane",
            last_name="Smith",
            username="janesmith",
            email=self.user.email,  # Same email
            password="Password456!",  # noqa: S106
        )

        response = self.client.post("/users/create", json=duplicate_user.model_dump())
        assert response.status_code == 400, "Should return 400 for duplicate email"

    def test_create_user_invalid_email(self) -> None:
        """
        Test create user with invalid email format.

        This test will try to create a user with an invalid email.
        """

        # Using dict instead of UserDataSchema to avoid validation at schema level
        invalid_user_data = {
            "first_name": "John",
            "last_name": "Doe",
            "username": "johndoe",
            "email": "invalid-email",
            "password": "password123",
        }

        response = self.client.post("/users/create", json=invalid_user_data)
        assert response.status_code == 406, "Should return 406 for invalid email"

    def test_create_user_weak_password(self) -> None:
        """
        Test create user with weak password.

        This test will try to create a user with a password that doesn't meet
        requirements.
        """

        # Using dict instead of UserDataSchema to avoid validation at schema level
        weak_password_user_data = {
            "first_name": "John",
            "last_name": "Doe",
            "username": "johndoe",
            "email": "john.doe@example.com",
            "password": "123",  # Too short and no letters
        }

        response = self.client.post("/users/create", json=weak_password_user_data)
        assert response.status_code == 406, "Should return 406 for weak password"

    def test_list_users(self) -> None:
        """
        Test list users.

        This test will create multiple users and then list them.
        """

        # Create multiple users
        for i in range(1, 6):
            user = UserDataSchema(
                first_name=f"User{i}",
                last_name=f"Test{i}",
                username=f"user{i}",
                email=f"user{i}@example.com",
                password="Password123!",  # noqa: S106
            )
            self.client.post("/users/create", json=user.model_dump())

        response = self.client.get("/users/?page=1&limit=3")

        assert response.status_code == 200, "Response status code is not 200"
        response_data = response.json()
        assert len(response_data["items"]) == 3, "Should return 3 users"
        assert response_data["total_pages"] == 2, "Should have 2 total pages"
        assert response_data["current_page"] == 1, "Current page should be 1"

    def test_list_users_admin_only(self) -> None:
        """
        Test list users when only admin user exists.

        This test will list users when only the admin user exists in the database.
        """

        response = self.client.get("/users/?page=1&limit=10")

        assert response.status_code == 200, "Response status code is not 200"
        response_data = response.json()
        assert len(response_data["items"]) == 1, "Should return 1 user (admin)"
        assert response_data["total_pages"] == 1, "Should have 1 total page"
        assert response_data["current_page"] == 1, "Current page should be 1"
        # Verify it's the admin user
        admin_user = response_data["items"][0]
        assert admin_user["email"] == "admin@test.com", "Should be the admin user"

    def test_get_user(self) -> None:
        """
        Test get user by ID.

        This test will create a user and then retrieve it by ID.
        """

        # Create user
        response = self.client.post("/users/create", json=self.user.model_dump())
        assert response.status_code == 201, "User creation failed"
        created_user = response.json()
        user_id = created_user["id"]

        # Get user by ID
        response = self.client.get(f"/users/{user_id}")

        assert response.status_code == 200, "Response status code is not 200"
        response_data = response.json()
        assert response_data["id"] == user_id, f"Response ID is not {user_id}"
        assert response_data["first_name"] == self.user.first_name, (
            "First name mismatch"
        )
        assert response_data["last_name"] == self.user.last_name, "Last name mismatch"
        assert response_data["username"] == self.user.username, "Username mismatch"
        assert response_data["email"] == self.user.email, "Email mismatch"

    def test_get_user_not_found(self) -> None:
        """
        Test get user when the user does not exist.
        """
        response = self.client.get("/users/999")  # Non-existent ID
        assert response.status_code == 404, "Response status code is not 404"

    def test_update_user(self) -> None:
        """
        Test update user.

        This test will create a user, update it, and verify the changes.
        """

        # Create user
        response = self.client.post("/users/create", json=self.user.model_dump())
        assert response.status_code == 201, "User creation failed"
        created_user = response.json()
        user_id = created_user["id"]

        # Update user
        update_data = UserUpdateDataSchema(  # type: ignore[call-arg]
            first_name="Jane",
            last_name="Smith",
            username="janesmith",
        )

        response = self.client.patch(f"/users/{user_id}", json=update_data.model_dump())

        assert response.status_code == 200, "Response status code is not 200"
        response_data = response.json()
        assert response_data["first_name"] == "Jane", "First name not updated"
        assert response_data["last_name"] == "Smith", "Last name not updated"
        assert response_data["username"] == "janesmith", "Username not updated"
        assert response_data["email"] == self.user.email, (
            "Email should remain unchanged"
        )

    def test_update_user_password(self) -> None:
        """
        Test update user password.

        This test will create a user and update their password.
        """

        # Create user
        response = self.client.post("/users/create", json=self.user.model_dump())
        assert response.status_code == 201, "User creation failed"
        created_user = response.json()
        user_id = created_user["id"]

        # Update password
        update_data = UserUpdateDataSchema(  # type: ignore[call-arg]
            password="NewPassword123!",  # noqa: S106
        )

        response = self.client.patch(f"/users/{user_id}", json=update_data.model_dump())

        assert response.status_code == 200, "Response status code is not 200"
        # Password should not be returned in response
        response_data = response.json()
        assert "password" not in response_data, "Password should not be in response"

    def test_update_user_not_found(self) -> None:
        """
        Test update user when the user does not exist.
        """
        update_data = UserUpdateDataSchema(  # type: ignore[call-arg]
            first_name="Jane",
        )
        response = self.client.patch("/users/999", json=update_data.model_dump())
        assert response.status_code == 404, "Response status code is not 404"

    def test_delete_user(self) -> None:
        """
        Test delete user.

        This test will create a user, delete it, and verify it's no longer accessible.
        """

        # Create user
        response = self.client.post("/users/create", json=self.user.model_dump())
        assert response.status_code == 201, "User creation failed"
        created_user = response.json()
        user_id = created_user["id"]

        # Delete user
        response = self.client.delete(f"/users/{user_id}")
        assert response.status_code == 204, "Response status code is not 204"

        # Try to get deleted user
        response = self.client.get(f"/users/{user_id}")
        assert response.status_code == 404, "Deleted user should not be found"

    def test_delete_user_not_found(self) -> None:
        """
        Test delete user when the user does not exist.
        """
        response = self.client.delete("/users/999")  # Non-existent ID
        assert response.status_code == 404, "Response status code is not 404"

    def test_user_model_fields(self) -> None:
        """
        Test user model has all required fields.

        This test verifies that the user model contains all expected fields.
        """

        # Create user
        response = self.client.post("/users/create", json=self.user.model_dump())
        assert response.status_code == 201, "User creation failed"

        response_data = response.json()

        # Check all expected fields are present
        expected_fields = [
            "id",
            "first_name",
            "last_name",
            "username",
            "email",
            "is_active",
            "is_superuser",
            "created_at",
            "updated_at",
            "deleted_at",
        ]

        for field in expected_fields:
            assert field in response_data, f"Field {field} is missing from response"

        # Check field types and constraints
        assert isinstance(response_data["id"], int), "ID should be integer"
        assert isinstance(response_data["is_active"], bool), (
            "is_active should be boolean"
        )
        assert isinstance(response_data["is_superuser"], bool), (
            "is_superuser should be boolean"
        )
        assert response_data["deleted_at"] is None, (
            "deleted_at should be None for active user"
        )


if __name__ == "__main__":
    unittest.main()
