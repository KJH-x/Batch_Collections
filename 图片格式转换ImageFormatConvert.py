# encoding=utf-8
'''
Filename :图片格式转换ImageFormatConvert.py
Datatime :2022/11/30
Author :KJH-x
'''
import pillow_avif
from PIL import Image
# 必须先安装pillow-avif-plugin才能使用
# pip install pillow-avif-plugin

# 图片格式批量转换PNG JPG AVIF
import pyperclip


def clipboard_analyse() -> list:
    clip = pyperclip.paste()
    file_list = []
    if clip.count("\"") % 2 != 0:
        print("the number of \" is an odd")
        return []
    else:
        if clip.find("“") != -1:
            print("[Warning]illegal “ fond in path might cause Error")
        clip = clip.strip()
        start = clip.find("\"")
        end = clip.rfind("\"")
        clip = clip[start:end+1]
        for file_name in clip.splitlines():
            if file_name.find(".") != -1:
                file_list.append(file_name.replace("\"", ""))

        return file_list


def convert_img(from_type: str, to_type: str, file_list: list) -> bool:
    try:
        # 建议使用完整路径
        from_type = from_type.lower()
        to_type = to_type.lower()

        for file_name in file_list:
            file_name = str(file_name)
            try:
                Image.open(file_name).save(
                    file_name.replace(from_type, to_type), to_type.upper())
            except Exception:
                print(f"[Error]Cannot open {file_name} as an image, skipped")
        return 1
    except Exception:
        print("Unknown Error")
        return 0


file_list = clipboard_analyse()
ft = ""
if file_list != []:
    ftl = []
    print("[INFO]Clipboard Work File Found:")
    for item in file_list:
        print(item)
        ftl.append(
            str(item[
                str(item).rfind(".")+1:
            ]).lower()
        )
    print(f"[INFO]Total {len(file_list)} file(s)")
    if len(set(ftl)) != 1:
        ft = input("[REQUEST INPUT]Input File Type:\n")
    else:
        ft = str(ftl[0])


else:
    path = (input("[REQUEST INPUT]Drag File or Paste the path:\n"))
    ft = str(path[
        str(path).rfind(".")+1:
        str(path).rfind("\"")
    ]).lower()
    file_list.append(path.replace("\"", ""))


print(f"[INFO]Input File Type: {ft}")
print(30*"*")

tt = input("[REQUEST INPUT]Output File Type:\n")

if convert_img(ft, tt, file_list) != 0:
    input("[INFO]Done, hit Enter to exit")
else:
    input("[ERROR]Error occur")


# 反向，其他格式转AVIF
# JPGfilename = 'test.jpg'
# JPGimg = Image.open(JPGfilename)
# JPGimg.save(JPGfilename.replace("jpg", 'avif'), 'AVIF')
