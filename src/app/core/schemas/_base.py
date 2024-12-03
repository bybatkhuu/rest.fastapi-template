# -*- coding: utf-8 -*-

from datetime import datetime

from pydantic import BaseModel, Field, constr, ConfigDict

from app.core import utils


class BasePM(BaseModel):
    model_config = ConfigDict(json_encoders={datetime: utils.datetime_to_iso})


class ExtraBasePM(BasePM):
    model_config = ConfigDict(extra="allow")


class IdPM(BasePM):
    id: constr(strip_whitespace=True) = Field(  # type: ignore
        ...,
        min_length=8,
        max_length=64,
        title="ID",
        description="Identifier value of the resource.",
        examples=["res1701388800_dc2cc6c9033c4837b6c34c8bb19bb289"],
    )


class TimestampPM(BasePM):
    updated_at: datetime = Field(
        ...,
        title="Updated datetime",
        description="Last updated datetime of the resource.",
        examples=["2024-12-01T00:00:00+00:00"],
    )
    created_at: datetime = Field(
        ...,
        title="Created datetime",
        description="Created datetime of the resource.",
        examples=["2024-12-01T00:00:00+00:00"],
    )


__all__ = [
    "BasePM",
    "ExtraBasePM",
    "IdPM",
    "TimestampPM",
]