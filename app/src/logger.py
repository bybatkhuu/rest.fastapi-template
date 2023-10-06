# -*- coding: utf-8 -*-

from pydantic import validate_arguments
from fastapi import Request
from fastapi.concurrency import run_in_threadpool

from beans_logging import Logger, LoggerLoader
from beans_logging.fastapi import add_http_file_handler, add_http_file_json_handler

from src.config import config


logger_loader = LoggerLoader(config=config.logger, auto_config_file=False)
logger: Logger = logger_loader.load()

if config.logger.extra.http_file_enabled:
    add_http_file_handler(
        logger_loader=logger_loader,
        log_path=config.logger.extra.http_log_path,
        err_path=config.logger.extra.http_err_path,
    )

if config.logger.extra.http_json_enabled:
    add_http_file_json_handler(
        logger_loader=logger_loader,
        log_path=config.logger.extra.http_json_path,
        err_path=config.logger.extra.http_json_err_path,
    )


@validate_arguments(config=dict(arbitrary_types_allowed=True))
async def log_http_error(request: Request, status_code: int):
    """Log HTTP error for unhandled Exception.

    Args:
        request     (Request, required): Request instance.
        status_code (int    , required): HTTP status code.
    """

    _MSG_FORMAT = '<n><w>[{request_id}]</w></n> {client_host} {user_id} "<u>{method} {url_path}</u> HTTP/{http_version}" <n>{status_code}</n>'

    _http_info: dict = request.state.http_info
    _http_info["status_code"] = status_code

    _msg = _MSG_FORMAT.format(**_http_info)
    _logger: Logger = logger.opt(colors=True, record=True).bind(http_info=_http_info)
    await run_in_threadpool(_logger.error, _msg)


@validate_arguments
async def log_trace(message: str):
    """Log trace message.

    Args:
        message (str, required): Message to log.
    """

    await run_in_threadpool(logger.trace, message)


@validate_arguments
async def log_debug(message: str):
    """Log debug message.

    Args:
        message (str, required): Message to log.
    """

    await run_in_threadpool(logger.debug, message)


@validate_arguments
async def log_info(message: str):
    """Log info message.

    Args:
        message (str, required): Message to log.
    """

    await run_in_threadpool(logger.info, message)


@validate_arguments
async def log_success(message: str):
    """Log success message.

    Args:
        message (str, required): Message to log.
    """

    await run_in_threadpool(logger.success, message)


@validate_arguments
async def log_warning(message: str):
    """Log warning message.

    Args:
        message (str, required): Message to log.
    """

    await run_in_threadpool(logger.warning, message)


@validate_arguments
async def log_critical(message: str):
    """Log critical message.

    Args:
        message (str, required): Message to log.
    """

    await run_in_threadpool(logger.critical, message)


@validate_arguments
async def log_level(level: str, message: str):
    """Log level message.

    Args:
        level   (str, required): Log level.
        message (str, required): Message to log.
    """

    await run_in_threadpool(logger.log, level, message)


__all__ = [
    "logger_loader",
    "logger",
    "log_http_error",
    "log_trace",
    "log_debug",
    "log_info",
    "log_success",
    "log_warning",
    "log_critical",
    "log_level",
]
