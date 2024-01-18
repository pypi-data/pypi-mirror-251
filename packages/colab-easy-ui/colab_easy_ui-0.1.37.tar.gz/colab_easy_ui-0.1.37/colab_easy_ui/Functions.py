from fastapi import APIRouter
from typing import Callable, Dict, Any
from fastapi import Response
from dataclasses import dataclass

from colab_easy_ui.data.Response import FunctionInfoResponse, FunctionTaskStatusResponse, JsonApiFuncInfo

from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse


@dataclass
class JsonApiFunc:
    id: str
    display_name: str
    method: str
    path: str
    func: Callable[[Dict[str, Any]], Dict[str, Any]]


class Functions:
    def __init__(self):
        self.status_store = {}

    def register_functions(self, funcs: list[JsonApiFunc]):
        self.functions = funcs

        router = APIRouter()
        for func in funcs:
            router.add_api_route(func.path, func.func, methods=[func.method])
        router.add_api_route("/functions", self.get_function_info, methods=["GET"])
        router.add_api_route("/functions_set_task_status", self.set_task_status, methods=["GET"])
        router.add_api_route("/functions_del_task_status", self.del_task_status, methods=["GET"])
        router.add_api_route("/functions_get_task_status", self.get_task_status, methods=["GET"])

        self.router = router

    def set_task_status(self, task_id: str, status: str, data: str):
        self.status_store[task_id] = {"status": status, "data": data}
        print(self.status_store)

    def del_task_status(self, task_id: str):
        del self.status_store[task_id]

    def get_task_status(self, task_id: str):
        data = FunctionTaskStatusResponse(
            status="OK",
            message="",
            task_id=task_id,
            task_status=self.status_store[task_id]["status"] if hasattr(self.status_store, task_id) else "not found",
            task_status_data=self.status_store[task_id]["data"],
        )
        json_compatible_item_data = jsonable_encoder(data)
        return JSONResponse(content=json_compatible_item_data)

    def get_function_info(self):
        if self.functions is None:
            data = Response(
                status="error",
                message="No functions registered.",
            )
            return JSONResponse(content=jsonable_encoder(data))

        functions: list[JsonApiFuncInfo] = []
        for f in self.functions:
            f_info = JsonApiFuncInfo(
                id=f.id,
                display_name=f.display_name,
                method=f.method,
                path=f.path,
            )
            functions.append(f_info)

        data = FunctionInfoResponse(
            status="ok",
            message="",
            functions=functions,
        )

        json_compatible_item_data = jsonable_encoder(data)
        return JSONResponse(content=json_compatible_item_data)
