import dataclasses
import typing
import uuid

import pydantic


def id_generator() -> str:
    return str(uuid.uuid4())


class RID(pydantic.BaseModel):
    namespace: str
    domain: str
    id: typing.Optional[str] = pydantic.Field(default_factory=id_generator)

    def to_string(self) -> str:
        return f"{self.namespace}:{self.domain}:{self.id}"
