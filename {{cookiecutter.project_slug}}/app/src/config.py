# -*- coding: utf-8 -*-

from typing import Dict, Any

from onion_config import ConfigLoader
from beans_logging import logger

from src.core.schemas.configs import ConfigSchema


def _pre_load_hook(config_data: Dict[str, Any]) -> Dict[str, Any]:
    """Pre-load hook to modify config data before loading and validation.

    Args:
        config_data (Dict[str, Any]): Pre-loaded config data.

    Returns:
        Dict[str, Any]: Modified config data.
    """

    # Modify config_data here...

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
