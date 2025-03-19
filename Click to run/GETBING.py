# GETBING
# pyright:reportUnknownVariableType =false
# pyright:reportUnknownMemberType =false
import json
import math
import os
import re
import sys
import time
import winreg
from traceback import print_exc
from typing import Any, Optional

import numpy as np
import requests
from PIL import Image, ImageDraw, ImageFont
from PIL.Image import Image as ImageType
from PIL.ImageDraw import ImageDraw as ImageDrawType
from PIL.ImageFont import FreeTypeFont
from requests.exceptions import ConnectionError, RequestException


class GetProxyFail(Exception):
    pass


# 获取本地代理信息（IE代理/System Proxy）
def get_ie_proxy_settings() -> str | None:
    try:
        reg = winreg.OpenKey(winreg.HKEY_CURRENT_USER,
                             r"Software\Microsoft\Windows\CurrentVersion\Internet Settings")
        proxy_enable = winreg.QueryValueEx(reg, "ProxyEnable")[0]
        if proxy_enable == 1:
            proxy_server = winreg.QueryValueEx(reg, "ProxyServer")[0]
            return proxy_server
        else:
            raise GetProxyFail
    except Exception:
        # print("Error:", e)
        return None
        # raise GetProxyFail


def read_config(config_path: str) -> dict[str, dict[str, str]]:
    with open(config_path, 'r', encoding='utf-8') as cfg:
        return json.load(cfg)


def get_response(url: str, headers: dict[str, Any], proxy: str = "") -> tuple[requests.Response, dict[str, str]]:
    while True:
        try:
            session = requests.Session()
            if proxy == "":
                response = session.get(url=url, headers=headers)
            else:
                response = session.get(url=url, headers=headers, proxies={
                    "http": f"http://{proxy}"})
            # 出现意外时主动报告错误
            response.raise_for_status()
            if response.text == "":
                raise ValueError(
                    "reponse length = 0, consider changing cookies")
            return response, session.cookies.get_dict()
        except RequestException | ConnectionError | GetProxyFail as e:
            print(f"Request failed: {str(e)}")


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
        while True:
            # 请求下载
            if proxy == "":
                pic = requests.get(imgUrl, headers=user_agent).content
            else:
                pic = requests.get(imgUrl, headers=user_agent, proxies={
                    "http": proxy}).content
            if len(pic) == 0:
                print("Err: Request: Returning 0 size content, retrying...")
                continue
            else:
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


def adjustAndCopy(copyFrom: str, copyTo: str, font_path: Optional[str] = None):
    # 确保路径正常
    copyFrom = os.path.abspath(copyFrom)
    copyTo = os.path.abspath(copyTo)
    # 此处省略了确认文件夹存在
    # 获取文件列表
    file_list_fr = [f"{_[:-4]}.jpg" for _ in getFileList(copyFrom)]
    file_list_to = [f"{_[:-4]}.jpg" for _ in getFileList(copyTo)]
    # 获取差异列表，os.listdir返回的是list所以沿用list而非set
    copy_list = [x for x in file_list_fr if x not in file_list_to]
    copy_list_length = len(copy_list)
    print(f"文件列表统计完成：{copy_list_length}个文件待处理")
    for idx, file_name in enumerate(copy_list):
        print(f"正在处理：[{idx}/{copy_list_length}]{file_name}")
        if not os.path.exists(os.path.join(copyTo, file_name)):
            # shutil.copy(os.path.join(copyFrom, file_name), copyTo)
            # 读取，降低明度，保存（另存为）
            decrease_brightness(
                os.path.join(copyFrom, file_name), 0.2, font_path, f"{file_name[:-4]}"
            ).save(os.path.join(copyTo, f"{file_name[:-4]}.jpg"))


