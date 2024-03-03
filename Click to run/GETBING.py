# GETBING
import sys
import os
from traceback import print_exc
import yaml
import re
import requests
import json
import shutil
import time
from PIL import Image
from PIL.Image import Image as ImageType
import numpy as np


def read_config(yaml_path):
    try:
        with open(yaml_path, "r", encoding="utf-8") as config_file:
            data = yaml.load(config_file, Loader=yaml.SafeLoader)
            return data
    except:
        input(print_exc())
        exit()


def get_response(url, headers):
    try:
        response = requests.get(url=url, headers=headers)
        response.raise_for_status()
        return response
    except requests.exceptions.RequestException as e:
        raise Exception(f"Request failed: {str(e)}")


def checkDir(path):
    if not os.path.exists(path):
        print(f"不存在:{path}")
        os.makedirs(path)
        print(f"已创建:{path}")


def main():
    try:
        os.system("chcp 65001 >nul")
        os.chdir(sys.path[0])
        data = read_config(".\\config.yaml")

        UA = {'user-agent': data["net"]["user_agent"]}
        resolution = "UHD"
        download_path = data["file"]["temp"]
        static_path = data["file"]["storage"]

        checkDir(download_path)
        checkDir(static_path)

        getFileList(static_path)
        existed_list = getFileList(download_path, False)
        print(f"正在向必应查询图片列表")
        response_json_zh = dict(json.loads(
            get_response(url=request_url,headers=UA).text
        ))
        response_json = {**response_json_zh}

        for serial in range(0, 7):
            pic_url_base = (response_json['images'][serial]['urlbase'])
            # URLBASE: '/th?id=OHR.{NAME}_ZH-CN{NUMBERS}'
            pattern = r"(.[A-Za-z]+_)"
            pic_name = str(re.findall(pattern, pic_url_base)[0]).strip("._")

            url = f"http://www.bing.com{pic_url_base}_{resolution}.jpg"
            pic_save_path = f"{download_path}\\{pic_name}.jpg"
            if pic_name in existed_list:
                print(f"已下载：{pic_name}")
            else:
                print(f"正在下载：{pic_name}")
                saveImg(url, pic_save_path)
        adjustAndCopy(copyFrom=download_path, copyTo=static_path)
        print("全部完成!")
        time.sleep(3)
    except Exception:
        input(print_exc())


def saveImg(imgUrl, saveAs):
    try:
        pic = requests.get(imgUrl).content
        with open(saveAs, 'wb') as picture:
            picture.write(pic)
        return 1
    except Exception:
        print("Failed to save image!")
        print_exc()
        return 0


def getFileList(folder_path: str, flag=True) -> list:
    if not os.path.exists(folder_path):
        return []

    file_list = os.listdir(folder_path)
    if flag:
        return file_list
    else:
        return [os.path.splitext(file_name)[0] for file_name in file_list]


def adjustAndCopy(copyFrom, copyTo):
    copyFrom = os.path.abspath(copyFrom)
    copyTo = os.path.abspath(copyTo)
    if not os.path.exists(copyFrom):
        os.makedirs(copyFrom)
    if not os.path.exists(copyTo):
        os.makedirs(copyTo)
    file_list_fr = getFileList(copyFrom)
    file_list_to = getFileList(copyTo)
    copy_list = [x for x in file_list_fr if x not in file_list_to]
    for file_name in copy_list:
        if not os.path.exists(os.path.join(copyTo, file_name)):
            # shutil.copy(os.path.join(copyFrom, file_name), copyTo)
            decrease_brightness(
                os.path.join(copyFrom, file_name), 0.2
            ).save(os.path.join(copyTo, file_name))


def decrease_brightness(file_path: str, intensity: float) -> ImageType:
    h, s, v = Image.open(file_path).convert("HSV").split()
    v = Image.fromarray(
        np.clip(np.array(v) * intensity, 0, 255).astype(np.uint8)
    )
    return Image.merge("HSV", (h, s, v)).convert("RGB")


if __name__ == '__main__':
    request_url = "https://cn.bing.com/HPImageArchive.aspx?format=js&idx=0&n=7&mkt=zh-CN&uhd=1&uhdwidth=3840&uhdheight=2160"
    main()
