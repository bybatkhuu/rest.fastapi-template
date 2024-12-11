# 🚸 Examples

## CLI

Send request to the server using `curl` and parse the response using `jq`:

```sh
curl -s http://localhost:8000/api/v1/ping | jq
```

## Simple

Using python `requests` library to send request to the server:

[**`examples/simple/main.py`**](https://github.com/bybatkhuu/rest.fastapi-template/blob/main/examples/simple/main.py):

```python
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
```

## Async

Using python `aiohttp` library to send request to the server:

[**`examples/async/main.py`**](https://github.com/bybatkhuu/rest.fastapi-template/blob/main/examples/async/main.py):

```python
## Standard libraries
import sys
import logging
import pprint
import asyncio
from typing import Dict, Any

## Third-party libraries
import aiohttp


logger = logging.getLogger(__name__)


async def main() -> None:
    logging.basicConfig(stream=sys.stdout, level=logging.INFO)

    _base_url = "http://localhost:8000"
    _api_prefix = "/api/v1"
    _endpoint = "/ping"
    _method = "GET"

    _url = f"{_base_url}{_api_prefix}{_endpoint}"
    _payload = {}
    _headers = {"Accept": "application/json"}

    logger.info("Sending request...")
    _result_dict: Dict[str, Any] = {}
    async with aiohttp.ClientSession() as _http_session:
        async with _http_session.request(
            method=_method, url=_url, headers=_headers, json=_payload
        ) as _response:
            _result_dict = await _response.json()
    logger.info("Done!\n")

    logging.info(f"\n{pprint.pformat(_result_dict)}")


if __name__ == "__main__":
    asyncio.run(main())
```
