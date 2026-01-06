"""
SQLAdmin - Authentication Backend.

This module is responsible to handle authentication for the SQLAdmin interface.
"""

import base64

from sqladmin.authentication import AuthenticationBackend
from starlette.requests import Request

from src.apps.auth.services import generate_token, revoke_token
from src.apps.users.models import UsersModel
from src.libs.log import get_context as _
from src.libs.log import get_logger
from src.settings import Settings

log = get_logger()


class AdminAuth(AuthenticationBackend):
    """
    SQLAdmin Authentication Backend.
    """

    def handle_cookie_ingestion(self, request: Request) -> None:
        """
        Handle cookie ingestion for authentication.
        """

        cookies = request.cookies

        if "tokens" in cookies:
            log.debug(f"{_()}: Tokens found in cookies.")

            access_token = cookies["tokens"].split("%2C")[0]
            request.session.update({"token": access_token})

            log.debug(f"{_()}: Access token ingested into session.")

    async def login(self, request: Request) -> bool:
        """
        Handle the login process.
        """

        log.info(f"{_()}: Admin login attempt.")
        log.debug(f"{_()}: Determining type of authentication.")

        self.handle_cookie_ingestion(request)

        log.debug(f"{_()}: Processing login form.")

        form = await request.form()
        username, password = form["username"], form["password"]

        user_model = (
            UsersModel.query()
            .filter(
                (UsersModel.username == username) | (UsersModel.email == username),
            )
            .first()
        )

        if not user_model or user_model.role.slug != "admin":
            return False

        credentials = f"{username}:{password}"
        basic_token = base64.b64encode(credentials.encode("utf-8")).decode("utf-8")

        tokens = await generate_token(f"Basic {basic_token}")

        request.session.update({"token": tokens.access_token})

        return True

    async def logout(self, request: Request) -> bool:
        """
        Handle the logout process.
        """

        token = request.session.get("token")
        request.session.clear()

        if token:
            revoke_token(f"Bearer {token}")

        return True

    async def authenticate(self, request: Request) -> bool:
        """
        Validate the user.
        """

        log.info(f"{_()}: Verifying authentication.")

        self.handle_cookie_ingestion(request)

        log.debug(f"{_()}: Checking for token in session.")

        token = request.session.get("token")

        if not token:
            log.warning(f"{_()}: No token found in session.")
            return False

        log.debug(f"{_()}: Token found, authentication successful.")

        return True


auth_backend = AdminAuth(secret_key=Settings.SECRET_KEY)
