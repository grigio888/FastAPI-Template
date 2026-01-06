"""
SQLAdmin - Configuration Module.
"""

from enum import Enum

from src.libs.admin.authentication import auth_backend
from src.libs.database.session import engine as db_engine
from src.settings import Settings


class AdminConfig(Enum):
    """
    Admin Configuration.

    This class is responsible for providing configuration
    settings for the SQLAdmin interface.
    """

    engine = db_engine
    authentication_backend = auth_backend
    title = Settings.APP_NAME
    logo_url = "/static/favicon.png"
    favicon_url = "/static/favicon.png"  # noqa: PIE796
    templates_dir = "src/libs/admin/templates"

    @classmethod
    def as_dict(cls) -> dict:
        """
        Return the configuration as a dictionary.
        """
        return {item.name: item.value for item in cls}
