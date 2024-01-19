"""Fastapp Database Driver
Schematics for objects in the database

Author: Collin Meyer
Created: 2024-01-11 22:21
"""
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from fastapp.core.settings import get_settings

settings = get_settings()

connect_args = {"check_same_thread": False} if "sqlite" in settings.database_uri else {}
engine = create_engine(settings.database_uri, connect_args=connect_args)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# Dependency
def get_db():
    """Get a database connection"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
