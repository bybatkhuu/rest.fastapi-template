# -*- coding: utf-8 -*-

from typing import Any, Union, Optional

from pydantic import BaseModel, Field, constr

from src.config import config
from src.core.constants.base import MethodEnum
from .base import ExtraBaseModel
from __version__ import __version__


class LinksResPM(ExtraBaseModel):
    self_link: Optional[constr(strip_whitespace=True, max_length=2047)] = Field(
        default=None,
        alias="self",
        title="Self link",
        description="Link to the current resource.",
        examples=["https://api.{{cookiecutter.domain}}/v1/ping"],
    )


class MetaResPM(ExtraBaseModel):
    request_id: Optional[
        constr(strip_whitespace=True, min_length=32, max_length=36)
    ] = Field(
        default=None,
        title="Request ID",
        description="Current request ID.",
        examples=["211203afa2844d55b1c9d38b9f8a7063"],
    )
    method: Optional[MethodEnum] = Field(
        default=None,
        title="Method",
        description="Current request method.",
        examples=["GET"],
    )
    api_version: constr(strip_whitespace=True) = Field(
        default=config.api.version,
        min_length=1,
        max_length=15,
        title="API version",
        description="Current API version.",
        examples=[config.api.version],
    )
    version: constr(strip_whitespace=True) = Field(
        default=__version__,
        min_length=5,
        max_length=31,
        title="Version",
        description="Current service version.",
        examples=[__version__],
    )


class ErrorResPM(BaseModel):
    code: constr(strip_whitespace=True) = Field(..., min_length=3, max_length=36)
    description: Optional[constr(strip_whitespace=True)] = Field(
        default=None, max_length=511
    )
    detail: Union[Any, dict, list] = Field(default=None)


class BaseResPM(BaseModel):
    message: str = Field(
        ...,
        min_length=1,
        max_length=255,
        title="Message",
        description="Response message about the current request for the client.",
        examples=["Request processed successfully."],
    )
    data: Union[Any, dict, list] = Field(
        default=None,
        title="Data",
        description="Resource data or any response related data.",
        examples=["Any data: dict, list, str, int, float, null, etc."],
    )
    links: LinksResPM = Field(
        default_factory=LinksResPM,
        title="Links",
        description="Resource related links.",
    )
    meta: MetaResPM = Field(
        default_factory=MetaResPM,
        title="Meta",
        description="Meta information about the current request.",
    )
    error: Union[ErrorResPM, Any] = Field(
        default=None,
        title="Error",
        description="Error information about the current request.",
        examples=[None],
    )


class BadBaseResPM(BaseResPM):
    message: str = Field(
        ...,
        min_length=1,
        max_length=255,
        title="Message",
        description="Response message about the current request for the client.",
        examples=["Bad Request!"],
    )
    data: Union[Any, dict, list] = Field(
        default=None,
        title="Data",
        description="Resource data or any response related data.",
        examples=[None],
    )
    error: Union[ErrorResPM, Any] = Field(
        default=None,
        title="Error",
        description="Error information about the current request.",
        examples=[
            {
                "code": "400_00000",
                "description": "Bad request syntax or unsupported method.",
                "detail": None,
            }
        ],
    )


class MethodNotBaseResPM(BadBaseResPM):
    message: str = Field(
        ...,
        min_length=1,
        max_length=255,
        title="Message",
        description="Response message about the current request for the client.",
        examples=["Method Not Allowed!"],
    )
    error: Union[ErrorResPM, Any] = Field(
        default=None,
        title="Error",
        description="Error information about the current request.",
        examples=[
            {
                "code": "405_00000",
                "description": "Specified method is invalid for this resource.",
                "detail": None,
            }
        ],
    )


class InvalidBaseResPM(BadBaseResPM):
    message: str = Field(
        ...,
        min_length=1,
        max_length=255,
        title="Message",
        description="Response message about the current request for the client.",
        examples=["Validation error!"],
    )
    error: Union[ErrorResPM, Any] = Field(
        default=None,
        title="Error",
        description="Error information about the current request.",
        examples=[
            {
                "code": "422_00000",
                "description": "Error description.",
                "detail": [
                    {
                        "loc": ["body", "field"],
                        "msg": "Error message.",
                        "type": "Error type.",
                        "ctx": {"constraint": "value"},
                    }
                ],
            }
        ],
    )


class ErrorBaseResPM(BadBaseResPM):
    message: str = Field(
        ...,
        min_length=1,
        max_length=255,
        title="Message",
        description="Response message about the current request for the client.",
        examples=["Internal Server Error!"],
    )
    error: Union[ErrorResPM, Any] = Field(
        default=None,
        title="Error",
        description="Error information about the current request.",
        examples=[
            {
                "code": "500_00000",
                "description": "Server got itself in trouble.",
                "detail": None,
            }
        ],
    )


__all__ = [
    "LinksResPM",
    "MetaResPM",
    "ErrorResPM",
    "BaseResPM",
    "BadBaseResPM",
    "MethodNotBaseResPM",
    "InvalidBaseResPM",
    "ErrorBaseResPM",
]
