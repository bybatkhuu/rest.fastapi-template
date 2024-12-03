# -*- coding: utf-8 -*-

import os
from typing import Any, Dict, List, Optional

from pydantic import Field, constr, model_validator, field_validator
from pydantic_settings import SettingsConfigDict

from ._base import BaseConfig


class DocsConfig(BaseConfig):
    enabled: bool = Field(...)
    openapi_url: Optional[
        constr(strip_whitespace=True, max_length=128)  # type: ignore
    ] = Field(default=None)
    docs_url: Optional[
        constr(strip_whitespace=True, max_length=128)  # type: ignore
    ] = Field(default=None)
    redoc_url: Optional[
        constr(strip_whitespace=True, max_length=128)  # type: ignore
    ] = Field(default=None)
    swagger_ui_oauth2_redirect_url: Optional[
        constr(strip_whitespace=True, max_length=128)  # type: ignore
    ] = Field(default=None)
    summary: Optional[
        constr(strip_whitespace=True, min_length=2, max_length=128)  # type: ignore
    ] = Field(default=None)
    description: str = Field(default="", max_length=8192)
    terms_of_service: Optional[
        constr(strip_whitespace=True, min_length=1, max_length=256)  # type: ignore
    ] = Field(default=None)
    contact: Optional[Dict[str, Any]] = Field(default=None)
    license_info: Optional[Dict[str, Any]] = Field(default=None)
    openapi_tags: Optional[List[Dict[str, Any]]] = Field(default=None)
    swagger_ui_parameters: Optional[Dict[str, Any]] = Field(default=None)


class FrozenDocsConfig(DocsConfig):
    @field_validator("description")
    @classmethod
    def _check_description(cls, val: str) -> str:
        _desc_file_path = "./assets/description.md"
        if (not val) and os.path.isfile(_desc_file_path):
            with open(_desc_file_path, "r") as _file:
                val = _file.read()

        return val

    @model_validator(mode="before")
    @classmethod
    def _check_all(cls, values: Dict[str, Any]) -> Dict[str, Any]:

        if values["openapi_url"] == "":
            values["openapi_url"] = None

        if values["docs_url"] == "":
            values["docs_url"] = None

        if values["redoc_url"] == "":
            values["redoc_url"] = None

        if values["swagger_ui_oauth2_redirect_url"] == "":
            values["swagger_ui_oauth2_redirect_url"] = None

        if not values["enabled"]:
            values["openapi_url"] = None
            values["docs_url"] = None
            values["redoc_url"] = None
            values["swagger_ui_oauth2_redirect_url"] = None

        return values

    model_config = SettingsConfigDict(frozen=True)


__all__ = ["DocsConfig", "FrozenDocsConfig"]
