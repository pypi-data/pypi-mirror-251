from fastapi import APIRouter
from typing import Callable, Dict, Any
from fastapi import Response
from dataclasses import dataclass

from colab_easy_ui.data.Response import FunctionInfoResponse, JsonApiFuncInfo


@dataclass
class JsonApiFunc:
    id: str
    display_name: str
    method: str
    path: str
    func: Callable[[Dict[str, Any]], Dict[str, Any]]


class Functions:
    def register_functions(self, funcs: list[JsonApiFunc]):
        self.functions = funcs

        router = APIRouter()
        for func in funcs:
            router.add_api_route(func.path, func.func, methods=[func.method])
        router.add_api_route("/functions", self.get_function_info, methods=["GET"])

        self.router = router

    def get_function_info(self):
        from fastapi.encoders import jsonable_encoder
        from fastapi.responses import JSONResponse

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
