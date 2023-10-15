# -*- coding: utf-8 -*-

from fastapi import HTTPException, Request

from src.core.constants.error_code import ErrorCodeEnum
from src.core.responses.base import BaseResponse


## For 404 status code:
async def not_found_handler(request: Request, exc: HTTPException) -> BaseResponse:
    """404 status code handler.

    Args:
        request (Request      , required): Request object from FastAPI.
        exc     (HTTPException, required): HTTPException object from FastAPI.

    Returns:
        BaseResponse: Response object.
    """

    _error = ErrorCodeEnum.NOT_FOUND.value.dict()
    _message: str = _error.get("message")

    return BaseResponse(
        request=request, status_code=404, message=_message, error=_error
    )


__all__ = ["not_found_handler"]
