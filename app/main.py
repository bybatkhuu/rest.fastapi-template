#!/usr/bin/env python
# -*- coding: utf-8 -*-

## Third-party libraries
import uvicorn
from fastapi import FastAPI

## Internal modules
from src.config import config
from src.logger import logger
from src.lifespan import lifespan
from src.middleware import add_middlewares
from src.router import add_routers
from src.exception import add_exception_handlers
from src.core.responses.base import BaseResponse
from __version__ import __version__


app = FastAPI(
    title=config.app.name,
    version=__version__,
    lifespan=lifespan,
    default_response_class=BaseResponse,
    **config.app.docs.dict(exclude={"enabled"}),
)

add_middlewares(app=app)
add_routers(app=app)
add_exception_handlers(app=app)


if __name__ == "__main__":
    logger.info(f"Starting server from 'main.py'...")
    uvicorn.run(
        app="main:app",
        host=config.app.bind_host,
        port=config.app.port,
        access_log=False,
        server_header=False,
        proxy_headers=config.app.behind_proxy,
        forwarded_allow_ips=config.app.forwarded_allow_ips,
        **config.app.dev.dict(),
    )


__all__ = ["app"]
