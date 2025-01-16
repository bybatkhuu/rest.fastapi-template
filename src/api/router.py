# -*- coding: utf-8 -*-

from pydantic import validate_call
from fastapi import FastAPI, APIRouter

from api.config import config
from api.core.routers.utils import router as utils_router
from api.core.routers.default import router as default_router


@validate_call(config={"arbitrary_types_allowed": True})
def add_routers(app: FastAPI) -> None:
    """Add routers to FastAPI app.

    Args:
        app (FastAPI): FastAPI app instance.
    """

    _api_router = APIRouter(prefix=config.api.prefix)
    _api_router.include_router(utils_router)
    ## Add more API routers here...

    ## Add admin API routers here...

    app.include_router(_api_router)
    app.include_router(default_router)

    return


__all__ = ["add_routers"]
