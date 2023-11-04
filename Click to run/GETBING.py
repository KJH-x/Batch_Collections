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


def main():
    try:
        os.system("chcp 65001 >nul")
        os.chdir(sys.path[0])
        data = read_config(".\\config.yaml")

        UA = {'user-agent': data["net"]["user_agent"]}
        resolution = "1920x1080"
        download_path = data["file"]["temp"]
        static_path = data["file"]["storage"]

        if not os.path.exists(download_path):
            print(f"不存在:{download_path}")
            os.makedirs(download_path)
            print(f"已创建:{download_path}")
        if not os.path.exists(static_path):
            print(f"不存在:{static_path}")
            os.makedirs(static_path)
            print(f"已创建:{static_path}")
        get_file_list(static_path)
        existed_list = get_file_list(static_path,False)
        print(f"正在查询图片列表")
        response_json = json.loads(
            get_response(
                url="https://cn.bing.com/HPImageArchive.aspx?format=js&idx=0&n=7&mkt=zh-CN",
                headers=UA
                ).text
        )

        for serial in range(0, 7):
            pic_url_base = (response_json['images'][serial]['urlbase'])
            pic_copyright = str(response_json['images'][serial]['copyright'])
            pic_name = re.findall('^([^,，（()]+)', pic_copyright)[0]
            

            x1, x2 = map(lambda x: x.end() if x else len(pic_name),
                        [re.match('.*（', pic_name), re.match('.*\(', pic_name)])

            pic_name = pic_name[:min(x1, x2)]

            pic_name = re.sub("[ 　（）,，]", "", pic_name)
            url = f"http://www.bing.com{pic_url_base}_{resolution}.jpg"
            pic_save_path = f"{download_path}\\{pic_name}.jpg"
            if pic_name in existed_list:
                print(f"已下载：{pic_name}")
            else:
                print(f"正在下载：{pic_name}")
                saveImg(url, pic_save_path)
        xcopy(fromTrack=download_path, toTrack=static_path)
        print("All Done!")
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


def get_file_list(folder_path: str, flag=True) -> list:
    """
    Get a list of file names in the folder_path.

    Args:
        folder_path (str): the folder path
        flag (bool): if True, the file name will contain the extension, otherwise not

    Returns:
        list: a list of file names
    """
    if not os.path.exists(folder_path):
        return []

    file_list = os.listdir(folder_path)
    if flag:
        return file_list
    else:
        return [os.path.splitext(file_name)[0] for file_name in file_list]


def xcopy(fromTrack, toTrack):
    fromTrack = os.path.abspath(fromTrack)
    toTrack = os.path.abspath(toTrack)
    if not os.path.exists(fromTrack):
        os.makedirs(fromTrack)
    if not os.path.exists(toTrack):
        os.makedirs(toTrack)
    file_list_fr = get_file_list(fromTrack)
    file_list_to = get_file_list(toTrack)
    copy_list = [x for x in file_list_fr if x not in file_list_to]
    for file_name in copy_list:
        if not os.path.exists(os.path.join(toTrack, file_name)):
            shutil.copy(os.path.join(fromTrack, file_name), toTrack)


if __name__ == '__main__':
    main()
