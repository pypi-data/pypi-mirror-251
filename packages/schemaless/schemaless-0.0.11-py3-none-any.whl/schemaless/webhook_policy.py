import enum
import typing

import pydantic

import schemaless.bases
import schemaless.config
import schemaless.http_client
import schemaless.delta
import schemaless.utils
import schemaless.rid


class PolicyTypeEnum(str, enum.Enum):
    JsonAta = "JsonAta"


class WebhookPolicyModel(pydantic.BaseModel):
    rid: schemaless.rid.RID
    policy_type: PolicyTypeEnum
    expression: str
    lifecycle: schemaless.utils.Lifecycle
    model_config = pydantic.ConfigDict(use_enum_values=True)

    @classmethod
    def from_api_response(cls, response: dict) -> "WebhookPolicyModel":
        return cls(
            **response,
        )


class BodyAddWebhookPolicy(pydantic.BaseModel):
    id: str
    policy_type: PolicyTypeEnum
    expression: str
    model_config = pydantic.ConfigDict(use_enum_values=True)


class WebhookPolicy(schemaless.bases.Handler):
    def __init__(self, http_client: schemaless.bases.BaseHTTP):
        self.http_client = http_client

    @classmethod
    def from_config(cls, config: schemaless.config.Config) -> "WebhookPolicy":
        return cls(
            http_client=schemaless.http_client.HTTP.from_config(config),
        )

    async def add(self, webhook_policy: BodyAddWebhookPolicy) -> WebhookPolicyModel:
        response = await self.http_client.post(
            url="/api/v1/webhook/policy/add",
            json=webhook_policy.model_dump(),
        )

        return response.parse_to_model(WebhookPolicyModel)

    def load_all(self):
        pass
