"""Fastapp Database Schema
Schematics for objects in the database

Author: Collin Meyer
Created: 2024-01-11 22:21
"""
from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


# pylint: disable=too-few-public-methods
class User(Base):
    """User model"""

    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True, unique=True)
    email = Column(String, index=True, unique=True)
    password = Column(String)
    is_active = Column(Boolean, default=True)
    is_admin = Column(Boolean, default=False)
    reset_token = Column(String, nullable=True)
