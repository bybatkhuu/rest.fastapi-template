# -*- coding: utf-8 -*-

# Standard libraries
import os
from typing import Union

## Third-party libraries
import uvicorn
from pydantic import validate_call
from fastapi import FastAPI

## Internal modules
from .config import config
from .lifespan import lifespan, pre_check
from .middleware import add_middlewares
from .router import add_routers
from .mount import add_mounts
from .exception import add_exception_handlers
from .core.responses import BaseResponse


pre_check()

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


@validate_call
def run_server(app: str = "main:app") -> None:
    """Run uvicorn server.

    Args:
        app (str, optional): Application instance. Defaults to "main:app".
    """

    _ssl_keyfile: Union[str, None] = None
    _ssl_certfile: Union[str, None] = None

    if config.api.security.ssl.enabled:
        _ssl_keyfile = os.path.join(
            config.api.paths.ssl_dir, config.api.security.ssl.key_fname
        )
        _ssl_certfile = os.path.join(
            config.api.paths.ssl_dir, config.api.security.ssl.cert_fname
        )

    uvicorn.run(
        app=app,
        host=config.api.bind_host,
        port=config.api.port,
        access_log=False,
        server_header=False,
        proxy_headers=config.api.behind_proxy,
        forwarded_allow_ips=config.api.security.forwarded_allow_ips,
        ssl_keyfile=_ssl_keyfile,
        ssl_certfile=_ssl_certfile,
        **config.api.dev.model_dump(),
    )


__all__ = ["app", "run_server"]
