"""Fastapp Settings
Settings for the different environments of the application.

Author: Collin Meyer
Created: 2024-01-10 22:37
"""
from pathlib import Path
from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict

APP_DESC = """
Fastapp is a boilerplate for fastapi projects. 🚀

## Users

- List users
- Authenticate users
- Add users
- Remove users
- Update users

"""


# pylint: disable=too-few-public-methods
class Settings(BaseSettings):
    """Development settings"""

    title: str = "Fastapp"
    description: str = APP_DESC
    version: str = "0.0.0"

    server_name: str = "http://localhost"

    log_level: str = "DEBUG"
    log_file: Path = Path("fastapp.log")

    cors_origins: list[str] = ["*"]

    api_prefix: str = "/api/v1"
    openapi_url: str = "/api/v1/openapi.json"
    docs_url: str = "/api/v1/docs"

    secret_key: str
    jwt_encode_algorithm: str = "HS256"
    access_token_expire: int = 30

    database_uri: str = "sqlite:///./fastapp.db"

    admin_username: str = "admin"
    admin_email: str = ""
    admin_password: str = "admin"

    mail_username: str
    mail_password: str
    mail_from: str
    mail_from_name: str
    mail_port: int = 587
    mail_server: str

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")


@lru_cache()
def get_settings() -> Settings:
    """Get settings"""

    return Settings()