def decrease_brightness(file_path: str, intensity: float, font_path: Optional[str] = None, print_text: Optional[str] = None) -> ImageType:
    # 以hsv 读取图片
    h, s, v = Image.open(file_path).convert("HSV").split()
    # 处理v通道
    v = Image.fromarray(
        np.clip(np.array(v) * intensity, 0, 255).astype(np.uint8)
    )
    image: ImageType = Image.merge("HSV", (h, s, v)).convert("RGBA")

    if font_path is not None:
        layer_txt = Image.new("RGBA", image.size, (255, 255, 255, 0))

        w, h = layer_txt.size
        # Determine font size and margins
        font_size = math.ceil(3.5 / 100 * h)  # 3.5% of image height
        margin = math.ceil(0.2 / 100 * h)    # 0.2% of image height

        # Load the font
        font: FreeTypeFont = ImageFont.truetype(font_path, font_size)

        # Create a drawing context
        draw: ImageDrawType = ImageDraw.Draw(layer_txt, mode="RGBA")

        # Determine text size
        text_bbox = draw.textbbox((0, 0), print_text, font=font)
        text_width = text_bbox[2] - text_bbox[0]  # Width of the text
        text_height = text_bbox[3] - text_bbox[1]  # Height of the text

        # Calculate position for bottom-right alignment with margins
        x_position = w - text_width - 2*margin
        y_position = h - text_height - 8*margin

        # Draw text
        draw.text(
            (x_position, y_position),
            print_text,
            fill=(255, 255, 255, 25),  # White with 20% opacity
            font=font
        )
        image = Image.alpha_composite(image, layer_txt)

        # Save or show the image
        # image.show()  # Or save using image.save("output_path.jpg")
        # input()
    # 返回图片（类）
    return image.convert("RGB")


def update_cookie(new_cookies_dict: dict[str, str], config_path: str):
    if os.path.exists(config_path):
        with open(config_path, 'r', encoding='utf-8') as file:
            data = json.load(file)
    else:
        # 如果文件不存在，创建一个空的字典结构
        data = {"net": {}}

    # 如果 ["net"]["cookie"] 存在并且是字符串，则将其转换为字典
    if "cookie" in data.get("net", {}) and isinstance(data["net"]["cookie"], str):
        # 将 cookie 字符串转换为字典对象
        existing_cookies_dict = dict(item.split("=", maxsplit=1) for item in data["net"]["cookie"].split("; "))
    else:
        # 如果 cookie 不存在或不是字符串，初始化为一个空字典
        existing_cookies_dict = {}

    existing_cookies_dict.update(new_cookies_dict)

    # 将更新后的 Cookie 字典转换回字符串形式
    updated_cookies_str = "; ".join([f"{key}={value}" for key, value in existing_cookies_dict.items()])

    # 更新 JSON 中的 ["net"]["cookie"] 键
    data["net"]["cookie"] = updated_cookies_str

    # 将更新后的数据写回 JSON 文件
    with open(config_path, 'w', encoding='utf-8') as file:
        json.dump(data, file, ensure_ascii=False, indent=4)
        print("Cookie已更新")


def main():
    try:
        # BING4K原图下载器
        # 流程：获取bing列表，下载到【下载文件夹】，降低明度并保存副本到【储存文件夹】
        # 使用UTF-8显示
        os.system("chcp 65001 >nul|cls")
        os.chdir(sys.path[0])

        # 获取本地代理设置：
        if (local_proxy := get_ie_proxy_settings()):
            print(f"当前代理{local_proxy}")
        else:
            print(f"当前没有代理")
            local_proxy = ""

        # 读取配置
        data: dict[str, dict[str, str]] = read_config(".\\get_bing.json")

        # 提取配置到变量
        headers: dict[str, str] = {
            'user-agent': data["net"]["user_agent"], 'Cookie': data["net"]["cookie"]}
        query_url: str = data["net"]["query_url"]
        download_path: str = data["file"]["temp"]
        static_path: str = data["file"]["storage"]
        font_path: Optional[str] = data.get('test', {}).get('font', None)
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
        response, cookie_dict = get_response(
            url=query_url, headers=headers, proxy=local_proxy)
        response_json_zh = dict(json.loads(response.text))
        update_cookie(cookie_dict, ".\\get_bing.json")

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
                saveImg(url, headers, pic_save_path)

        # 调整图片明度并保存副本，此项会按文件名称重新检查差异项
        # 若下载文件夹有自定义内容也会被尝试操作，请注意保持干净
        adjustAndCopy(copyFrom=download_path, copyTo=static_path, font_path=font_path)

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
