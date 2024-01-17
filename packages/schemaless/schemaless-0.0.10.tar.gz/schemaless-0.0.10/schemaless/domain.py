import typing
import datetime

import pydantic

import schemaless.config
import schemaless.http_client
import schemaless.bases
import schemaless.rid
import schemaless.utils

DOMAIN_BASE_PATH = "/api/v1/domain"


class DomainModel(pydantic.BaseModel):
    rid: schemaless.rid.RID
    name: str
    description: str
    json_schema: typing.Union[typing.Dict[str, typing.Any], None] = None
    lifecycle: schemaless.utils.Lifecycle

    @classmethod
    def from_api_response(cls, response: dict) -> "DomainModel":
        return cls(
            **response,
        )


class CreateDomainBody(pydantic.BaseModel):
    rid: typing.Union[str, None] = None
    name: str
    description: str
    json_schema: typing.Union[typing.Dict[str, typing.Any], None] = None


class Domain(schemaless.bases.Handler):
    def __init__(self, http_client: schemaless.bases.BaseHTTP):
        self.http_client = http_client

    @classmethod
    def from_config(cls, config: schemaless.config.Config) -> "Domain":
        return cls(
            http_client=schemaless.http_client.HTTP.from_config(config),
        )

    async def create(self, domain: CreateDomainBody) -> DomainModel:
        response = await self.http_client.post(
            url=DOMAIN_BASE_PATH + "/add",
            json=domain.model_dump(),
        )

        return response.parse_to_model(DomainModel)

    def search(self):
        pass

    def get(self):
        pass

    def list(self):
        pass

    def delete(self):
        pass

    def update(self):
        pass
