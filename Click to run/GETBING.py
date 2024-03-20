# GETBING
import json
import os
import re
import sys
import time
import winreg
from traceback import print_exc
from typing import Any

import numpy as np
import requests
from PIL import Image
from PIL.Image import Image as ImageType


class GetProxyFail(Exception):
    pass


# 获取本地代理信息（IE代理/System Proxy）
def get_ie_proxy_settings() -> str:
    try:
        reg = winreg.OpenKey(winreg.HKEY_CURRENT_USER,
                             r"Software\Microsoft\Windows\CurrentVersion\Internet Settings")
        proxy_enable = winreg.QueryValueEx(reg, "ProxyEnable")[0]
        if proxy_enable == 1:
            proxy_server = winreg.QueryValueEx(reg, "ProxyServer")[0]
            return proxy_server
        else:
            raise GetProxyFail
    except Exception as e:
        print("Error:", e)
        raise GetProxyFail


def read_config(config_path: str) -> dict[str, dict[str, str]]:
    with open(config_path, 'r', encoding='utf-8') as cfg:
        return json.load(cfg)


def get_response(url: str, headers: dict[str, Any], proxy: str = ""):
    try:
        if proxy == "":
            response = requests.get(url=url, headers=headers)
        else:
            response = requests.get(url=url, headers=headers, proxies={
                                    "http": f"http://{get_ie_proxy_settings()}"})
        # 出现意外时主动报告错误
        response.raise_for_status()
        return response
    except requests.exceptions.RequestException | GetProxyFail as e:
        raise Exception(f"Request failed: {str(e)}")


def checkDir(path: str) -> bool:
    try:
        if not os.path.exists(path):
            print(f"不存在:{path}")
            os.makedirs(path)
            print(f"已创建:{path}")
        return True
    except Exception:
        input(print_exc())
        return False


def saveImg(imgUrl: str, user_agent: dict[str, Any], saveAs: str, proxy: str = "") -> bool:
    try:
        # 请求下载
        if proxy == "":
            pic = requests.get(imgUrl, headers=user_agent).content
        else:
            pic = requests.get(imgUrl, headers=user_agent, proxies={
                "http": f"http://{get_ie_proxy_settings()}"}).content
        # 保存
        with open(saveAs, 'wb') as picture:
            picture.write(pic)
        return True
    except Exception:
        print("Failed to save image!")
        print_exc()
        return False


def getFileList(folder_path: str, name_with_ext: bool = True) -> list[str]:
    if not os.path.exists(folder_path):
        return []
    file_list = os.listdir(folder_path)
    if name_with_ext:
        return file_list
    else:
        # 如果不要拓展名，处理并返回
        return [os.path.splitext(file_name)[0] for file_name in file_list]


def adjustAndCopy(copyFrom: str, copyTo: str):
    # 确保路径正常
    copyFrom = os.path.abspath(copyFrom)
    copyTo = os.path.abspath(copyTo)
    # 此处省略了确认文件夹存在
    # 获取文件列表
    file_list_fr = getFileList(copyFrom)
    file_list_to = getFileList(copyTo)
    # 获取差异列表，os.listdir返回的是list所以沿用list而非set
    copy_list = [x for x in file_list_fr if x not in file_list_to]
    for file_name in copy_list:
        if not os.path.exists(os.path.join(copyTo, file_name)):
            # shutil.copy(os.path.join(copyFrom, file_name), copyTo)
            # 读取，降低明度，保存（另存为）
            decrease_brightness(
                os.path.join(copyFrom, file_name), 0.2
            ).save(os.path.join(copyTo, file_name))


def decrease_brightness(file_path: str, intensity: float) -> ImageType:
    # 以hsv 读取图片
    h, s, v = Image.open(file_path).convert("HSV").split()
    # 处理v通道
    v = Image.fromarray(
        np.clip(np.array(v) * intensity, 0, 255).astype(np.uint8)
    )
    # 返回图片（类）
    return Image.merge("HSV", (h, s, v)).convert("RGB")


def main():
    try:
        # BING4K原图下载器
        # 流程：获取bing列表，下载到【下载文件夹】，降低明度并保存副本到【储存文件夹】
        # 使用UTF-8显示
        os.system("chcp 65001 >nul|cls")
        os.chdir(sys.path[0])

        # 获取本地代理设置：
        local_proxy = get_ie_proxy_settings()
        print(f"当前代理{local_proxy}")

        # 读取配置
        data: dict[str, dict[str, str]] = read_config(".\\get_bing.json")

        # 提取配置到变量
        user_agent: dict[str, str] = {'user-agent': data["net"]["user_agent"]}
        query_url: str = data["net"]["query_url"]
        download_path: str = data["file"]["temp"]
        static_path: str = data["file"]["storage"]
        resolution: str = "UHD"
        print("读取配置完成")

        # 检查（创建）目标文件夹
        checkDir(download_path)
        checkDir(static_path)
        print("路径检查完成")

        # 获取【储存文件夹】里的图片列表
        archive_list = getFileList(static_path)
        # 获取【下载文件夹】里的图片列表
        existed_list = getFileList(download_path, False)
        print(f"储存文件夹有：{len(archive_list)}文件，下载文件夹有：{len(existed_list)}文件")

        # 查询Bing图片列表
        print(f"正在向必应查询图片列表")
        response_json_zh = dict(json.loads(
            get_response(url=query_url, headers=user_agent,
                         proxy=local_proxy).text
        ))
        # 此处留有操作空间，若需要请求多个url可增添此项
        response_json = {**response_json_zh}

        # 下载图片组
        for serial in range(0, 7):
            # 从请求返回获取目标图片链接（以及在链接中的图片标题）
            # Hint: URLBASE: '/th?id=OHR.{NAME}_ZH-CN{NUMBERS}'
            # 请求返回中另有中文图片版权信息，可自行查看更改，由于匹配规则复杂，此处弃用
            pic_url_base = (response_json['images'][serial]['urlbase'])
            pattern = r"(.[A-Za-z0-9]+_)"
            pic_name = str(re.findall(pattern, pic_url_base)[0]).strip("._")

            # 下载、保存图片
            url = f"http://www.bing.com{pic_url_base}_{resolution}.jpg"
            pic_save_path = f"{download_path}\\{pic_name}.jpg"

            # 若已存在，跳过下载
            if pic_name in existed_list:
                print(f"已下载：{pic_name}")
            else:
                print(f"正在下载：{pic_name}")
                saveImg(url, user_agent, pic_save_path)

        # 调整图片明度并保存副本，此项会按文件名称重新检查差异项
        # 若下载文件夹有自定义内容也会被尝试操作，请注意保持干净
        adjustAndCopy(copyFrom=download_path, copyTo=static_path)

        print("全部完成!")
        time.sleep(3)

    except Exception:
        # 顶多是代理配置问题罢
        input(print_exc())


if __name__ == '__main__':
    """ Create get_bing.json in same folder with getbing.py, schema should like
    {
        "net": {
            "user_agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
            "query_url": "https://cn.bing.com/HPImageArchive.aspx?format=js&idx=0&n=7&mkt=zh-CN&uhd=1&uhdwidth=3840&uhdheight=2160"
        },
        "file": {
            "temp": "/path/to/download",
            "storage": "/path/to/after_processed"
        }
    }
    """
    main()
