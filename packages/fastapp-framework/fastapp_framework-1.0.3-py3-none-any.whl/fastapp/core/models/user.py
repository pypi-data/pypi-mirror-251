"""Fastapp User Models
Pydantic models for user returning, creation, etc.

Author: Collin Meyer
Created: 2024-01-13 15:09
"""

from pydantic import BaseModel


# pylint: disable=too-few-public-methods
# pylint: disable=missing-class-docstring
class User(BaseModel):
    name: str
    email: str
    is_active: bool
    is_admin: bool

    class Config:
        from_attributes = True


class CreateUser(BaseModel):
    name: str
    email: str
    password: str
    is_admin: bool = False
    is_active: bool = True

    class Config:
        from_attributes = True


class DeleteUser(BaseModel):
    uid: int | None = None
    name: str | None = None
    email: str | None = None

    class Config:
        from_attributes = True
