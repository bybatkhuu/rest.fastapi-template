#!/usr/bin/env python
# -*- coding: utf-8 -*-

## Internal modules
from app.server import app, run_server
from app.logger import logger


if __name__ == "__main__":
    logger.info(f"Starting server from 'main.py'...")
    run_server()

__all__ = ["app"]
