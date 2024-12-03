# -*- coding: utf-8 -*-

from typing import Any, Dict

from pydantic import Field, constr, SecretStr, model_validator

from ._base import FrozenBaseConfig


class JWTConfig(FrozenBaseConfig):
    secret: SecretStr = Field(..., min_length=8, max_length=64)
    algorithm: constr(strip_whitespace=True) = Field(  # type: ignore
        ...,
        pattern=r"^(HS256|HS384|HS512|ES256|ES256K|ES384|ES512|RS256|RS384|RS512|PS256|PS384|PS512|EdDSA)$",
    )
    access_duration: int = Field(..., ge=300, le=86400)
    refresh_window: int = Field(..., ge=60, le=86400)
    verify_duration: int = Field(..., ge=300, le=86400)
    reset_duration: int = Field(..., ge=300, le=86400)
    refresh_duration: int = Field(..., ge=86400, le=15552000)
    remember_duration: int = Field(..., ge=86400, le=15552000)

    @model_validator(mode="before")
    @classmethod
    def _check_all(cls, values: Dict[str, Any]) -> Dict[str, Any]:
        if values["access_duration"] < values["refresh_window"]:
            raise ValueError(
                "`access_duration` should be greater or equal to `refresh_window`!"
            )

        if values["remember_duration"] < values["refresh_duration"]:
            raise ValueError(
                "`remember_duration` should be greater or equal to `refresh_duration`!"
            )

        return values


__all__ = ["JWTConfig"]
