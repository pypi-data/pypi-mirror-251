from typing import Dict
import fire
from colab_easy_ui.ColabEasyUI import ColabEasyUI, JsonApiFunc
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
import uuid
import requests
import asyncio


def run_server():
    c = ColabEasyUI.get_instance()
    port = c.port
    c.enable_file_uploader("upload", {"abc": "voice.zip"})
    c.enable_colab_internal_fetcher()
    tb_port = c.colabInternalFetcher.start_tensorboard("trainer/amitaro/logs", "TB_LOG")
    print("Tensorflow port:::", tb_port)

    def get_info():
        # UUIDを作成
        uuid_str = str(uuid.uuid4())

        def callback(message):
            import json

            data = json.dumps(message)
            response = requests.get(f"http://localhost:{port}/functions_set_task_status?task_id={uuid_str}&status=running---&data={data}")

        async def dummy_exec():
            import time

            progresses: Dict[str, Dict[int, int, str]] = {}
            for i in range(10):
                time.sleep(1)
                url = "dummy_url"
                progresses[url] = {"display_name": "task_1", "progress": 0.1 * i, "n": 0, "total": 0, "status": "RUNNING"}
                callback({"message": f"message{i}"})

        # httpのgetを"http://localhost:8000/test"に対して実行
        dummy_exec()

        try:
            data = {
                "status": "ok",
                "uuid": uuid_str,
                "description": "easy-file-uploader-py created by wok!",
            }

            json_compatible_item_data = jsonable_encoder(data)
            return JSONResponse(content=json_compatible_item_data)
        except Exception as e:
            data = {
                "status": "error",
                "message": str(e),
                "description": "easy-file-uploader-py created by wok!",
            }
            print(data)
            return JSONResponse(content=json_compatible_item_data)

    c.register_functions(
        [
            JsonApiFunc("idid1", "function1", "GET", "/test", get_info),
            JsonApiFunc("idid2", "function2", "POST", "/test2", get_info),
        ]
    )
    c.mount_static_folder("/front2", "frontend/dist")
    port = c.start()
    print(port)


def main():
    fire.Fire(run_server)
