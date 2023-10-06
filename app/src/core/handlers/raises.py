# -*- coding: utf-8 -*-

from typing import Union

from fastapi import HTTPException, Request
from fastapi.exceptions import RequestValidationError

from src.core import utils
from src.core.constants.error_code import ErrorCodeEnum
from src.core.responses.base import BaseResponse


## For HTTPException error:
async def http_exception_handler(request: Request, exc: HTTPException) -> BaseResponse:
    """HTTPException handler.

    Args:
        request (Request      , required): Request object from FastAPI.
        exc     (HTTPException, required): HTTPException object from FastAPI.

    Returns:
        BaseResponse: Response object.
    """

    _message: str
    _error: Union[dict, str, None] = None

    _http_status, _ = utils.get_http_status(status_code=exc.status_code)
    if isinstance(exc.detail, dict):
        _message = str(exc.detail.get("message", _http_status.phrase))

        _error = exc.detail.get("error")
        if _error:
            if isinstance(_error, dict):
                if ("description" not in _error) and _http_status.description:
                    _error["description"] = _http_status.description
            else:
                _error = str(_error)
    else:
        _message = str(exc.detail)

        _error_code_enum = ErrorCodeEnum.get_by_status_code(status_code=exc.status_code)
        if _error_code_enum:
            _error = _error_code_enum.value.dict()

    return BaseResponse(
        request=request,
        status_code=exc.status_code,
        message=_message,
        error=_error,
        headers=exc.headers,
    )


## For RequestValidationError error:
async def validation_error_handler(
    request: Request, exc: RequestValidationError
) -> BaseResponse:
    """RequestValidationError handler for validation error.

    Args:
        request (Request               , required): Request object from FastAPI.
        exc     (RequestValidationError, required): RequestValidationError object from FastAPI.

    Returns:
        BaseResponse: Response object.
    """

    _message = "Validation error!"
    _error = ErrorCodeEnum.UNPROCESSABLE_ENTITY.value.dict()
    _error["description"] = str(exc)
    _error["detail"]: list = exc.errors()

    return BaseResponse(
        request=request, status_code=422, message=_message, error=_error
    )


__all__ = ["http_exception_handler", "validation_error_handler"]
