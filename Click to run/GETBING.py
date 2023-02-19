# GETBING
import sys
import os
from traceback import print_exc

import yaml
import re

import requests
import json
import pyperclip


def read_config():
    """
    加载yaml配置文件
    """
    yaml_path = ".\\config.yaml"
    try:
        # open config
        with open(yaml_path, "r", encoding="utf-8") as config_file:
            data = yaml.load(config_file, Loader=yaml.FullLoader)
            return data
    except:
        input(print_exc())
        exit()


def main():
    try:
        os.system("chcp 65001|cls")
        os.chdir(sys.path[0])
        data = read_config()
        UA = {'user-agent': data["net"]["user_agent"]}
        resolution = "1920x1080"
        DL_temp_track = data["file"]["temp"]
        static_track = data["file"]["storage"]

        clipboard_temp = pyperclip.paste()
        if not os.path.exists(DL_temp_track):
            print("no such folder")
            # 在当前路径创建img/文件夹
            os.makedirs(DL_temp_track)
            print("created target folder")
        if not os.path.exists(static_track):
            print("no such folder")
            # 在当前路径创建img/文件夹
            os.makedirs(static_track)
            print("created target folder")

        os.system("dir "+static_track+" /D /B /A:-D |clip")
        existed_list = list(
            pyperclip.paste()
            .replace(".jpg", "").replace(".png", "").
            splitlines()
        )
        pyperclip.copy(clipboard_temp)

        response = requests.get(
            url="https://cn.bing.com/HPImageArchive.aspx?format=js&idx=0&n=7&mkt=zh-CN",
            headers=UA
        )
        jsonData = json.loads(response.text)

        for serial in range(0, 7):
            urlbase = (jsonData['images'][serial]['urlbase'])
            copyright = str(jsonData['images'][serial]['copyright'])

            pic_name = copyright[0:copyright.find('，', 0)]

            x1 = pic_name.find('（', 0) \
                if pic_name.find('（', 0) != -1 \
                else len(pic_name)

            x2 = pic_name.find('(', 0) \
                if pic_name.find('(', 0) != -1 \
                else len(pic_name)

            pic_name = pic_name[0:min(x1, x2)]
            pic_name = re.sub("[ 　（）,，]", "", pic_name)

            url = f"http://www.bing.com{urlbase}_{resolution}.jpg"
            pictureTrack = DL_temp_track+"\\"+pic_name+".jpg"

            if pic_name in existed_list:
                print(pic_name, " had already downloaded!")
            else:
                print(f"Downloading {pic_name}")
                saveImg(url, pictureTrack)

        xcopy(fromTrack=DL_temp_track, toTrack=static_track)
        print("All Done!")
        input("Press Enter to exit")
    except Exception:
        input(print_exc())


def saveImg(imgUrl, saveAs):
    try:
        pic = requests.get(imgUrl).content
        with open(saveAs, 'wb') as picture:
            picture.write(pic)
        return 1
    except Exception:
        input(print_exc())
        return 0


def xcopy(fromTrack, toTrack):

    os.system("dir "+str(fromTrack)+" /D /B /A:-D | clip")
    file_list_fr = pyperclip.paste().split("\n")
    os.system("dir "+str(toTrack)+" /D /B /A:-D | clip")
    file_list_to = pyperclip.paste().split("\n")
    copy_list = [x for x in file_list_fr if x not in file_list_to]
    for file_name in copy_list:
        if not os.path.exists(toTrack+"\\"+file_name):
            command = "xcopy \""+fromTrack+"\\" +\
                str(file_name)+"\" \""+str(toTrack)+"\" /D"
            os.system(command)
        else:
            pass
    return 1


if __name__ == '__main__':
    main()
