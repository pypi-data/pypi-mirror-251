"""Fastapp Routers
Accumulation of all routers for the application

Author: Collin Meyer
Created: 2024-01-10 23:13
"""
from fastapi import APIRouter

from fastapp.core.settings import get_settings
from fastapp.routes.auth import router as auth_router

settings = get_settings()

router = APIRouter(prefix=settings.api_prefix)
router.include_router(auth_router)
