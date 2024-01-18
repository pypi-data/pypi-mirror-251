import abc
import typing

import schemaless.config


class Handler(abc.ABC):
    @classmethod
    @abc.abstractmethod
    def from_config(cls, config: schemaless.config.Config) -> "Handler":
        ...


T = typing.TypeVar("T")


class BaseHTTPResponse(abc.ABC):
    @abc.abstractmethod
    def parse_to_model(self, model: typing.Type[T]) -> T:
        ...

    @abc.abstractmethod
    def data(self) -> typing.Dict[str, typing.Any]:
        ...


class BaseHTTP(abc.ABC):
    @classmethod
    @abc.abstractmethod
    def from_config(cls, config: schemaless.config.Config) -> "BaseHTTP":
        ...

    @abc.abstractmethod
    async def _create_response(self, method: str, **kwargs) -> BaseHTTPResponse:
        ...

    @abc.abstractmethod
    async def get(self, url: str, params: dict = None) -> BaseHTTPResponse:
        ...

    @abc.abstractmethod
    async def post(self, url: str, json: dict = None) -> BaseHTTPResponse:
        ...

    @abc.abstractmethod
    async def put(self, url: str, json: dict = None) -> BaseHTTPResponse:
        ...

    @abc.abstractmethod
    async def delete(self, url: str) -> BaseHTTPResponse:
        ...
