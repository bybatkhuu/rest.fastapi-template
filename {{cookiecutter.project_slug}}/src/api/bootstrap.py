# -*- coding: utf-8 -*-

## Third-party libraries
from fastapi import FastAPI

## Internal modules
from api.config import config
from api.lifespan import lifespan, pre_init
from api.middleware import add_middlewares
from api.router import add_routers
from api.mount import add_mounts
from api.exception import add_exception_handlers
from api.core.responses import BaseResponse


def create_app() -> FastAPI:
    """Create FastAPI application instance.

    Returns:
        FastAPI: FastAPI application instance.
    """

    pre_init()

    app = FastAPI(
        title=config.api.name,
        version=config.version,
        lifespan=lifespan,
        default_response_class=BaseResponse,
        **config.api.docs.model_dump(exclude={"enabled"}),
    )

    add_middlewares(app=app)
    add_routers(app=app)
    add_mounts(app=app)
    add_exception_handlers(app=app)

    return app


__all__ = ["create_app"]
