import enum
import typing

import pydantic

"""
#[derive(Debug, PartialEq, Clone, Serialize, Deserialize)]
pub enum Operation {
    Add,
    Change,
    Delete,
}
"""


class Operation(enum.Enum):
    ADD = "Add"
    CHANGE = "Change"
    DELETE = "Delete"


class DeltaModel(pydantic.BaseModel):
    operation: Operation
    path: str
    old_value: typing.Union[typing.Any, None] = None
    new_value: typing.Union[typing.Any, None] = None
    hash: str

    @classmethod
    def from_api_response(cls, response: dict) -> "DeltaModel":
        return cls(
            **response,
        )
