#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from typing import Union

import uvicorn
from fastapi import FastAPI, Request
from dotenv import load_dotenv

from __version__ import __version__


load_dotenv()

app = FastAPI()


@app.get("/")
async def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
async def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}


@app.get("/api/v1/ping")
async def ping(request: Request):

    _response = {
        "message": "Pong!",
        "links": {
            "self": "/api/v1/ping"
        },
        "meta": {
            "api_version": "v1",
            "version": __version__,
            "method": request.method
        }
    }
    return _response


@app.get("/api/v1/health")
async def health(request: Request):

    _response = {
        "message": "Everything is OK.",
        "data": {},
        "links": {
            "self": "/api/v1/health"
        },
        "meta": {
            "api_version": "v1",
            "version": __version__,
            "method": request.method
        }
    }
    return _response


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=int(os.getenv("FASTAPI_PORT", "8000")), access_log=False)
