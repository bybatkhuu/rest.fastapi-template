# -*- coding: utf-8 -*-

from fastapi import Request
from pydantic import validate_arguments


@validate_arguments(config=dict(arbitrary_types_allowed=True))
def get_request_path(request: Request) -> str:
    """Get request path with query params.

    Args:
        request (Request, required): Request object.

    Returns:
        str: Request path.
    """

    _url_path = request.url.path
    if request.url.query:
        _url_path += "?" + request.url.query
    return _url_path


__all__ = ["get_request_path"]
