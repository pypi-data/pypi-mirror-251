"""Fastapp Main
Main application creation logic

Author: Collin Meyer
Created: 2024-01-10 23:11
"""
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from fastapp.routes import router as api_router
from fastapp.core.settings import get_settings
from fastapp.core.logging import get_logger
from fastapp.db import init as db_init
from fastapp.db.db import engine
from fastapp.db.schema import Base

settings = get_settings()
logger = get_logger(__name__)


def get_application() -> FastAPI:
    """FastAPI application factory"""

    application = FastAPI(
        title=settings.title,
        description=settings.description,
        version=settings.version,
        docs_url=settings.docs_url,
        openapi_url=settings.openapi_url,
    )

    # Database Init
    Base.metadata.create_all(bind=engine, checkfirst=True)
    db_init()

    # Middleware Init
    application.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    logger.debug("CORS middleware initialized, hosts: %s", settings.cors_origins)

    # Router Init
    application.include_router(api_router)

    logger.info("Application initialized")

    return application
