# -*- coding: utf-8 -*-

from fastapi import APIRouter, Request

from app.config import config
from app.core.schemas import BaseResPM
from app.core.responses import BaseResponse


router = APIRouter(tags=config.api.routes.utils.tags)


@router.get(
    "/",
    summary="Base",
    description="Base path for all API endpoints.",
    response_model=BaseResPM,
)
async def get_base(request: Request):
    return BaseResponse(request=request, message="Welcome to the REST API service!")


@router.get(
    config.api.routes.utils.ping,
    summary="Ping",
    description="Check if the service is up and running.",
    response_model=BaseResPM,
)
async def get_ping(request: Request):
    return BaseResponse(
        request=request, message="Pong!", headers={"Cache-Control": "no-cache"}
    )


@router.get(
    config.api.routes.utils.health,
    summary="Health",
    description="Check health of all related backend services.",
    response_model=BaseResPM,
)
async def get_health(request: Request):
    _message = "Everything is OK."
    _data = {"api": {"message": "API is up.", "is_alive": True}}

    return BaseResponse(
        request=request,
        content=_data,
        message=_message,
        headers={
            "Cache-Control": "no-cache, no-store, must-revalidate",
            "Pragma": "no-cache",
            "Expires": "0",
        },
    )


__all__ = ["router"]
