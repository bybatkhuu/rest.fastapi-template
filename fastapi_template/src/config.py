# -*- coding: utf-8 -*-

import os
from typing import Dict, Any

from onion_config import ConfigLoader
from beans_logging import logger

from src.core.constants.base import EnvEnum
from src.core.schemas.configs import ConfigSchema


def _pre_load_hook(config_data: Dict[str, Any]) -> Dict[str, Any]:
    """Pre-load hook to modify config data before loading and validation.

    Args:
        config_data (Dict[str, Any]): Pre-loaded config data.

    Returns:
        Dict[str, Any]: Modified config data.
    """

    try:
        # App:
        if "app" not in config_data:
            config_data["app"] = {}

        if "name" not in config_data["app"]:
            config_data["app"][
                "name"
            ] = "FastAPI Template"  # CHANGEME: Change project title

        if "TZ" in os.environ:
            config_data["app"]["tz"]: str = os.getenv("TZ")

        if "api_version" not in config_data["app"]:
            config_data["app"]["api_version"] = "v1"

        if "api_prefix" not in config_data["app"]:
            config_data["app"][
                "api_prefix"
            ] = f"/api/{config_data['app']['api_version']}"

        config_data["app"]["api_prefix"]: str = config_data["app"]["api_prefix"].format(
            api_version=config_data["app"]["api_version"]
        )

        # Docs:
        if "docs" not in config_data:
            config_data["docs"] = {}

        if "api_prefix" in config_data["app"]:
            if "openapi_url" in config_data["docs"]:
                config_data["docs"]["openapi_url"]: str = config_data["docs"][
                    "openapi_url"
                ].format(api_prefix=config_data["app"]["api_prefix"])

            if "docs_url" in config_data["docs"]:
                config_data["docs"]["docs_url"]: str = config_data["docs"][
                    "docs_url"
                ].format(api_prefix=config_data["app"]["api_prefix"])

            if "redoc_url" in config_data["docs"]:
                config_data["docs"]["redoc_url"]: str = config_data["docs"][
                    "redoc_url"
                ].format(api_prefix=config_data["app"]["api_prefix"])

            if "swagger_ui_oauth2_redirect_url" in config_data["docs"]:
                config_data["docs"][
                    "swagger_ui_oauth2_redirect_url"
                ]: str = config_data["docs"]["swagger_ui_oauth2_redirect_url"].format(
                    api_prefix=config_data["app"]["api_prefix"]
                )

        if ("enabled" in config_data["docs"]) and (not config_data["docs"]["enabled"]):
            config_data["docs"]["openapi_url"] = None
            config_data["docs"]["docs_url"] = None
            config_data["docs"]["redoc_url"] = None
            config_data["docs"]["swagger_ui_oauth2_redirect_url"] = None

        # Dev:
        if "dev" not in config_data:
            config_data["dev"] = {}

        if os.getenv("ENV") == EnvEnum.DEVELOPMENT:
            config_data["dev"]["reload"] = True

        if "reload" not in config_data["dev"]:
            config_data["dev"]["reload"] = False

        if not config_data["dev"]["reload"]:
            config_data["dev"]["reload_includes"] = None
            config_data["dev"]["reload_excludes"] = None

        # Logger:
        if "logger" not in config_data:
            config_data["logger"] = {}

        config_data["logger"]["app_name"]: str = (
            config_data["app"]["name"].replace(" ", "_").lower()
        )

        if "file" not in config_data["logger"]:
            config_data["logger"]["file"] = {}

        config_data["logger"]["file"]["logs_dir"]: str = "/var/log/{app_name}"

    except Exception:
        logger.exception(f"Error occured while pre-loading config:")
        exit(2)

    return config_data


config: ConfigSchema
try:
    _config_loader = ConfigLoader(
        config_schema=ConfigSchema,
        pre_load_hook=_pre_load_hook,
    )
    # Main config object:
    config: ConfigSchema = _config_loader.load()
except Exception:
    logger.exception("Failed to load config:")
    exit(2)


__all__ = ["config"]
