# -*- coding: utf-8 -*-

import os

from pydantic import Field, constr, field_validator, ValidationInfo
from pydantic_settings import SettingsConfigDict

from beans_logging import LoggerConfigPM

from app.__version__ import __version__
from app.core.constants import EnvEnum, ENV_PREFIX, ENV_PREFIX_API

from ._base import FrozenBaseConfig
from ._dev import DevConfig, FrozenDevConfig
from ._api import ApiConfig, FrozenApiConfig


# Main config schema:
class ConfigSchema(FrozenBaseConfig):
    env: EnvEnum = Field(...)
    debug: bool = Field(...)
    version: constr(strip_whitespace=True) = Field(  # type: ignore
        default=__version__, min_length=3, max_length=32
    )
    api: ApiConfig = Field(...)
    logger: LoggerConfigPM = Field(default_factory=LoggerConfigPM)

    @field_validator("version")
    @classmethod
    def _check_version(cls, val: str) -> str:
        val = __version__
        return val

    @field_validator("api")
    @classmethod
    def _check_api(cls, val: ApiConfig, info: ValidationInfo) -> FrozenApiConfig:
        _dev: DevConfig = val.dev
        if ("env" in info.data) and (info.data["env"] == EnvEnum.DEVELOPMENT):
            _dev.reload = True
        _dev = FrozenDevConfig(**_dev.model_dump())

        val = FrozenApiConfig(dev=_dev, **val.model_dump(exclude={"dev"}))
        return val

    @field_validator("logger")
    @classmethod
    def _check_logger(cls, val: LoggerConfigPM, info: ValidationInfo) -> LoggerConfigPM:
        if "api" in info.data:
            if not val.app_name:
                val.app_name = info.data["api"].slug
            elif "{app_slug}" in val.app_name:
                val.app_name = val.app_name.format(app_slug=info.data["api"].slug)

        if f"{ENV_PREFIX_API}LOGS_DIR" in os.environ:
            val.file.logs_dir = os.getenv(f"{ENV_PREFIX_API}LOGS_DIR")

        return val

    model_config = SettingsConfigDict(env_prefix=ENV_PREFIX, env_nested_delimiter="__")


__all__ = ["ConfigSchema"]
