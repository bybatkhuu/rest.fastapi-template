# -*- coding: utf-8 -*-

from typing import List

from pydantic import Field, constr

from ._base import FrozenBaseConfig


class BaseRoutesConfig(FrozenBaseConfig):
    tags: List[constr(strip_whitespace=True, min_length=2, max_length=64)] = Field(...)  # type: ignore
    prefix: constr(strip_whitespace=True, max_length=256) = Field(...)  # type: ignore


class UtilsRoutesConfig(BaseRoutesConfig):
    ping: constr(strip_whitespace=True) = Field(..., min_length=2, max_length=256)  # type: ignore
    health: constr(strip_whitespace=True) = Field(..., min_length=2, max_length=256)  # type: ignore


class RoutesConfig(FrozenBaseConfig):
    utils: UtilsRoutesConfig = Field(...)


__all__ = ["RoutesConfig"]
