# -*- coding: utf-8 -*-

from pydantic import validate_arguments
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware

from beans_logging.fastapi import HttpAccessLogMiddleware

from src.config import config
from src.core.middlewares import ProcessTimeMiddleware, RequestIdMiddleware


@validate_arguments(config=dict(arbitrary_types_allowed=True))
def add_middlewares(app: FastAPI):
    """Add middlewares to FastAPI app.

    Args:
        app (FastAPI): FastAPI app instance.
    """

    # Add more middlewares here...
    app.add_middleware(
        HttpAccessLogMiddleware,
        has_proxy_headers=config.app.behind_proxy,
        has_cf_headers=config.app.behind_cf_proxy,
        debug_format=config.logger.extra.http_std_debug_format,
        msg_format=config.logger.extra.http_std_msg_format,
    )
    app.add_middleware(GZipMiddleware, minimum_size=config.app.gzip_min_size)
    app.add_middleware(CORSMiddleware, **config.app.cors.dict())
    app.add_middleware(TrustedHostMiddleware, allowed_hosts=config.app.allowed_hosts)
    app.add_middleware(RequestIdMiddleware)
    app.add_middleware(ProcessTimeMiddleware)


__all__ = ["add_middlewares"]
