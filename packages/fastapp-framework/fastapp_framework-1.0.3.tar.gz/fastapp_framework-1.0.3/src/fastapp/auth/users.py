"""Fastapp Auth Users Utilities

Author: Collin Meyer
Created: 2024-01-11 22:21
"""
from typing import Annotated
from jose import JWTError, jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from fastapp.db.schema import User
from fastapp.db.db import get_db
from fastapp.core.models import user as user_models
from fastapp.core.settings import get_settings
from fastapp.auth.password import get_password_hash

settings = get_settings()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl=settings.api_prefix + "/auth/token")


def get_user(db: Session, uid: int = None, name: str = None, email: str = None):
    """Get a user from the database

    One of uid, name, or email must be specified

    Args:
        db (SessionLocal): The database connection
        uid (int, optional): The user's id. Defaults to None.
        name (str, optional): The user's name. Defaults to None.
        email (str, optional): The user's email. Defaults to None.

    Returns:
        User: The user object
    """
    filters = {}
    if uid is not None:
        filters["id"] = uid
    if name is not None:
        filters["name"] = name
    if email is not None:
        filters["email"] = email

    if len(filters) == 0:
        raise ValueError("One of uid, name, or email must be specified")

    return db.query(User).filter_by(**filters).first()


async def get_current_user(
    db: Annotated[Session, Depends(get_db)],
    token: Annotated[str, Depends(oauth2_scheme)],
):
    """Get the current user from db based on OAuth2 token

    Args:
        db (SessionLocal): The database connection
        token (str): The OAuth2 token

    Raises:
        HTTPException: The token is invalid

    Returns:
        User: The current user
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(
            token, settings.secret_key, algorithms=[settings.jwt_encode_algorithm]
        )
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception

    except JWTError as exc:
        raise credentials_exception from exc

    user = get_user(db, name=username)
    if user is None:
        raise credentials_exception

    user_models.User(**user.__dict__)

    return user


async def get_current_active_user(
    current_user: Annotated[User, Depends(get_current_user)]
):
    """Get the current user and validate they are active

    Args:
        current_user (User): The current user

    Raises:
        HTTPException: The user is not active

    Returns:
        User (User): The validated active user
    """
    if not current_user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")

    return current_user


async def get_current_admin_user(
    current_user: Annotated[User, Depends(get_current_user)]
):
    """Get the current user and validate they are an admin

    Args:
        current_user (User): The current user

    Raises:
        HTTPException: The user is not an admin

    Returns:
        User (User): The validated admin user
    """
    if not current_user.is_admin or not current_user.is_active:
        raise HTTPException(
            status_code=400, detail="User cannot access requested resource"
        )

    return current_user


async def get_all_users(
    db: Session, skip: int, limit: int, is_admin: bool | None
) -> list[user_models.User]:
    """Get all users from the database

    Args:
        db (Session): The database connection

    Returns:
        List[models.user.User]: The list of users
    """
    if is_admin is None:
        users = db.query(User).offset(skip).limit(limit).all()
    else:
        users = (
            db.query(User)
            .filter(User.is_admin == is_admin)
            .offset(skip)
            .limit(limit)
            .all()
        )

    return [user_models.User(**user.__dict__) for user in users]


def create_user(
    db: Session,
    user: user_models.CreateUser,
) -> user_models.User:
    """Create a user in the database

    Args:
        db (Session): The database connection
        user (models.user.CreateUser): The user to create

    Returns:
        models.user.User: The created user
    """
    try:
        db_user = User(
            name=user.name,
            email=user.email,
            password=get_password_hash(user.password),
            is_admin=user.is_admin,
            is_active=user.is_active,
        )
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
    except IntegrityError:
        return None

    return user_models.User(**db_user.__dict__)


def delete_user(db: Session, user_id: user_models.DeleteUser) -> user_models.User:
    """Delete a user from the database

    Args:
        db (Session): The database connection
        user_id (models.user.DeleteUser): identification of the user to delete

    Returns:
        models.user.User: The deleted user
    """

    user = get_user(db, **user_id.__dict__)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")

    db.delete(user)
    db.commit()

    return user_models.User(**user.__dict__)
