from dataclasses import dataclass
from typing import TypeAlias, Literal

from typing import Dict

# from typing import Union, Dict

RESPONSE_STATUS: TypeAlias = Literal[
    "OK",
    "NG",
]


@dataclass
class Response:
    status: RESPONSE_STATUS
    message: str


@dataclass
class JsonApiFuncInfo:
    id: str
    display_name: str
    method: str
    path: str


@dataclass
class FunctionInfoResponse(Response):
    functions: list[JsonApiFuncInfo]


@dataclass
class GetFunctionTaskStatusResponse(Response):
    task_id: str
    task_status: str
    task_status_data: str


# @dataclass
# class ColabInternalFetchResponse(Response):
#     url: str
#     data: Dict[str, Union[str, int, float]] | None


@dataclass
class EasyFileUploaderResponse(Response):
    allowed_filenames: Dict[str, str] | None = None
