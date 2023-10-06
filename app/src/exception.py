# -*- coding: utf-8 -*-

from pydantic import validate_arguments
from fastapi import FastAPI, HTTPException
from fastapi.exceptions import RequestValidationError

from src.core.handlers.status import (
    not_found_handler,
    method_not_allowed_handler,
    server_error_handler,
)
from src.core.handlers.raises import (
    http_exception_handler,
    validation_error_handler,
)


@validate_arguments(config=dict(arbitrary_types_allowed=True))
def add_exception_handlers(app: FastAPI):
    """Add exception handlers to FastAPI application.

    Args:
        app (FastAPI): FastAPI application instance.
    """

    app.add_exception_handler(404, not_found_handler)
    app.add_exception_handler(405, method_not_allowed_handler)
    app.add_exception_handler(500, server_error_handler)
    app.add_exception_handler(HTTPException, http_exception_handler)
    app.add_exception_handler(RequestValidationError, validation_error_handler)
    # Add more exception handlers here...


__all__ = ["add_exception_handlers"]
