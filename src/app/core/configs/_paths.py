# -*- coding: utf-8 -*-

from typing import Any, Dict

from pydantic import Field, constr, model_validator
from pydantic_settings import SettingsConfigDict

from app.core.constants import ENV_PREFIX_API

from ._base import BaseConfig


class PathsConfig(BaseConfig):
    tmp_dir: constr(strip_whitespace=True) = Field(..., min_length=2, max_length=1024)  # type: ignore
    uploads_dir: constr(strip_whitespace=True) = Field(  # type: ignore
        ..., min_length=2, max_length=1024
    )
    data_dir: constr(strip_whitespace=True) = Field(  # type: ignore
        ..., min_length=2, max_length=1024
    )
    credentials_dir: constr(strip_whitespace=True) = Field(  # type: ignore
        ..., min_length=2, max_length=1024
    )
    rsa_keys_dir: constr(strip_whitespace=True) = Field(  # type: ignore
        ..., min_length=2, max_length=1024
    )
    # models_dir: constr(strip_whitespace=True) = Field(  # type: ignore
    #     ..., min_length=2, max_length=1024
    # )
    # model_dir: constr(strip_whitespace=True) = Field(..., min_length=2, max_length=1024)  # type: ignore


class FrozenPathsConfig(PathsConfig):
    @model_validator(mode="before")
    @classmethod
    def _check_all(cls, values: Dict[str, Any]) -> Dict[str, Any]:
        for _key, _val in values.items():
            if isinstance(_val, str) and ("{data_dir}" in _val):
                values[_key] = _val.format(data_dir=values["data_dir"])

        return values

    model_config = SettingsConfigDict(frozen=True)


__all__ = ["PathsConfig", "FrozenPathsConfig"]
