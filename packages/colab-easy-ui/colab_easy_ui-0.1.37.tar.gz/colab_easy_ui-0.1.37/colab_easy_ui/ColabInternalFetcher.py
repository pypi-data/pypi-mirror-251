import portpicker
from fastapi.responses import Response
import requests
from tensorboard import notebook


class ColabInternalFetcher:
    tb_port = 0

    def start_tensorboard_colab(self, ipython, tb_logs_dir, logfile=None):
        tb_port = portpicker.pick_unused_port()
        if logfile is not None:
            ipython.system_raw(f"tensorboard --port {tb_port} --logdir {tb_logs_dir} >{logfile} 2>&1 &")
        else:
            ipython.system_raw(f"tensorboard --port {tb_port} --logdir {tb_logs_dir} &")
        self.tb_port = tb_port
        return tb_port

    def start_tensorboard(self, tb_logs_dir, logfile=None):
        tb_port = portpicker.pick_unused_port()
        notebook.start(f"--port {tb_port} --logdir {tb_logs_dir}")
        self.tb_port = tb_port
        return tb_port

    def _fetch(self, url):
        response = requests.get(url)
        content_type = response.headers.get("Content-Type")
        return Response(content=response.content, media_type=content_type)
        # try:
        #     response = requests.get(url)
        #     if response.status_code == 200:
        #         content_type = response.headers.get("Content-Type")
        #         print(content_type)
        #         if "application/json" in content_type:
        #             data = response.json()
        #         else:
        #             # レスポンスがバイナリデータの場合
        #             base64_encoded_data = base64.b64encode(response.content)
        #             data = base64_encoded_data.decode("utf-8")  # Base64文字列にする

        #         response = ColabInternalFetchResponse(
        #             status="OK",
        #             url=url,
        #             message="",
        #             data=data,
        #         )
        #     else:
        #         response = ColabInternalFetchResponse(
        #             status="NG",
        #             url=url,
        #             message=f"http response code is not 200, {response.status_code}.",
        #             data=None,
        #         )
        # except requests.exceptions.RequestException as e:
        #     response = ColabInternalFetchResponse(
        #         status="NG",
        #         url=url,
        #         message=f"Exception, {e}.",
        #         data=None,
        #     )

        # json_compatible_item_data = jsonable_encoder(response)
        # return JSONResponse(content=json_compatible_item_data)

    def get_runs(self):
        url = f"http://localhost:{self.tb_port}/data/runs"
        return self._fetch(url)

    def get_scalars_tags(self):
        url = f"http://localhost:{self.tb_port}/data/plugin/scalars/tags"
        return self._fetch(url)

    def get_scalars_scalars(self, run: str, tag: str):
        url = f"http://localhost:{self.tb_port}/data/plugin/scalars/scalars?run={run}&tag={tag}"
        return self._fetch(url)

    def get_images_tags(self):
        url = f"http://localhost:{self.tb_port}/data/plugin/images/tags"
        return self._fetch(url)

    def get_images_images(self, run: str, tag: str, sample: int):
        url = f"http://localhost:{self.tb_port}/data/plugin/images/images?run={run}&tag={tag}&sample={sample}"
        return self._fetch(url)

    def get_images_individualImage(self, blob_key: str):
        url = f"http://localhost:{self.tb_port}/data/plugin/images/individualImage?blob_key={blob_key}"
        return self._fetch(url)

    def get_audio_tags(self):
        url = f"http://localhost:{self.tb_port}/data/plugin/audio/tags"
        return self._fetch(url)

    def get_audio_audio(self, run: str, tag: str, sample: int):
        url = f"http://localhost:{self.tb_port}/data/plugin/audio/audio?run={run}&tag={tag}&sample={sample}"
        return self._fetch(url)

    def get_audio_individualAudio(self, blob_key: str):
        url = f"http://localhost:{self.tb_port}/data/plugin/audio/individualAudio?blob_key={blob_key}"
        return self._fetch(url)
