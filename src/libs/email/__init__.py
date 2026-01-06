"""
Email Manager - Index.

This package handles email behaviors.
"""

from collections.abc import Mapping
from datetime import UTC, datetime
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from pathlib import Path
from smtplib import SMTP_SSL
from typing import Any

from jinja2 import (
    Environment,
    FileSystemLoader,
    StrictUndefined,
    TemplateNotFound,
    select_autoescape,
)

from src.libs.log import get_context as _
from src.libs.log import get_logger
from src.settings import Settings

log = get_logger()


class EmailTemplateRenderer:
    """
    # Template Renderer.

    ---

    Render HTML emails using Jinja2 templates.
    """

    def __init__(
        self,
        template_dir: Path | str | None = None,
    ) -> None:
        """
        # Initialize Template Renderer.

        ---

        Args:
            template_dir (Path | str | None):
                Directory where email templates are stored.

        ---

        Example:
        ```
            renderer = EmailTemplateRenderer()  # Uses default template directory
            # or
            renderer = EmailTemplateRenderer(template_dir="path/to/templates")
            # or
            renderer = EmailTemplateRenderer(template_dir=Path("path/to/templates"))
        ```

        """

        base_dir = (
            Path(template_dir)
            if template_dir
            else Path(__file__).resolve().parent / "templates"
        )

        self.env = Environment(
            loader=FileSystemLoader(base_dir),
            autoescape=select_autoescape(["html", "xml"]),
            undefined=StrictUndefined,
        )

        self.base_context: dict[str, Any] = {
            "app_name": Settings.APP_NAME,
            "app_url": Settings.APP_URL.rstrip("/"),
        }

    def render(
        self,
        template_name: str,
        context: Mapping[str, Any] | None = None,
    ) -> str:
        """
        # Renderer.

        ---

        Render a template with default and custom context.

        Args:
            template_name (str): Name of the template file to render.
            context (Mapping[str, Any] | None):
                Additional context to pass to the template.

        Returns:
            str: Rendered template as a string.

        ---

        Example:
        ```
            renderer = EmailTemplateRenderer()
            rendered_html = renderer.render(
                "welcome.html",
                {"user_name": "John Doe"},
            )
            # <p>Hello, John Doe!</p>
        ```

        """

        context_data: dict[str, Any] = {
            **self.base_context,
            "current_year": datetime.now(tz=UTC).year,
        }

        if context:
            context_data.update(context)

        try:
            template = self.env.get_template(template_name)
        except TemplateNotFound:
            log.exception(f"{_()}: Email template '{template_name}' not found.")
            raise

        try:
            return template.render(**context_data)
        except Exception:
            log.exception(
                f"{_()}: Unable to render email template '{template_name}'.",
            )
            raise


class EmailController:
    """
    # Email Controller.

    ---

    This class is responsible to handle everything about email.
    """

    def __init__(
        self,
        email_address: str = Settings.EMAIL_USER,
        password: str = Settings.EMAIL_PASS,
        template_dir: Path | str | None = None,
    ) -> None:
        """
        # Initialize Email Controller.

        ---

        Args:
            email_address (str): Email address used to send emails.
            password (str): Password for the email account.
            template_dir (Path | str | None):
                Directory where email templates are stored.

        ---

        Example:
        ```
            # Uses default email and template directory
            email_controller = EmailController()
            # or
            email_controller = EmailController(
                email_address="user@example.com",
                password="securepassword",
                template_dir="path/to/templates",
            )
        ```

        """

        self.email_address = email_address
        self.password = password

        self.smtp_host = Settings.SMTP_HOST
        self.smtp_port = Settings.SMTP_PORT
        self.imap_host = Settings.IMAP_HOST
        self.imap_port = Settings.IMAP_PORT

        self.renderer = EmailTemplateRenderer(template_dir=template_dir)

    def send_email(
        self,
        to_email: str,
        subject: str,
        body: str,
    ) -> None:
        """
        # Send email to user.

        This method sends an email to the specified recipient. Normally, this method is
        used internally by other methods.

        ---

        Args:
            to_email (str): Recipient email address.
            subject (str): Subject of the email.
            body (str): HTML body of the email.

        ---

        Example:
        ```
            email_controller = EmailController()
            email_controller.send_email(
                to_email="user@example.com",
                subject="Welcome!",
                body="<p>Hello, welcome to our service!</p>",
            )
        ```

        """

        log.debug(f"{_()}: Constructing email to {to_email}.")

        msg = MIMEMultipart("alternative")
        msg["From"] = self.email_address
        msg["To"] = to_email
        msg["Subject"] = subject
        msg.attach(MIMEText(body, "html"))

        try:
            with SMTP_SSL(self.smtp_host, self.smtp_port) as server:
                server.login(self.email_address, self.password)
                server.sendmail(self.email_address, to_email, msg.as_string())
        except Exception:
            log.exception(f"{_()}: Unable to send email to {to_email}.")
            raise

        log.debug(f"{_()}: Email sent to {to_email}.")

    def send_email_confirmation(
        self,
        to_email: str,
        token: str,
    ) -> None:
        """
        # Send an email confirmation to user.

        This method sends an email confirmation to the specified recipient.

        ---

        Args:
            to_email (str): Recipient email address.
            token (str): Email confirmation token.

        ---

        Example:
        ```
            email_controller = EmailController()
            email_controller.send_email_confirmation(
                to_email="user@example.com",
                token="exampletoken",
            )
        ```

        """

        log.debug(f"{_()}: Sending email confirmation to {to_email}.")

        body = self.renderer.render(
            "verification.html",
            {
                "token": token,
                "subject": "Email confirmation",
            },
        )

        self.send_email(
            to_email=to_email,
            subject="Email confirmation",
            body=body,
        )

    def send_email_password_reset(
        self,
        to_email: str,
        token: str,
    ) -> None:
        """
        # Send a password reset email to user.

        This method sends a password reset email to the specified recipient.

        ---

        Args:
            to_email (str): Recipient email address.
            token (str): Password reset token.

        ---

        Example:
        ```
            email_controller = EmailController()
            email_controller.send_email_password_reset(
                to_email="user@example.com",
                token="exampletoken",
            )
        ```

        """

        log.debug(f"{_()}: Sending email of password reset to {to_email}.")

        body = self.renderer.render(
            "password_reset.html",
            {
                "token": token,
                "subject": "Password Reset",
            },
        )

        self.send_email(
            to_email=to_email,
            subject="Password Reset",
            body=body,
        )
