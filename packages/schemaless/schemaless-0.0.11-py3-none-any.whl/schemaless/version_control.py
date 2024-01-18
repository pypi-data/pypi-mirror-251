import typing

import pydantic

import schemaless.bases
import schemaless.config
import schemaless.http_client
import schemaless.delta
import schemaless.rid
import schemaless.utils


class PathHistoryItem(pydantic.BaseModel):
    delta: schemaless.delta.DeltaModel
    lifecycle: schemaless.utils.Lifecycle


class PathHistoryResponse(pydantic.BaseModel):
    history: typing.List[PathHistoryItem]


class SubmitObjectBody(pydantic.BaseModel):
    domain_rid: schemaless.rid.RID
    entity_rid: schemaless.rid.RID
    object: dict[str, typing.Any]


class DeltaListResponse(pydantic.BaseModel):
    delta: typing.List[schemaless.delta.DeltaModel]


class SubmitDeltaItem(pydantic.BaseModel):
    operation: schemaless.delta.Operation
    path: str
    old_value: typing.Union[typing.Any, None] = None
    new_value: typing.Union[typing.Any, None] = None

    @pydantic.field_serializer("operation")
    def serialize_operation(self, operation: schemaless.delta.Operation) -> str:
        return operation.value


class SubmitDeltaBody(pydantic.BaseModel):
    domain_rid: schemaless.rid.RID
    entity_rid: schemaless.rid.RID
    deltas: typing.List[SubmitDeltaItem]


class VersionControl(schemaless.bases.Handler):
    def __init__(self, http_client: schemaless.bases.BaseHTTP):
        self.http_client = http_client

    @classmethod
    def from_config(cls, config: schemaless.config.Config) -> "VersionControl":
        return cls(
            http_client=schemaless.http_client.HTTP.from_config(config),
        )

    async def submit_object(
        self,
        domain_rid: schemaless.rid.RID,
        entity_rid: schemaless.rid.RID,
        obj: dict[str, typing.Any],
    ) -> DeltaListResponse:
        response = await self.http_client.post(
            url="/api/v1/vc/object/submit",
            json=SubmitObjectBody(
                domain_rid=domain_rid,
                entity_rid=entity_rid,
                object=obj,
            ).model_dump(),
        )

        return response.parse_to_model(DeltaListResponse)

    async def get_snapshot(
        self,
        domain_rid: schemaless.rid.RID,
        entity_rid: schemaless.rid.RID,
        model: typing.Optional[typing.Type[schemaless.bases.T]] = None,
    ) -> typing.Union[typing.Dict[str, typing.Any], typing.Type[schemaless.bases.T]]:
        response = await self.http_client.get(
            url="/api/v1/vc/object/snapshot",
            params={
                "domain_rid": domain_rid.to_string(),
                "entity_rid": entity_rid.to_string(),
            },
        )

        if model is None:
            return response.data()

        return response.parse_to_model(model)

    async def get_history_of_path(
        self,
        domain_rid: schemaless.rid.RID,
        entity_rid: schemaless.rid.RID,
        path: str,
    ) -> PathHistoryResponse:
        response = await self.http_client.get(
            url="/api/v1/vc/history/path",
            params={
                "domain_rid": domain_rid.to_string(),
                "entity_rid": entity_rid.to_string(),
                "path": path,
            },
        )
        return response.parse_to_model(PathHistoryResponse)

    async def patch_object(
        self,
        domain_rid: schemaless.rid.RID,
        entity_rid: schemaless.rid.RID,
        deltas: typing.List[SubmitDeltaItem],
        model: typing.Optional[typing.Type[schemaless.bases.T]] = None,
    ) -> typing.Union[typing.Dict[str, typing.Any], typing.Type[schemaless.bases.T]]:
        body = SubmitDeltaBody(
            domain_rid=domain_rid,
            entity_rid=entity_rid,
            deltas=deltas,
        ).model_dump()
        response = await self.http_client.post(
            url="/api/v1/vc/object/object/patch",
            json=body,
        )

        if model is None:
            return response.data()

        return response.parse_to_model(model)

    async def patch_object_with_dict(
        self,
        domain_rid: schemaless.rid.RID,
        entity_rid: schemaless.rid.RID,
        input_dict: dict[str, typing.Any],
        operation: schemaless.delta.Operation = schemaless.delta.Operation.CHANGE,
        model: typing.Optional[typing.Type[schemaless.bases.T]] = None,
    ) -> typing.Union[typing.Dict[str, typing.Any], typing.Type[schemaless.bases.T]]:
        deltas = []
        for path, value in schemaless.utils.generate_json_paths_and_values(
            data=input_dict,
        ).items():
            deltas.append(
                SubmitDeltaItem(
                    operation=operation,
                    path=path,
                    old_value=None,
                    new_value=value,
                ),
            )

        return await self.patch_object(
            domain_rid=domain_rid, entity_rid=entity_rid, deltas=deltas, model=model
        )
