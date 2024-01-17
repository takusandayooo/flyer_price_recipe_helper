import shutil

import requests
from gdown import download


def get_resipe():
    # 変更不要
    API_url = "APIのURLを入力してください"
    # スクレイピングをした後の画像が保存されている場所。
    params = {"fileID": "フォルダーIDを入力してください"}
    jsons = requests.get(API_url, params)
    print(jsons.json())
    extract_dir = "./photo"
    File_ID = jsons.json()["text"]["ID"]
    Zip_url = "https://drive.google.com/uc?export=download&id={}".format(File_ID)

    try:
        shutil.rmtree("dir_out")
        shutil.rmtree("test.zip")
    except:
        pass

    download(
        Zip_url,
        "test.zip",
        quiet=False,
    )
    shutil.unpack_archive("test.zip", "dir_out")


if __name__ == "__main__":
    get_resipe()
