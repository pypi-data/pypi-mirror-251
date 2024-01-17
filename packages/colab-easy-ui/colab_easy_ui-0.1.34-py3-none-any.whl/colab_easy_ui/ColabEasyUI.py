from dataclasses import dataclass
import os
from typing import Callable, Dict, Any
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi import HTTPException
from fastapi import Request
from fastapi import Response
from fastapi.routing import APIRoute
from fastapi.exceptions import RequestValidationError
from fastapi.staticfiles import StaticFiles

from colab_easy_ui.EasyFileUploaderInternal import EasyFileUploader
import uvicorn
import threading
import nest_asyncio
import portpicker
from colab_easy_ui.ColabInternalFetcher import ColabInternalFetcher
from colab_easy_ui.data.Response import FunctionInfoResponse, JsonApiFuncInfo


class ValidationErrorLoggingRoute(APIRoute):
    def get_route_handler(self) -> Callable:
        original_route_handler = super().get_route_handler()

        async def custom_route_handler(request: Request) -> Response:
            try:
                return await original_route_handler(request)
            except RequestValidationError as exc:  # type: ignore
                print("Exception", request.url, str(exc))
                body = await request.body()
                detail = {"errors": exc.errors(), "body": body.decode()}
                raise HTTPException(status_code=422, detail=detail)

        return custom_route_handler


@dataclass
class JsonApiFunc:
    id: str
    display_name: str
    method: str
    path: str
    func: Callable[[Dict[str, Any]], Dict[str, Any]]


class ColabEasyUI(FastAPI):
    _instance = None

    @classmethod
    def get_instance(
        cls,
    ):
        if cls._instance is None:
            app_fastapi = ColabEasyUI()

            app_fastapi.mount(
                "/front",
                StaticFiles(directory=f"{os.path.dirname(__file__)}/front/dist", html=True),
                name="static",
            )

            cls._instance = app_fastapi
            return cls._instance

        return cls._instance

    def __init__(self):
        super().__init__()
        self.router.route_class = ValidationErrorLoggingRoute
        self.add_middleware(
            CORSMiddleware,
            allow_origins=["*"],
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )

    def _run_server(self, port: int):
        uvicorn.run(self, host="127.0.0.1", port=port, log_level="info")

    def start(self):
        nest_asyncio.apply()
        port = portpicker.pick_unused_port()
        server_thread = threading.Thread(target=self._run_server, args=(port,))
        server_thread.start()
        return port

    def mount_static_folder(self, path: str, real_path: str):
        self.mount(
            path,
            StaticFiles(directory=real_path, html=True),
            name="static",
        )

    def enable_file_uploader(self, upload_dir: str, allowed_files: dict[str, str] | None = None):
        self.fileUploader = EasyFileUploader(upload_dir)
        self.fileUploader.set_allowed_filenames(allowed_files)
        self.include_router(self.fileUploader.router)

    def register_functions(self, funcs: list[JsonApiFunc]):
        from fastapi import APIRouter

        self.functions = funcs

        router = APIRouter()
        for func in funcs:
            router.add_api_route(func.path, func.func, methods=[func.method])
        router.add_api_route("/functions", self.get_function_info, methods=["GET"])

        self.include_router(router)

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

    def enable_colab_internal_fetcher(
        self,
    ):
        from fastapi import APIRouter

        self.colabInternalFetcher = ColabInternalFetcher()
        router = APIRouter()
        router.add_api_route("/runs", self.colabInternalFetcher.get_runs, methods=["GET"])
        router.add_api_route("/scalars_tags", self.colabInternalFetcher.get_scalars_tags, methods=["GET"])
        router.add_api_route("/scalars_scalars", self.colabInternalFetcher.get_scalars_scalars, methods=["GET"])
        router.add_api_route("/images_tags", self.colabInternalFetcher.get_images_tags, methods=["GET"])
        router.add_api_route("/images_images", self.colabInternalFetcher.get_images_images, methods=["GET"])
        router.add_api_route("/images_individualImage", self.colabInternalFetcher.get_images_individualImage, methods=["GET"])
        router.add_api_route("/audio_tags", self.colabInternalFetcher.get_audio_tags, methods=["GET"])
        router.add_api_route("/audio_audio", self.colabInternalFetcher.get_audio_audio, methods=["GET"])
        router.add_api_route("/audio_individualAudio", self.colabInternalFetcher.get_audio_individualAudio, methods=["GET"])
        self.include_router(router)
