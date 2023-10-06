# -*- coding: utf-8 -*-

from fastapi import HTTPException, Request

from src.logger import log_http_error
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


## For unhandled Exception or 500 internal server error:
async def server_error_handler(request: Request, exc: Exception) -> BaseResponse:
    """Error handler for any kind of unhandled Exception or 500 internal server error.

    Args:
        request (Request  , required): Request object from FastAPI.
        exc     (Exception, required): Any kind of Exception object.

    Returns:
        BaseResponse: Response object.
    """

    _status_code = 500
    _error = ErrorCodeEnum.INTERNAL_SERVER_ERROR.value.dict()
    _error["detail"] = str(exc)
    _message: str = _error.get("message")

    await log_http_error(request=request, status_code=_status_code)
    return BaseResponse(
        request=request, status_code=_status_code, message=_message, error=_error
    )


__all__ = ["not_found_handler", "method_not_allowed_handler", "server_error_handler"]
