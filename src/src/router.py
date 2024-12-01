# -*- coding: utf-8 -*-

from pydantic import validate_arguments
from fastapi import FastAPI, APIRouter

from src.config import config
from src.core.routers.utils import router as utils_router
from src.core.routers.default import router as default_router
from src.core.routers.error_test import router as error_test_router


@validate_arguments(config=dict(arbitrary_types_allowed=True))
def add_routers(app: FastAPI):
    """Add routers to FastAPI app.

    Args:
        app (FastAPI): FastAPI app instance.
    """

    _api_router = APIRouter(prefix=config.api.prefix)
    _api_router.include_router(utils_router)
    # Add more API routers here...

    app.include_router(_api_router)
    app.include_router(default_router)
    app.include_router(error_test_router)


__all__ = ["add_routers"]
