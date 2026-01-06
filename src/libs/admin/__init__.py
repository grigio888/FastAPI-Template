"""
SQLAdmin.

This module is responsible to create a self feeded admin interface for
SQLAlchemy models.
"""

from sqladmin import Admin as SQLAdmin

from src.libs.utilities.path import load_all_objects_from


class Admin(SQLAdmin):
    """
    SQLAdmin wrapper.

    This wrapper is responsible for loading all admin views.
    """

    def __init__(self, *args: list, **kwargs: dict) -> None:
        """
        Initialize the Admin class.
        """

        super().__init__(*args, **kwargs)

        objects = load_all_objects_from("admin", "Admin", as_list=True)

        if not objects:
            return

        for obj in objects:
            self.add_view(obj)
