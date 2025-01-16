# -*- coding: utf-8 -*-

## Standard libraries
import os
from typing import Union

## Third-party libraries
import uvicorn
from uvicorn._types import ASGIApplication
from pydantic import validate_call

## Internal modules
from api.config import config


@validate_call(config={"arbitrary_types_allowed": True})
def run(app: Union[ASGIApplication, str] = "main:app") -> None:
    """Run uvicorn server.

    Args:
        app (Union[ASGIApplication, str], optional): ASGI application instance or module path.
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

    return


__all__ = ["run"]
