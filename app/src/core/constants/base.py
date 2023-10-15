# -*- coding: utf-8 -*-

from enum import Enum


ENV_PREFIX = "FASTAPI_TEMPLATE_"
ENV_PREFIX_APP = f"{ENV_PREFIX}APP_"


class EnvEnum(str, Enum):
    LOCAL = "local"
    DEVELOPMENT = "development"
    TEST = "test"
    DEMO = "demo"
    DOCUMENTATION = "documentation"
    STAGING = "staging"
    PRODUCTION = "production"


class CORSMethodEnum(str, Enum):
    GET = "GET"
    POST = "POST"
    PUT = "PUT"
    PATCH = "PATCH"
    DELETE = "DELETE"
    HEAD = "HEAD"
    OPTIONS = "OPTIONS"
    CONNECT = "CONNECT"
    TRACE = "TRACE"
    ALL = "*"


class MethodEnum(str, Enum):
    GET = "GET"
    POST = "POST"
    PUT = "PUT"
    PATCH = "PATCH"
    DELETE = "DELETE"
    HEAD = "HEAD"
    OPTIONS = "OPTIONS"
    CONNECT = "CONNECT"
    TRACE = "TRACE"


__all__ = ["ENV_PREFIX", "ENV_PREFIX_APP", "EnvEnum", "CORSMethodEnum", "MethodEnum"]
