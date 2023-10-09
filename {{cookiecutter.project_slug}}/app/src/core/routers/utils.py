# -*- coding: utf-8 -*-

from fastapi import APIRouter, Request

from src.config import config
from src.core.schemas.responses import BaseResPM
from src.core.responses.base import BaseResponse


router = APIRouter(tags=config.routes["utils"]["_tags"])


@router.get(
    "/",
    summary="Base",
    description="Base path for all REST API endpoints.",
    response_model=BaseResPM,
)
async def get_base(request: Request):
    return BaseResponse(
        request=request, message="Welcome to the {{cookiecutter.project_name}} service."
    )


@router.get(
    config.routes["utils"]["ping"],
    summary="Ping",
    description="Check if the service is up and running.",
    response_model=BaseResPM,
)
async def get_ping(request: Request):
    return BaseResponse(
        request=request, message="Pong!", headers={"Cache-Control": "no-cache"}
    )


@router.get(
    config.routes["utils"]["health"],
    summary="Health",
    description="Check health of all related backend services.",
    response_model=BaseResPM,
)
async def get_health(request: Request):
    _message = "Everything is OK."
    _data = {"DB": None}

    return BaseResponse(
        request=request,
        content=_data,
        message=_message,
        headers={"Cache-Control": "no-cache"},
    )


__all__ = ["router"]
