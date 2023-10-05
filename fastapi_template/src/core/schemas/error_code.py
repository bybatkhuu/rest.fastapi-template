# -*- coding: utf-8 -*-

from typing import Optional, Any

from pydantic import BaseModel, constr, Field


class ErrorCodePM(BaseModel):
    code: constr(strip_whitespace=True) = Field(..., min_length=3, max_length=36)
    name: constr(strip_whitespace=True) = Field(..., min_length=3, max_length=64)
    status_code: int = Field(..., ge=100, le=599)
    message: constr(strip_whitespace=True) = Field(..., min_length=1, max_length=255)
    description: Optional[constr(strip_whitespace=True)] = Field(
        default=None, max_length=511
    )
    detail: Any = Field(default=None)

    class Config:
        frozen = True


__all__ = ["ErrorCodePM"]
