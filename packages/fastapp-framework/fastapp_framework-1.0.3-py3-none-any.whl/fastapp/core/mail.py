"""Fastapp Mail Configuration
Settings for the different environments of the application.

Author: Collin Meyer
Created: 2024-01-10 22:37
"""
import os
from fastapi_mail import FastMail, MessageSchema, ConnectionConfig, MessageType

from fastapp.core.settings import get_settings

settings = get_settings()

mail_conf = ConnectionConfig(
    MAIL_USERNAME=settings.mail_username,
    MAIL_PASSWORD=settings.mail_password,
    MAIL_FROM=settings.mail_from,
    MAIL_FROM_NAME=settings.mail_from_name,
    MAIL_PORT=settings.mail_port,
    MAIL_SERVER=settings.mail_server,
    MAIL_STARTTLS=True,
    MAIL_SSL_TLS=False,
    USE_CREDENTIALS=True,
    VALIDATE_CERTS=True,
    TEMPLATE_FOLDER=os.path.join(os.path.dirname(__file__), "./templates"),
)

fastmail = FastMail(mail_conf)


async def send_email_async(
    subject: str, email_to: list[str], body: dict, template_name: str
):
    """Asyncronously send an email

    Args:
        subject (str): Subject of the email
        email_to (list[str]): List of email addresses to send to
        body (dict): Body of the email

    Returns:
        None
    """
    message = MessageSchema(
        subject=subject,
        recipients=email_to,
        template_body=body,
        subtype=MessageType.html,
    )

    await fastmail.send_message(message, template_name=template_name)


async def send_reset_email(email_to: str, name: str, token: str):
    """Send a reset email to a user

    Args:
        email_to (str): Email address to send to
        token (str): Reset token to send

    Returns:
        None
    """

    url = f"{settings.server_name}/reset-password?token={token}"
    subject = "[Fastapp] Password Recovery"
    body = {"name": name, "url": url}

    await send_email_async(subject, [email_to], body, "reset_password.html")
