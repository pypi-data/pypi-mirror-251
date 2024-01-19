import fire
from colab_easy_ui.ColabEasyUI import ColabEasyUI, JsonApiFunc
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
import uuid
import requests
import threading

from colab_easy_ui.dummy.dummy_downloder_function import download_weights
import functools

from colab_easy_ui.dummy.dummy_unzip_function import unzip_function


def downloader_callback(status: str, message: str, port: int, uuid_str: str):
    import json

    data = json.dumps(message)
    requests.get(f"http://localhost:{port}/functions_set_task_status?task_id={uuid_str}&status={status}&data={data}")


def dummy_downloader_function(port: int, uuid_str: str):
    downloader_callback_fixed = functools.partial(downloader_callback, port=port, uuid_str=uuid_str)
    download_weights(downloader_callback_fixed)


def download(port: int):
    # UUIDを作成
    uuid_str = str(uuid.uuid4())

    server_thread = threading.Thread(target=dummy_downloader_function, args=(port, uuid_str))
    server_thread.start()

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


def unzip_callback(status: str, message: str, port: int, uuid_str: str):
    import json

    data = json.dumps(message)
    requests.get(f"http://localhost:{port}/functions_set_task_status?task_id={uuid_str}&status={status}&data={data}")


def dummy_unzip_function(port: int, uuid_str: str):
    unzip_callback_fixed = functools.partial(unzip_callback, port=port, uuid_str=uuid_str)
    unzip_function(unzip_callback_fixed, "upload/voice.zip", "raw_data")


def unzip(port: int):
    # UUIDを作成
    uuid_str = str(uuid.uuid4())

    server_thread = threading.Thread(target=dummy_unzip_function, args=(port, uuid_str))
    server_thread.start()

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


def run_server():
    c = ColabEasyUI.get_instance()
    port = c.port
    c.enable_file_uploader("upload", {"abc": "voice.zip"})
    c.enable_colab_internal_fetcher()
    tb_port = c.colabInternalFetcher.start_tensorboard("trainer/amitaro/logs", "TB_LOG")
    print("Tensorflow port:::", tb_port)

    c.register_functions(
        [
            JsonApiFunc("downloader_id", "progress", "downloader_name", "GET", "/downloader", functools.partial(download, port=port)),
            JsonApiFunc("unzip_id", "progress", "unzip_name", "GET", "/unzip", functools.partial(unzip, port=port)),
        ]
    )
    c.mount_static_folder("/front2", "frontend/dist")
    port = c.start()
    print(port)


def main():
    fire.Fire(run_server)
