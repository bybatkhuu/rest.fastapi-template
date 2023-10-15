# -*- coding: utf-8 -*-

## Third-party libraries
import uvicorn

## Internal modules
from src.config import config
from src.logger import logger


if __name__ == "__main__":
    logger.info(f"Starting server from '__main__.py'...")
    uvicorn.run(
        app="main:app",
        host=config.app.bind_host,
        port=config.app.port,
        access_log=False,
        server_header=False,
        proxy_headers=config.app.behind_proxy,
        forwarded_allow_ips=config.app.forwarded_allow_ips,
        **config.app.dev.dict(),
    )
