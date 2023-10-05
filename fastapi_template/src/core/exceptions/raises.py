# -*- coding: utf-8 -*-

from typing import Any, Optional, Dict

from pydantic import conint, constr, validate_arguments
from fastapi import HTTPException

from src.core.constants.error_code import ErrorCodeEnum


@validate_arguments
def raise_http_exception(
    error_enum: ErrorCodeEnum,
    status_code: Optional[conint(ge=100, le=599)] = None,
    message: Optional[
        constr(strip_whitespace=True, min_length=1, max_length=255)
    ] = None,
    description: Optional[constr(strip_whitespace=True, max_length=511)] = None,
    detail: Any = None,
    headers: Optional[Dict[str, str]] = None,
):
    """Raise custom HTTPException with error code.

    Args:
        error_enum  (ErrorCodeEnum           , required): Main error code enum.
        status_code (Optional[int]           , optional): HTTP status code: [ge=100, le=599]. Defaults to None.
        message     (Optional[str]           , optional): Error message: [min_length=1, max_length=255]. Defaults to None.
        description (Optional[str]           , optional): Error description: [max_length=511]. Defaults to None.
        detail      (Any                     , optional): Error detail. Defaults to None.
        headers     (Optional[Dict[str, str]], optional): Headers. Defaults to None.

    Raises:
        HTTPException: Raise HTTPException with custom error information.
    """

    _error = error_enum.value.dict()

    if not status_code:
        status_code: int = _error.get("status_code")

    if not message:
        message: str = _error.get("message")

    if description:
        _error["description"] = description

    if detail:
        _error["detail"] = detail

    raise HTTPException(
        status_code=status_code,
        detail={"message": message, "error": _error},
        headers=headers,
    )


__all__ = ["raise_http_exception"]
