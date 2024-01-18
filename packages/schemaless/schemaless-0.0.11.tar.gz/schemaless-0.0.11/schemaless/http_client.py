import enum
import typing

import httpx

import pydantic
import schemaless.bases
import schemaless.config

API_KEY_KEY = "X-API-Key"


class HTTPResponse(schemaless.bases.BaseHTTPResponse):
    def __init__(self, status_code: int, headers=None, json=None):
        self.status_code = status_code
        self.headers = headers
        self.json = json

    @classmethod
    def from_httpx_response(cls, response: httpx.Response) -> "HTTPResponse":
        return cls(
            status_code=response.status_code,
            headers=response.headers,
            json=response.json(),
        )

    def parse_to_schemaless_model(self) -> "SchemalessHTTPResponseModel":
        if not self.json:
            raise ValueError("Response does not contain json")

        return SchemalessHTTPResponseModel(**self.json)

    def parse_to_model(
        self, model: typing.Type[schemaless.bases.T]
    ) -> schemaless.bases.T:
        schemaless_response = self.parse_to_schemaless_model()
        if schemaless_response.status == Status.Success:
            if isinstance(schemaless_response.data, list):
                return model.validate_python(schemaless_response.data)
            return model(**schemaless_response.data)
        elif schemaless_response.status == Status.Error:
            raise SchemalessException(schemaless_response.data)

        raise ValueError("Response does not contain json")

    def data(self) -> typing.Dict[str, typing.Any]:
        return self.parse_to_schemaless_model().data


class Status(str, enum.Enum):
    Success = "Success"
    Error = "Error"
    Fail = "Fail"


class SchemalessHTTPResponseModel(pydantic.BaseModel):
    status: Status
    data: typing.Any


class SchemalessException(Exception):
    pass


class HTTP(schemaless.bases.BaseHTTP):
    def __init__(self, base_url: str, api_key: str):
        super().__init__()
        self.api_key = api_key
        self.http_client = httpx.AsyncClient(base_url=base_url)

    @classmethod
    def from_config(cls, config: schemaless.config.Config) -> "HTTP":
        return cls(
            base_url=config.get_base_url(),
            api_key=config.get_api_key(),
        )

    async def _create_response(self, method: str, **kwargs) -> HTTPResponse:
        response = await getattr(self.http_client, method)(**kwargs)
        return HTTPResponse.from_httpx_response(response)

    async def get(self, url: str, params: dict = None) -> HTTPResponse:
        return await self._create_response(
            "get",
            url=url,
            params=params,
            headers={API_KEY_KEY: self.api_key},
        )

    async def post(self, url: str, json: dict = None) -> HTTPResponse:
        return await self._create_response(
            "post",
            url=url,
            json=json,
            headers={API_KEY_KEY: self.api_key},
        )

    async def put(self, url: str, json: dict = None) -> HTTPResponse:
        return await self._create_response(
            "put",
            url=url,
            json=json,
            headers={API_KEY_KEY: self.api_key},
        )

    async def delete(self, url: str) -> HTTPResponse:
        return await self._create_response(
            "delete",
            url=url,
            headers={API_KEY_KEY: self.api_key},
        )
