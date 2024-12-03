# -*- coding: utf-8 -*-

## Third-party libraries
import uvicorn
from fastapi import FastAPI

## Internal modules
from .__version__ import __version__
from .config import config
from .lifespan import lifespan
from .middleware import add_middlewares
from .router import add_routers
from .exception import add_exception_handlers
from .core.responses import BaseResponse


app = FastAPI(
    title=config.api.name,
    version=__version__,
    lifespan=lifespan,
    default_response_class=BaseResponse,
    **config.api.docs.model_dump(exclude={"enabled"}),
)

add_middlewares(app=app)
add_routers(app=app)
add_exception_handlers(app=app)


def run_server() -> None:
    """Run uvicorn server."""

    uvicorn.run(
        app=app,
        host=config.api.bind_host,
        port=config.api.port,
        access_log=False,
        server_header=False,
        proxy_headers=config.api.behind_proxy,
        forwarded_allow_ips=config.api.security.forwarded_allow_ips,
        **config.api.dev.model_dump(),
    )


__all__ = ["app", "run_server"]
