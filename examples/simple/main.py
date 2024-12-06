#!/usr/bin/env python
# -*- coding: utf-8 -*-

## Standard libraries
import sys
import logging
import pprint

## Third-party libraries
import requests


logger = logging.getLogger(__name__)


if __name__ == "__main__":
    logging.basicConfig(stream=sys.stdout, level=logging.INFO)

    _base_url = "http://localhost:8000"
    _api_prefix = "/api/v1"
    _endpoint = "/ping"
    _method = "GET"

    _url = f"{_base_url}{_api_prefix}{_endpoint}"
    _payload = {}
    _headers = {"Accept": "application/json"}

    logger.info("Sending request...")
    response = requests.request(
        method=_method, url=_url, headers=_headers, data=_payload
    )
    logger.info("Done!\n")

    logging.info(f"\n{pprint.pformat(response.json())}")