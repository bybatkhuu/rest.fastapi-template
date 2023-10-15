# -*- coding: utf-8 -*-

from fastapi import APIRouter
from fastapi.responses import RedirectResponse

from src.config import config


router = APIRouter(tags=["Default"])


@router.get(
    "/",
    summary="Root",
    description=f"Redirect to base endpoint: '{config.api.prefix}/'",
    status_code=307,
)
async def get_root():
    return RedirectResponse(url=f"{config.api.prefix}/")


if config.app.docs.enabled:

    @router.get(
        "/openapi.json",
        summary="OpenAPI JSON",
        description=f"Redirect to OpenAPI JSON: '{config.app.docs.openapi_url}'",
        status_code=307,
    )
    def get_openapi_json():
        return RedirectResponse(url=f"{config.app.docs.openapi_url}")

    @router.get(
        "/docs",
        summary="Swagger UI docs",
        description=f"Redirect to Swagger UI docs: '{config.app.docs.docs_url}'",
        status_code=307,
    )
    def get_docs():
        return RedirectResponse(url=f"{config.app.docs.docs_url}")

    @router.get(
        "/redoc",
        summary="Redoc",
        description=f"Redirect to Redoc: '{config.app.docs.redoc_url}'",
        status_code=307,
    )
    def get_redoc():
        return RedirectResponse(url=f"{config.app.docs.redoc_url}")


__all__ = ["router"]
