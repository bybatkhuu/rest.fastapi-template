# -*- coding: utf-8 -*-

from pydantic import Field, constr

from ._base import FrozenBaseConfig


class RSAConfig(FrozenBaseConfig):
    algorithm: constr(strip_whitespace=True) = Field(  # type: ignore
        ..., pattern=r"^(RS256|RS384|RS512)$"
    )
    key_size: int = Field(..., ge=2048, le=8192)
    private_key_fname: constr(strip_whitespace=True) = Field(  # type: ignore
        ..., min_length=2, max_length=256
    )
    public_key_fname: constr(strip_whitespace=True) = Field(  # type: ignore
        ..., min_length=2, max_length=256
    )


__all__ = ["RSAConfig"]
