"""Fastapp DB Functions"""
from fastapp.db.db import get_db
from fastapp.db.schema import User
from fastapp.core.settings import get_settings
from fastapp.core.logging import get_logger
from fastapp.auth.users import create_user
from fastapp.core.models import user as user_models

settings = get_settings()
logger = get_logger(__name__)


def init():
    """Initialize the database"""
    db = next(get_db())

    user = (
        db.query(User)
        .filter(
            User.name == settings.admin_username, User.email == settings.admin_email
        )
        .first()
    )

    if not user:
        create_user(
            db,
            user_models.CreateUser(
                name=settings.admin_username,
                email=settings.admin_email,
                password=settings.admin_password,
                is_admin=True,
                is_active=True,
            ),
        )

        logger.info("Admin user not found, created one")
        logger.debug(
            "Admin username: %s, email: %s",
            settings.admin_username,
            settings.admin_email,
        )

    logger.info("Database initialized")
