"""Fastapp Auth Models
Pydantic models for authentication and authorization

Author: Collin Meyer
Created: 2024-01-13 15:09
"""
from enum import Enum
from pydantic import BaseModel


class Grant(Enum):
    """OAuth Grant Types"""

    ADMIN = "admin"
    USER = "user"


# pylint: disable=too-few-public-methods
class Token(BaseModel):
    """OAuth2 Token Pydantic Model"""

    access_token: str
    token_type: str
    grants: list[Grant]


class PasswordReset(BaseModel):
    """Password Reset Pydantic Model"""

    token: str
    password: str
