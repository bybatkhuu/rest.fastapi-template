# -*- coding: utf-8 -*-

import os
from typing import Dict, Any

from onion_config import ConfigLoader
from beans_logging import logger

from .core.constants import EnvEnum, ENV_PREFIX_API
from .core.configs import ConfigSchema


_required_envs = [
    f"{ENV_PREFIX_API}SECURITY_PASSWORD_PEPPER",
    f"{ENV_PREFIX_API}SECURITY_JWT_SECRET",
]


def _pre_load_hook(config_data: Dict[str, Any]) -> Dict[str, Any]:
    """Pre-load hook to modify config data before loading and validation.

    Args:
        config_data (Dict[str, Any]): Pre-loaded config data.

    Returns:
        Dict[str, Any]: Modified config data.
    """

    try:
        if "ENV" in os.environ:
            config_data["env"] = os.getenv("ENV")

        if ("env" in config_data) and (
            (config_data["env"] == EnvEnum.STAGING)
            or (config_data["env"] == EnvEnum.PRODUCTION)
        ):

            for _env in _required_envs:
                if _env not in os.environ:
                    raise KeyError(
                        f"Missing required '{_env}' environment variable for STAGING/PRODUCTION environment!"
                    )

    except Exception:
        logger.error(f"Error occured while pre-loading config!")
        raise

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
    raise SystemExit(1)


__all__ = ["config"]
