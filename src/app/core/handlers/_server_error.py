# -*- coding: utf-8 -*-

from fastapi import Request

from beans_logging_fastapi import async_log_http_error

from app.core.constants import ErrorCodeEnum
from app.config import config
from app.core.exceptions import PrimaryKeyError, UniqueKeyError
from app.core.responses import BaseResponse
from app.logger import logger


## For unhandled Exception or 500 internal server error:
async def server_error_handler(request: Request, exc: Exception) -> BaseResponse:
    """Error handler for any kind of unhandled Exception or 500 internal server error.

    Args:
        request (Request  , required): Request object from FastAPI.
        exc     (Exception, required): Any kind of Exception object.

    Returns:
        BaseResponse: Response object.
    """

    _error_enum = ErrorCodeEnum.INTERNAL_SERVER_ERROR
    if isinstance(exc, PrimaryKeyError):
        _error_enum = ErrorCodeEnum.DB_PK_ERROR
    if isinstance(exc, UniqueKeyError):
        _error_enum = ErrorCodeEnum.DB_UQ_ERROR

    _request_id: str = request.state.request_id
    _exc_str = str(exc)
    _status_code = _error_enum.value.status_code
    _error = _error_enum.value.dict()
    _error["detail"] = _exc_str
    _message: str = _error.get("message")

    logger.exception(f"[{_request_id}] {_error_enum.value.code} - {_exc_str}")
    await async_log_http_error(
        request=request,
        status_code=_status_code,
        msg_format=config.logger.extra.http_std_error_format,
    )
    return BaseResponse(
        request=request, status_code=_status_code, message=_message, error=_error
    )


__all__ = ["server_error_handler"]
