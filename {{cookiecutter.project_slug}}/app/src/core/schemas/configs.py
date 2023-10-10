# -*- coding: utf-8 -*-

import os
from typing import List, Dict, Any, Optional

from pydantic import Field, constr, root_validator, validator

from beans_logging import LoggerConfigPM

from src.core.constants.base import EnvEnum, CORSMethodEnum
from .base import FrozenBaseConfig, BaseConfig
from __version__ import __version__


_ENV_PREFIX = "{{cookiecutter.env_prefix}}"


# App config schema:
class AppConfig(FrozenBaseConfig):
    name: constr(strip_whitespace=True) = Field(
        default="{{cookiecutter.project_name}}",
        min_length=2,
        max_length=127,
    )
    bind_host: constr(strip_whitespace=True) = Field(
        default="0.0.0.0", min_length=2, max_length=127
    )
    port: int = Field(default=8000, ge=80, lt=65536, env=f"{_ENV_PREFIX}PORT")
    tz: constr(strip_whitespace=True) = Field(
        default="UTC", min_length=2, max_length=127, env="TZ"
    )
    version: constr(strip_whitespace=True) = Field(
        default=__version__, min_length=3, max_length=31
    )
    api_version: constr(strip_whitespace=True) = Field(
        default="v1", min_length=1, max_length=15
    )
    api_prefix: constr(strip_whitespace=True) = Field(default="", max_length=127)
    behind_proxy: bool = Field(default=True)
    behind_cf_proxy: bool = Field(default=False)
    gzip_min_size: int = Field(default=512, ge=0, le=10_485_760)
    data_dir: constr(strip_whitespace=True) = Field(
        default="/var/lib/{{cookiecutter.project_slug}}",
        min_length=2,
        max_length=1023,
        env=f"{_ENV_PREFIX}DATA_DIR",
    )

    @validator("api_prefix", always=True)
    def _check_api_prefix(cls, val: Any, values: dict):
        if (
            isinstance(val, str)
            and ("{api_version}" in val)
            and ("api_version" in values)
        ):
            val = val.format(api_version=values["api_version"])
        return val

    class Config:
        env_prefix = f"{_ENV_PREFIX}APP_"


class CorsConfig(FrozenBaseConfig):
    allow_origins: List[
        constr(strip_whitespace=True, min_length=1, max_length=253)
    ] = Field(default=["*"])
    allow_origin_regex: Optional[
        constr(strip_whitespace=True, min_length=1, max_length=253)
    ] = Field(default=None)
    allow_headers: List[
        constr(strip_whitespace=True, min_length=1, max_length=127)
    ] = Field(default=["*"])
    allow_methods: List[CORSMethodEnum] = Field(default=[CORSMethodEnum.ALL])
    allow_credentials: bool = Field(default=False)
    expose_headers: List[
        constr(strip_whitespace=True, min_length=1, max_length=127)
    ] = Field(default=[])
    max_age: int = Field(default=600, ge=0, le=86_400)

    class Config:
        env_prefix = f"{_ENV_PREFIX}SECURE_CORS_"


class SecureConfig(FrozenBaseConfig):
    allowed_hosts: List[
        constr(strip_whitespace=True, min_length=1, max_length=253)
    ] = Field(default=["*"])
    forwarded_allow_ips: List[
        constr(strip_whitespace=True, min_length=1, max_length=253)
    ] = Field(default=["*"])
    cors: CorsConfig = Field(default_factory=CorsConfig)

    class Config:
        env_prefix = f"{_ENV_PREFIX}SECURE_"


class DevConfig(BaseConfig):
    reload: bool = Field(default=False)
    reload_includes: Optional[
        List[constr(strip_whitespace=True, min_length=1, max_length=255)]
    ] = Field(default=None)
    reload_excludes: Optional[
        List[constr(strip_whitespace=True, min_length=1, max_length=255)]
    ] = Field(default=None)

    class Config:
        env_prefix = f"{_ENV_PREFIX}DEV_"


class FrozenDevConfig(DevConfig):
    class Config:
        frozen = True

    @root_validator(skip_on_failure=True)
    def _check_reload(cls, values: dict):
        if "reload" in values:
            if not values["reload"]:
                values["reload_includes"] = None
                values["reload_excludes"] = None
        return values


