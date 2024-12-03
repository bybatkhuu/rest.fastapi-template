# -*- coding: utf-8 -*-

from typing import List, Optional

from pydantic import Field, constr

from ._base import FrozenBaseConfig


class CorsConfig(FrozenBaseConfig):
    allow_origins: List[
        constr(strip_whitespace=True, min_length=1, max_length=256)  # type: ignore
    ] = Field(...)
    allow_origin_regex: Optional[
        constr(strip_whitespace=True, min_length=1, max_length=256)  # type: ignore
    ] = Field(default=None)
    allow_headers: List[
        constr(strip_whitespace=True, min_length=1, max_length=128)  # type: ignore
    ] = Field(...)
    allow_methods: List[
        constr(
            strip_whitespace=True,
            pattern=r"^(GET|POST|PUT|PATCH|DELETE|HEAD|OPTIONS|CONNECT|TRACE|\*)$",
        )  # type: ignore
    ] = Field(...)
    allow_credentials: bool = Field(...)
    expose_headers: List[
        constr(strip_whitespace=True, min_length=1, max_length=128)  # type: ignore
    ] = Field(...)
    max_age: int = Field(..., ge=0, le=86_400)


__all__ = ["CorsConfig"]
