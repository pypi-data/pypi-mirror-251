import fire
from colab_easy_ui.ColabEasyUI import ColabEasyUI, JsonApiFunc


def get_info():
    from fastapi.encoders import jsonable_encoder
    from fastapi.responses import JSONResponse

    try:
        data = {
            "status": "ok",
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
    c.enable_file_uploader("upload", {"abc": "voice.zip"})
    c.enable_colab_internal_fetcher()
    tb_port = c.colabInternalFetcher.start_tensorboard("trainer/amitaro/logs", "TB_LOG")
    print("Tensorflow port:::", tb_port)

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