class DocsConfig(BaseConfig):
    enabled: bool = Field(default=True)
    openapi_url: Optional[
        constr(strip_whitespace=True, min_length=8, max_length=127)
    ] = Field(default="/openapi.json")
    docs_url: Optional[
        constr(strip_whitespace=True, min_length=5, max_length=127)
    ] = Field(default="/docs")
    redoc_url: Optional[
        constr(strip_whitespace=True, min_length=6, max_length=127)
    ] = Field(default="/redoc")
    swagger_ui_oauth2_redirect_url: Optional[
        constr(strip_whitespace=True, min_length=12, max_length=127)
    ] = Field(default="/docs/oauth2-redirect")
    summary: Optional[
        constr(strip_whitespace=True, min_length=1, max_length=127)
    ] = Field(default=None)
    description: str = Field(default="", max_length=8192)
    terms_of_service: Optional[
        constr(strip_whitespace=True, min_length=1, max_length=255)
    ] = Field(default=None)
    contact: Optional[Dict[str, Any]] = Field(default=None)
    license_info: Optional[Dict[str, Any]] = Field(default=None)
    openapi_tags: Optional[List[Dict[str, Any]]] = Field(default=None)
    swagger_ui_parameters: Optional[Dict[str, Any]] = Field(default=None)

    class Config:
        env_prefix = f"{_ENV_PREFIX}DOCS_"

    @validator("description", always=True)
    def _check_description(cls, val: Any):
        _desc_path = "./assets/description.md"
        if (not val) and os.path.isfile(_desc_path):
            with open(_desc_path, "r") as _file:
                val = _file.read()
        return val

    @root_validator(skip_on_failure=True)
    def _check_enabled(cls, values: dict):
        if "enabled" in values:
            if not values["enabled"]:
                values["openapi_url"] = None
                values["docs_url"] = None
                values["redoc_url"] = None
                values["swagger_ui_oauth2_redirect_url"] = None
        return values


class FrozenDocsConfig(DocsConfig):
    class Config:
        frozen = True


# Main config schema:
class ConfigSchema(FrozenBaseConfig):
    env: EnvEnum = Field(default=EnvEnum.LOCAL, env="ENV")
    debug: bool = Field(default=False, env="DEBUG")
    app: AppConfig = Field(default_factory=AppConfig)
    secure: SecureConfig = Field(default_factory=SecureConfig)
    dev: DevConfig = Field(default_factory=DevConfig)
    docs: DocsConfig = Field(default_factory=DocsConfig)
    logger: LoggerConfigPM = Field(default_factory=LoggerConfigPM)

    class Config:
        env_prefix = f"{_ENV_PREFIX}"
        env_nested_delimiter = "__"

    @validator("docs", always=True)
    def _check_docs_url_prefix(cls, val: DocsConfig, values: dict):
        if val.enabled:
            if "{api_prefix}" in val.openapi_url:
                val.openapi_url = val.openapi_url.format(
                    api_prefix=values["app"].api_prefix
                )

            if "{api_prefix}" in val.docs_url:
                val.docs_url = val.docs_url.format(api_prefix=values["app"].api_prefix)

            if "{api_prefix}" in val.redoc_url:
                val.redoc_url = val.redoc_url.format(
                    api_prefix=values["app"].api_prefix
                )

            if "{api_prefix}" in val.swagger_ui_oauth2_redirect_url:
                val.swagger_ui_oauth2_redirect_url = (
                    val.swagger_ui_oauth2_redirect_url.format(
                        api_prefix=values["app"].api_prefix
                    )
                )

        val = FrozenDocsConfig(**val.dict())
        return val

    @validator("dev", always=True)
    def _check_dev_reload(cls, val: DevConfig, values: dict):
        if values["env"] == EnvEnum.DEVELOPMENT:
            val.reload = True

        val = FrozenDevConfig(**val.dict())
        return val

    @validator("logger", always=True)
    def _check_logger(cls, val: LoggerConfigPM, values: dict):
        # val.app_name = (
        #     values["app"].name.strip().lower().replace(" ", "-").replace("_", "-")
        # ).replace(".", "-")
        if f"{_ENV_PREFIX}LOGS_DIR" in os.environ:
            val.file.logs_dir = os.getenv(f"{_ENV_PREFIX}LOGS_DIR")
        return val


__all__ = [
    "ConfigSchema",
    "AppConfig",
    "SecureConfig",
    "CorsConfig",
    "DevConfig",
    "DocsConfig",
    "LoggerConfigPM",
]
