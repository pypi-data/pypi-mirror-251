import typing
import pydantic

import schemaless.rid
import schemaless.bases
import schemaless.config
import schemaless.http_client
import schemaless.delta
import schemaless.utils


class Relations(pydantic.BaseModel):
    domain_rid: schemaless.rid.RID
    entity_rid: schemaless.rid.RID


class CommitModel(pydantic.BaseModel):
    rid: schemaless.rid.RID
    relations: Relations
    deltas: typing.List[schemaless.delta.DeltaModel]
    branch: str
    parents: typing.Union[typing.List[schemaless.rid.RID], None] = None
    hash: str
    lifecycle: schemaless.utils.Lifecycle

    model_config = pydantic.ConfigDict(use_enum_values=True)

    @classmethod
    def from_api_response(cls, response: dict) -> "CommitModel":
        return cls(
            **response,
        )


class Domain(schemaless.bases.Handler):
    def __init__(self, http_client: schemaless.bases.BaseHTTP):
        self.http_client = http_client

    @classmethod
    def from_config(cls, config: schemaless.config.Config) -> "Domain":
        return cls(
            http_client=schemaless.http_client.HTTP.from_config(config),
        )
