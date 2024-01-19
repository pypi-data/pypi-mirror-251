import zipfile
import os
from typing import Callable, Dict


def unzip_function(_callback: Callable[[str, Dict[str, Dict[str, int | str]]], None], zip_path: str, extract_to: str):
    progresses: Dict[str, Dict[str, int | str]] = {}

    os.makedirs(extract_to, exist_ok=True)
    progresses["unzip"] = {
        "display_name": "Unzip",
        "n": 0,
        "total": 0,
        "status": "RUNNING",
    }

    # ZIPファイルを開く
    with zipfile.ZipFile(zip_path, "r") as zip_ref:
        # 解凍するファイルリストを取得
        file_list = zip_ref.namelist()
        # ファイルの総数を取得し、進捗バーの最大値として設定
        total_files = len(file_list)
        # tqdmを使用して進捗表示を行う
        for i, file in enumerate(file_list):
            # ファイルを解凍
            zip_ref.extract(file, extract_to)
            print(f"unzip:: {i},{total_files}")
            progresses["unzip"]["n"] = i
            progresses["unzip"]["total"] = total_files
            progresses["unzip"]["status"] = "RUNNING"
            _callback("RUNNING", progresses)

        progresses["unzip"]["status"] = "DONE"
        _callback("DONE", progresses)
