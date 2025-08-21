import requests
from typing import Dict, Any, Optional
from .logger import get_test_logger
from . import config

logger = get_test_logger()

class HttpClient:
    def __init__(self, base_url: str = None, default_headers: Optional[Dict[str, str]] = None):
        self.base_url = base_url or config.BASE_URL
        self.default_headers = default_headers or {"Content-Type": "application/json"}

    def _url(self, path: str) -> str:
        return path if path.startswith("http") else f"{self.base_url.rstrip('/')}/{path.lstrip('/')}"

    def request(self, method: str, path: str, **kwargs) -> requests.Response:
        headers = kwargs.pop("headers", {})
        merged = {**self.default_headers, **headers}
        url = self._url(path)
        logger.info(f"{method.upper()} {url}")
        resp = requests.request(method=method, url=url, headers=merged, **kwargs)
        logger.info(f"-> {resp.status_code}")
        if resp.content:
            logger.info(f"Response body: {resp.text[:500]}")
        return resp

    def get(self, path: str, **kwargs):
        return self.request("GET", path, **kwargs)

    def post(self, path: str, **kwargs):
        return self.request("POST", path, **kwargs)

    def put(self, path: str, **kwargs):
        return self.request("PUT", path, **kwargs)

    def patch(self, path: str, **kwargs):
        return self.request("PATCH", path, **kwargs)

    def delete(self, path: str, **kwargs):
        return self.request("DELETE", path, **kwargs)
