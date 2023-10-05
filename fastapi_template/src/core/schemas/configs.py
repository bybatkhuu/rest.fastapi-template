# -*- coding: utf-8 -*-

from typing import List, Dict, Any, Optional

from pydantic import Field, constr

from beans_logging import LoggerConfigPM

from src.core.constants.base import EnvEnum, CORSMethodEnum
from .base import FrozenBaseConfig
from __version__ import __version__


# App config schema:
class AppConfig(FrozenBaseConfig):
    name: constr(strip_whitespace=True) = Field(
        default="FastAPI Template",  # CHANGEME: Change project title
        min_length=2,
        max_length=127,
    )
    bind_host: constr(strip_whitespace=True) = Field(
        default="0.0.0.0", min_length=2, max_length=127
    )
    port: int = Field(default=8000, ge=80, lt=65536)
    tz: constr(strip_whitespace=True) = Field(
        default="UTC", min_length=2, max_length=127
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


class SecureConfig(FrozenBaseConfig):
    allowed_hosts: List[
        constr(strip_whitespace=True, min_length=1, max_length=253)
    ] = Field(default=["*"])
    forwarded_allow_ips: List[
        constr(strip_whitespace=True, min_length=1, max_length=253)
    ] = Field(default=["*"])
    cors: CorsConfig = Field(CorsConfig())


class DevConfig(FrozenBaseConfig):
    reload: bool = Field(default=False)
    reload_includes: Optional[
        List[constr(strip_whitespace=True, min_length=1, max_length=255)]
    ] = Field(default=None)
    reload_excludes: Optional[
        List[constr(strip_whitespace=True, min_length=1, max_length=255)]
    ] = Field(default=None)


class DocsConfig(FrozenBaseConfig):
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
        env_prefix = (
            "FASTAPI_TEMPLATE_"  # CHANGEME: Change project env variables prefix
        )
        env_nested_delimiter = "__"


__all__ = [
    "ConfigSchema",
    "AppConfig",
    "SecureConfig",
    "CorsConfig",
    "DevConfig",
    "DocsConfig",
    "LoggerConfigPM",
]
