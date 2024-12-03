# -*- coding: utf-8 -*-

from typing import List

from pydantic import Field, constr

from ._base import FrozenBaseConfig
from ._cors import CorsConfig
from ._rsa import RSAConfig
from ._jwt import JWTConfig


class SecurityConfig(FrozenBaseConfig):
    allowed_hosts: List[constr(strip_whitespace=True, min_length=1, max_length=256)] = (  # type: ignore
        Field(...)
    )
    forwarded_allow_ips: List[
        constr(strip_whitespace=True, min_length=1, max_length=256)  # type: ignore
    ] = Field(...)
    cors: CorsConfig = Field(...)
    rsa: RSAConfig = Field(...)
    jwt: JWTConfig = Field(...)


__all__ = ["SecurityConfig"]
