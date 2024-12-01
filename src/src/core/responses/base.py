# -*- coding: utf-8 -*-

from http import HTTPStatus
from typing import Any, Optional, Dict, Type

from pydantic import validate_arguments, conint, constr
from starlette.background import BackgroundTask
from fastapi import Request
from fastapi.responses import JSONResponse

from src.config import config
from src.core import utils
from src.core.constants.base import EnvEnum
from src.core.schemas.responses import BaseResPM
from __version__ import __version__


class BaseResponse(JSONResponse):
    """Base response class for most of the API responses with JSON format.
    Based on BaseResPM schema.

    Inherits:
        JSONResponse: JSON response class from FastAPI.
    """

    @validate_arguments(config=dict(arbitrary_types_allowed=True))
    def __init__(
        self,
        content: Any = None,
        status_code: Optional[conint(ge=100, le=599)] = 200,
        headers: Optional[
            Dict[constr(strip_whitespace=True), constr(strip_whitespace=True)]
        ] = None,
        media_type: Optional[constr(strip_whitespace=True)] = None,
        background: Optional[BackgroundTask] = None,
        request: Optional[Request] = None,
        message: Optional[
            constr(strip_whitespace=True, min_length=1, max_length=255)
        ] = None,
        links: Optional[Dict[constr(strip_whitespace=True), Any]] = None,
        meta: Optional[Dict[constr(strip_whitespace=True), Any]] = None,
        error: Any = None,
        response_schema: Optional[Type[BaseResPM]] = BaseResPM,
    ):
        """Constructor method for BaseResponse class.
        This will prepare the most response data and pass it to `JSONResponse` parent class constructor.

        Args:
            content         (Any                      , optional): Main data content for response. Defaults to None.
            status_code     (Optional[int]            , optional): HTTP status code: [100 <= status_code <= 599]. Defaults to 200.
            headers         (Optional[Dict[str, str]] , optional): HTTP headers. Defaults to None.
            media_type      (Optional[str]            , optional): Media type for 'Content-Type' header. Defaults to None.
            background      (Optional[BackgroundTask] , optional): Background task. Defaults to None.
            request         (Optional[Request]        , optional): Request object from FastAPI. Defaults to None.
            message         (Optional[str]            , optional): Message for response: [1 <= len(message) <= 255]. Defaults to None.
            links           (Optional[Dict[str, Any]] , optional): Links for response. Defaults to None.
            meta            (Optional[Dict[str, Any]] , optional): Meta data for response. Defaults to None.
            error           (Any                      , optional): Error data for response. Defaults to None.
            response_schema (Optional[Type[BaseResPM]], optional): Response schema type. Defaults to Type[BaseResPM].
        """

        _http_status: HTTPStatus
        _http_status, _ = utils.get_http_status(status_code=status_code)

        if not message:
            if error and isinstance(error, dict) and ("message" in error):
                message = str(error["message"])
            else:
                message: str = _http_status.phrase

        if not links:
            links = {}

        if not meta:
            meta = {}

        if request:
            _http_info: dict = request.state.http_info
            _self_link = f"{_http_info['request_proto']}://{_http_info['request_host']}{utils.get_request_path(request)}"
            links["self"] = _self_link
            meta["request_id"]: str = request.state.request_id
            meta["method"]: str = request.method

            if not headers:
                headers = {"X-Request-Id": request.state.request_id}
            elif "X-Request-Id" not in headers:
                headers["X-Request-Id"] = request.state.request_id

        meta["api_version"]: str = config.api.version
        meta["version"]: str = __version__

        if (
            (config.env == EnvEnum.PRODUCTION)
            and (not config.debug)
            and (500 <= status_code)
        ):
            error = None

        if (error is None) and (400 <= status_code) and _http_status.description:
            error = f"{_http_status.description}!"

        if error and isinstance(error, dict) and ("code" in error):
            if not headers:
                headers = {"X-Error-Code": error.get("code")}
            elif "X-Error-Code" not in headers:
                headers["X-Error-Code"] = error.get("code")

        response_pm = response_schema(
            message=message, data=content, links=links, meta=meta, error=error
        )
        _content = response_pm.dict(by_alias=True)

        super().__init__(
            content=_content,
            status_code=status_code,
            headers=headers,
            media_type=media_type,
            background=background,
        )


__all__ = ["BaseResponse"]
