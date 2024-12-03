# -*- coding: utf-8 -*-

from pydantic import Field, constr, field_validator, ValidationInfo
from pydantic_settings import SettingsConfigDict

from ._base import BaseConfig
from ._dev import DevConfig
from ._security import SecurityConfig
from ._docs import DocsConfig, FrozenDocsConfig
from ._paths import PathsConfig, FrozenPathsConfig
from ._routes import RoutesConfig


class ApiConfig(BaseConfig):
    name: constr(strip_whitespace=True) = Field(..., min_length=2, max_length=128)  # type: ignore
    slug: constr(strip_whitespace=True) = Field(..., min_length=2, max_length=128)  # type: ignore
    bind_host: constr(strip_whitespace=True) = Field(..., min_length=2, max_length=128)  # type: ignore
    port: int = Field(..., ge=80, lt=65536)
    version: constr(strip_whitespace=True) = Field(..., min_length=1, max_length=16)  # type: ignore
    prefix: constr(strip_whitespace=True) = Field(..., max_length=128)  # type: ignore
    gzip_min_size: int = Field(..., ge=0, le=10_485_760)  # 512 bytes
    behind_proxy: bool = Field(...)
    behind_cf_proxy: bool = Field(...)
    dev: DevConfig = Field(...)
    security: SecurityConfig = Field(...)
    docs: DocsConfig = Field(...)
    paths: PathsConfig = Field(...)
    routes: RoutesConfig = Field(default_factory=RoutesConfig)

    @field_validator("slug")
    @classmethod
    def _check_slug(cls, val: str, info: ValidationInfo) -> str:
        if "name" in info.data:
            val = (
                info.data["name"]
                .lower()
                .strip()
                .replace(" ", "-")
                .replace("_", "-")
                .replace(".", "-")
            )

        return val

    @field_validator("prefix")
    @classmethod
    def _check_prefix(cls, val: str, info: ValidationInfo) -> str:
        if val and ("{api_version}" in val) and ("version" in info.data):
            val = val.format(api_version=info.data["version"])

        return val

    @field_validator("docs")
    @classmethod
    def _check_docs(cls, val: DocsConfig, info: ValidationInfo) -> DocsConfig:
        if val.enabled and ("prefix" in info.data):
            if val.openapi_url and ("{api_prefix}" in val.openapi_url):
                val.openapi_url = val.openapi_url.format(api_prefix=info.data["prefix"])

            if val.docs_url and ("{api_prefix}" in val.docs_url):
                val.docs_url = val.docs_url.format(api_prefix=info.data["prefix"])

            if val.redoc_url and ("{api_prefix}" in val.redoc_url):
                val.redoc_url = val.redoc_url.format(api_prefix=info.data["prefix"])

            if val.swagger_ui_oauth2_redirect_url and (
                "{api_prefix}" in val.swagger_ui_oauth2_redirect_url
            ):
                val.swagger_ui_oauth2_redirect_url = (
                    val.swagger_ui_oauth2_redirect_url.format(
                        api_prefix=info.data["prefix"]
                    )
                )

        val = FrozenDocsConfig(**val.model_dump())
        return val

    @field_validator("paths")
    @classmethod
    def _check_paths(cls, val: PathsConfig, info: ValidationInfo) -> FrozenPathsConfig:
        if "slug" in info.data:
            if "{app_slug}" in val.tmp_dir:
                val.tmp_dir = val.tmp_dir.format(app_slug=info.data["slug"])

            if "{app_slug}" in val.uploads_dir:
                val.uploads_dir = val.uploads_dir.format(app_slug=info.data["slug"])

            if "{app_slug}" in val.data_dir:
                val.data_dir = val.data_dir.format(app_slug=info.data["slug"])

            if "{tmp_dir}" in val.uploads_dir:
                val.uploads_dir = val.uploads_dir.format(tmp_dir=val.tmp_dir)

        val = FrozenPathsConfig(**val.model_dump())
        return val


class FrozenApiConfig(ApiConfig):
    model_config = SettingsConfigDict(frozen=True)


__all__ = ["ApiConfig", "FrozenApiConfig"]
