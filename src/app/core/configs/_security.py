# -*- coding: utf-8 -*-

from typing import List, Optional

from pydantic import Field, constr, SecretStr
from pydantic_settings import SettingsConfigDict

from app.core.constants import (
    ENV_PREFIX_API,
    HTTP_METHOD_REGEX,
    RSA_ALGORITHM_REGEX,
    JWT_ALGORITHM_REGEX,
)
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
    allow_methods: List[constr(strip_whitespace=True, pattern=HTTP_METHOD_REGEX)] = (  # type: ignore
        Field(...)
    )
    allow_credentials: bool = Field(...)
    expose_headers: List[
        constr(strip_whitespace=True, min_length=1, max_length=128)  # type: ignore
    ] = Field(...)
    max_age: int = Field(..., ge=0, le=86_400)

    model_config = SettingsConfigDict(env_prefix=f"{ENV_PREFIX_API}SECURITY_CORS_")


class RSAConfig(FrozenBaseConfig):
    algorithm: constr(strip_whitespace=True) = Field(..., pattern=RSA_ALGORITHM_REGEX)  # type: ignore
    key_size: int = Field(..., ge=2048, le=8192)
    private_key_fname: constr(strip_whitespace=True) = Field(  # type: ignore
        ..., min_length=2, max_length=256
    )
    public_key_fname: constr(strip_whitespace=True) = Field(  # type: ignore
        ..., min_length=2, max_length=256
    )

    model_config = SettingsConfigDict(env_prefix=f"{ENV_PREFIX_API}SECURITY_RSA_")


class JWTConfig(FrozenBaseConfig):
    secret: SecretStr = Field(..., min_length=8, max_length=64)
    algorithm: constr(strip_whitespace=True) = Field(..., pattern=JWT_ALGORITHM_REGEX)  # type: ignore

    model_config = SettingsConfigDict(env_prefix=f"{ENV_PREFIX_API}SECURITY_JWT_")


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

    model_config = SettingsConfigDict(env_prefix=f"{ENV_PREFIX_API}SECURITY_")


__all__ = ["SecurityConfig", "CorsConfig", "RSAConfig", "JWTConfig"]
