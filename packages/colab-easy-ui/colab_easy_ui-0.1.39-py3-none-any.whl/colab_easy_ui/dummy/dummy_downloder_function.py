from typing import Callable, Dict


def download_weights(_callback: Callable[[str, Dict[str, Dict[str, int | str]]], None] | None = None):
    # def callback(param):
    #     print("Callback...", param)

    progresses: Dict[str, Dict[str, int | str | str]] = {}

    def callback(url: str, display_name: str, n: int, total: int, status: str):
        if url not in progresses:
            progresses[url] = {"display_name": display_name, "n": 0, "total": 0, "status": "RUNNING"}

        if n != -1:
            progresses[url]["n"] = n
        if total != -1:
            progresses[url]["total"] = total

        progresses[url]["display_name"] = display_name
        progresses[url]["status"] = status
        print(progresses)
        all_valid = all(progress["status"] == "VALID" for progress in progresses.values())
        if all_valid:
            global_status = "DONE"  # 全て"valid"ならグローバルステータスを"DONE"に更新
        else:
            global_status = "RUNNING"  # そうでなければ、"RUNNING"を保持する

        if _callback is not None:
            _callback(global_status, progresses)

        # print(progresses)

    for i in range(10):
        import time

        time.sleep(0.3)
        callback("http://dummy.co/1", "DN1", i, 10, "RUNNING")

        time.sleep(0.3)
        callback("http://dummy.co/2", "DN2", i, 10, "RUNNING")

    callback("http://dummy.co/2", "DN2", i, 10, "VALID")
    callback("http://dummy.co/1", "DN1", i, 10, "VALID")
