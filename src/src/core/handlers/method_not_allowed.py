# -*- coding: utf-8 -*-

from fastapi import HTTPException, Request

from src.core.constants.error_code import ErrorCodeEnum
from src.core.responses.base import BaseResponse


## For 405 status code:
async def method_not_allowed_handler(
    request: Request, exc: HTTPException
) -> BaseResponse:
    """405 status code handler.

    Args:
        request (Request      , required): Request object from FastAPI.
        exc     (HTTPException, required): HTTPException object from FastAPI.

    Returns:
        BaseResponse: Response object.
    """

    _error = ErrorCodeEnum.METHOD_NOT_ALLOWED.value.dict()
    _message: str = _error.get("message")

    return BaseResponse(
        request=request, status_code=405, message=_message, error=_error
    )


__all__ = ["method_not_allowed_handler"]
