# -*- coding: utf-8 -*-

from enum import Enum
from http import HTTPStatus
from typing import Union

from src.core.schemas.error_code import ErrorCodePM


class ErrorCodeEnum(Enum):
    BAD_REQUEST = ErrorCodePM(
        code="400_00000",
        name="BAD_REQUEST",
        status_code=400,
        message=f"{HTTPStatus(400).phrase}!",
        description=f"{HTTPStatus(400).description}.",
        detail=None,
    )
    NOT_FOUND = ErrorCodePM(
        code="404_00000",
        name="NOT_FOUND",
        status_code=404,
        message=f"{HTTPStatus(404).phrase}!",
        description=f"{HTTPStatus(404).description}.",
        detail=None,
    )
    METHOD_NOT_ALLOWED = ErrorCodePM(
        code="405_00000",
        name="METHOD_NOT_ALLOWED",
        status_code=405,
        message=f"{HTTPStatus(405).phrase}!",
        description=f"{HTTPStatus(405).description}.",
        detail=None,
    )
    UNPROCESSABLE_ENTITY = ErrorCodePM(
        code="422_00000",
        name="UNPROCESSABLE_ENTITY",
        status_code=422,
        message=f"{HTTPStatus(422).phrase}!",
        description=None,
        detail=None,
    )
    INTERNAL_SERVER_ERROR = ErrorCodePM(
        code="500_00000",
        name="INTERNAL_SERVER_ERROR",
        status_code=500,
        message=f"{HTTPStatus(500).phrase}!",
        description=f"{HTTPStatus(500).description}.",
        detail=None,
    )

    @classmethod
    def get_by_code(cls, code: str) -> Union["ErrorCodeEnum", None]:
        for _error_code_enum in ErrorCodeEnum:
            if _error_code_enum.value.code == code:
                return _error_code_enum
        return None

    @classmethod
    def get_by_name(cls, name: str) -> Union["ErrorCodeEnum", None]:
        for _error_code_enum in ErrorCodeEnum:
            if _error_code_enum.value.name == name:
                return _error_code_enum
        return None

    @classmethod
    def get_by_status_code(cls, status_code: int) -> Union["ErrorCodeEnum", None]:
        for _error_code_enum in ErrorCodeEnum:
            if _error_code_enum.value.status_code == status_code:
                return _error_code_enum
        return None


__all__ = ["ErrorCodeEnum"]
