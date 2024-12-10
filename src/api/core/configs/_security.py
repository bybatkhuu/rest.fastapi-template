# -*- coding: utf-8 -*-

from typing import List, Optional, Dict, Any

from pydantic import Field, constr, SecretStr, model_validator
from pydantic_settings import SettingsConfigDict

from api.core.constants import (
    ENV_PREFIX_API,
    HTTP_METHOD_REGEX,
    ASYMMETRIC_ALGORITHM_REGEX,
    JWT_ALGORITHM_REGEX,
)
from ._base import FrozenBaseConfig


_ENV_PREFIX_SECURITY = f"{ENV_PREFIX_API}SECURITY_"


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

    model_config = SettingsConfigDict(env_prefix=f"{_ENV_PREFIX_SECURITY}CORS_")


class PasswordConfig(FrozenBaseConfig):
    pepper: SecretStr = Field(..., min_length=8, max_length=32)
    min_length: int = Field(..., ge=8, le=128)
    max_length: int = Field(..., ge=8, le=128)

    @model_validator(mode="before")
    @classmethod
    def _check_all(cls, values: Dict[str, Any]) -> Dict[str, Any]:
        if values["max_length"] < values["min_length"]:
            raise ValueError(
                "`min_length` is greater than `max_length`, should be vice versa!"
            )

        return values

    model_config = SettingsConfigDict(env_prefix=f"{_ENV_PREFIX_SECURITY}PASSWORD_")


class AsymmetricKeysConfig(FrozenBaseConfig):
    algorithm: constr(strip_whitespace=True) = Field(..., pattern=ASYMMETRIC_ALGORITHM_REGEX)  # type: ignore
    key_size: int = Field(..., ge=2048, le=8192)
    private_key_fname: constr(strip_whitespace=True) = Field(  # type: ignore
        ..., min_length=2, max_length=256
    )
    public_key_fname: constr(strip_whitespace=True) = Field(  # type: ignore
        ..., min_length=2, max_length=256
    )

    model_config = SettingsConfigDict(
        env_prefix=f"{_ENV_PREFIX_SECURITY}ASYMMETRIC_KEYS_"
    )


class JWTConfig(FrozenBaseConfig):
    secret: SecretStr = Field(..., min_length=8, max_length=64)
    algorithm: constr(strip_whitespace=True) = Field(..., pattern=JWT_ALGORITHM_REGEX)  # type: ignore

    model_config = SettingsConfigDict(env_prefix=f"{_ENV_PREFIX_SECURITY}JWT_")


class SecurityConfig(FrozenBaseConfig):
    allowed_hosts: List[constr(strip_whitespace=True, min_length=1, max_length=256)] = (  # type: ignore
        Field(...)
    )
    forwarded_allow_ips: List[
        constr(strip_whitespace=True, min_length=1, max_length=256)  # type: ignore
    ] = Field(...)
    cors: CorsConfig = Field(...)
    password: PasswordConfig = Field(default_factory=PasswordConfig)
    asymmetric_keys: AsymmetricKeysConfig = Field(...)
    jwt: JWTConfig = Field(...)

    model_config = SettingsConfigDict(env_prefix=_ENV_PREFIX_SECURITY)


__all__ = ["SecurityConfig", "CorsConfig", "AsymmetricKeysConfig", "JWTConfig"]
