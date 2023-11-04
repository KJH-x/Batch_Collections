import os
import sys
import shutil
import re

if __name__ == "__main__":
    os.system("chcp 65001 > nul")

    # 输入aria2导出的文本文件路径
    print("\n本脚本搭配 Bilibili-Evolved 生成的文件使用\n")
    while 1:
        instructive_txtfile_path = input(
            "请输入文本文件路径(支持拖入): "
        ).replace("\'", "").replace("\"", "")
        if instructive_txtfile_path.endswith(".txt"):
            break

    # 提取文件名，并去除特殊字符，防止路径错误
    file_name = os.path.basename(instructive_txtfile_path)
    media_name = re.sub(
        r'[\\/:*?"<>|]', '', file_name
    ).removesuffix(".txt")

    # 读取txt目录并创建子目录，设为工作目录，移动到新文件夹
    txt_folder_path = os.path.dirname(instructive_txtfile_path)
    # os.chdir(txt_folder_path)
    valid_new_folder = os.path.join(txt_folder_path, media_name)
    os.makedirs(media_name, exist_ok=True)
    new_file_path = os.path.join(
        valid_new_folder, f"{media_name}.txt")
    shutil.move(instructive_txtfile_path, new_file_path)

    # 将当前工作目录改为文本文件所在目录
    os.chdir(valid_new_folder)

    # aria2c下载
    os.system(f"aria2c -i \"{media_name}.txt\"")

    # ffmpeg合并音画
    v_enc = "-c:v copy"
    a_enc = "-c:a copy"
    a_suffix = ".join"
    global_para = "-hide_banner"
    os.system(
        f"ffmpeg {global_para} -i \"{media_name}.m4a\" -i \"{media_name}.mp4\" {v_enc} {a_enc} \"{media_name}{a_suffix}.mp4\""
    )

    input("处理完成，回车退出。")
