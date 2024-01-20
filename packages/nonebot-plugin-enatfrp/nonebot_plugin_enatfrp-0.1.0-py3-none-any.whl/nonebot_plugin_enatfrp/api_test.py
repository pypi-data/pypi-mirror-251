from json import loads
from typing import TYPE_CHECKING, Protocol, Any, Literal, Tuple
from pathlib import PurePosixPath
from functools import partial
from urllib.parse import urlparse, urlunparse

from nonebot import get_driver

from nonebot.internal.driver import HTTPClientMixin, Request

if TYPE_CHECKING:
    class _ApiCall(Protocol):
        async def __call__(self, **data: Any) -> Any:
            ...

driver = get_driver()  # type:ignore

assert isinstance(driver, HTTPClientMixin), "必须使用支持http请求的驱动器。"

driver: HTTPClientMixin


class API:
    def __init__(self, api: str, token: str):
        self.api = api
        self.headers = {"Authorization": f"Bearer {token}"}

    def get_api(self, path: str) -> str:
        u = urlparse(self.api)
        return urlunparse(u._replace(path=(PurePosixPath(u.path) / path).as_posix()))  # type:ignore

    async def call_api(
            self,
            path: str, method: Literal["GET", "PUT", "POST", "DELETE", "OPTIONS", "HEAD", "PATCH", "TRACE"], **data: Any
    ) -> Tuple[int, Any]:
        resp = await driver.request(Request(
            method, self.get_api(path),
            headers=self.headers,
            **({"params": data} if method == "GET" else {"json": data})
        ))
        return resp.status_code, loads(resp.content)

    def __getattr__(self, name: str) -> "_ApiCall":
        if (name.startswith("__") and name.endswith("__")) or len(_ := name.split("_", 1)) != 2:
            raise AttributeError(
                f"'{self.__class__.__name__}' object has no attribute '{name}'"
            )
        return partial(self.call_api, _[1], _[0].upper())



__all__ = ["API"]
