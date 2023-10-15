# -*- coding: utf-8 -*-

from fastapi import Request
from fastapi.exceptions import RequestValidationError

from src.core.constants.error_code import ErrorCodeEnum
from src.core.responses.base import BaseResponse


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


__all__ = ["validation_error_handler"]
