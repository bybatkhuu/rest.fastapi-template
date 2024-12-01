# -*- coding: utf-8 -*-

from contextlib import asynccontextmanager

from fastapi import FastAPI

from src.config import config
from src.logger import logger
from __version__ import __version__


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifespan context manager for FastAPI application.
    Startup and shutdown events are logged.

    Args:
        app (FastAPI): FastAPI application instance.
    """

    logger.info("Preparing to startup...")
    # Add startup code here...
    logger.success("Finished preparation to startup.")
    logger.opt(colors=True).info(f"App version: <c>{__version__}</c>")
    logger.opt(colors=True).info(f"API version: <c>{config.api.version}</c>")

    yield
    logger.info("Praparing to shutdown...")
    # Add shutdown code here...
    logger.success("Finished preparation to shutdown.")


__all__ = ["lifespan"]
