# -*- coding: utf-8 -*-

from typing import AsyncGenerator

from contextlib import asynccontextmanager

from fastapi import FastAPI

from .config import config
from .helpers.crypto import rsa as rsa_helper
from .logger import logger


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    """Lifespan context manager for FastAPI application.
    Startup and shutdown events are logged.

    Args:
        app (FastAPI, required): FastAPI application instance.
    """

    logger.info("Preparing to startup...")
    await rsa_helper.async_create_keys(
        rsa_keys_dir=config.api.paths.rsa_keys_dir,
        key_size=config.api.security.rsa.key_size,
        private_key_fname=config.api.security.rsa.private_key_fname,
        public_key_fname=config.api.security.rsa.public_key_fname,
    )
    # Add startup code here...
    logger.success("Finished preparation to startup.")
    logger.opt(colors=True).info(f"App version: <c>{config.version}</c>")
    logger.opt(colors=True).info(f"API version: <c>{config.api.version}</c>")
    logger.opt(colors=True).info(f"API prefix: <c>{config.api.prefix}</c>")
    logger.opt(colors=True).info(
        f"Listening on: <c>http://{config.api.bind_host}:{config.api.port}</c>"
    )

    yield

    logger.info("Praparing to shutdown...")
    # Add shutdown code here...
    logger.success("Finished preparation to shutdown.")


__all__ = ["lifespan"]
