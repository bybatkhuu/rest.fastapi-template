#!/usr/bin/env python
# -*- coding: utf-8 -*-

from typing import Type, Tuple, Dict, Any

from pydantic import Field, constr, field_validator, ValidationInfo, model_validator
from pydantic_settings import (
    BaseSettings,
    SettingsConfigDict,
    PydanticBaseSettingsSource,
)


class BaseConfig(BaseSettings):

    model_config = SettingsConfigDict(
        extra="allow",
        arbitrary_types_allowed=True,
    )

    @classmethod
    def settings_customise_sources(
        cls,
        settings_cls: Type[BaseSettings],
        init_settings: PydanticBaseSettingsSource,
        env_settings: PydanticBaseSettingsSource,
        dotenv_settings: PydanticBaseSettingsSource,
        file_secret_settings: PydanticBaseSettingsSource,
    ) -> Tuple[PydanticBaseSettingsSource, ...]:
        return dotenv_settings, env_settings, init_settings, file_secret_settings


class FrozenBaseConfig(BaseConfig):

    model_config = SettingsConfigDict(frozen=True)


class TestConfig(FrozenBaseConfig):
    test: constr(strip_whitespace=True, min_length=2, max_length=128) = Field(...)  # type: ignore
    number: int = Field(..., ge=80, lt=65536)

    # @model_validator(mode="before")
    # @classmethod
    # def _check_all(cls, values: Dict[str, Any]) -> Dict[str, Any]:
    #     print("values:", values)
    #     print(type(values))
    #     return values


class Config(FrozenBaseConfig):
    env: str = Field(...)
    test: constr(strip_whitespace=True, min_length=2, max_length=128) = Field(...)  # type: ignore
    number: int = Field(..., ge=80, lt=65536)
    config2: TestConfig = Field(...)

    @field_validator("test")
    @classmethod
    def _check_test(cls, val: str) -> str:
        return val

    model_config = SettingsConfigDict(
        env_file=".env",
        env_prefix="ES_",
        env_nested_delimiter="__",
    )


if __name__ == "__main__":
    _config = Config(
        # test="test",
        number=100,
        new_field="new_field",
        config2={"test": "test", "number": 100},
    )

    print(_config)
