import os
import shutil
import re
from glob import glob
from collections import defaultdict


def update_dl_info(txt_file_path, media_name):
    try:
        with open(txt_file_path, 'r', encoding='utf-8') as file:
            lines = file.readlines()

        for i, line in enumerate(lines):
            match = re.search(r'out=\[(.*?)]\.(.*?)$', line)
            if match:
                original_filename = match.group(1)
                file_extension = match.group(2)
                new_line = f'out={media_name}.{file_extension}\n'
                lines[i] = new_line

        with open(txt_file_path, 'w', encoding='utf-8') as file:
            file.writelines(lines)

    except Exception as e:
        print(f"Error processing aria2 txt file: {e}")


def name_rectify(string):
    brackets = re.compile(r'[{}\[\]\(\)（）]')
    result = re.sub(brackets, '', string)
    blanks = re.compile(r'\s+')
    return re.sub(blanks, '.', result)


def file_exam(file_path: str) -> int:
    if not file_path:
        return 0
    try:
        os.access(file_path, os.R_OK)
        return 1
    except (FileNotFoundError, PermissionError) as error:
        print(error)
    except Exception as e:
        print(f"An unexpected error occurred: \n{e}")
    return 0


def find_media_files(folder):
    files_in_given_path = glob(os.path.join(folder, '*'))
    media_files = [
        media_file for media_file in files_in_given_path
        if media_file.split(".")[-1] in
        {"flac", "mp4", "m4a", "aac", "mp3"}
    ]
    print("找到以下媒体", media_files)
    return media_files


def find_file_pairs(file_list):
    file_pairs = defaultdict(list)
    for file_path in file_list:
        file_name, file_ext = os.path.splitext(file_path)
        file_pairs[file_name].append(file_path)
    valid_pairs = [files for files in file_pairs.values() if len(files) == 2]
    return valid_pairs


def merge_files(input_files):
    v_enc = "-c:v copy"
    a_enc = "-c:a copy"
    a_suffix = ".join"
    global_para = "-hide_banner"
    input_files_str = ' '.join([f' -i "{file}"' for file in input_files])
    output_file_name = name_rectify(
        os.path.splitext(os.path.basename(input_files[0]))[0])
    print(
        f"ffmpeg {global_para}{input_files_str} {v_enc} {a_enc} \"{output_file_name}{a_suffix}.mp4\"")
    os.system(
        f"ffmpeg {global_para}{input_files_str} {v_enc} {a_enc} \"{output_file_name}{a_suffix}.mp4\"")

    os.remove(max(input_files, key=os.path.getsize))


if __name__ == "__main__":
    os.system("chcp 65001 > nul")

    print("\n本脚本搭配 Bilibili-Evolved 生成的aria2 input文件使用\n")
    print("\n请确认aria2已经添加到PATH,否则无法下载\n")
    print("\n请确认ffmpeg已经添加到PATH,否则无法合并\n")
    dl_info_txt = ""

    # [获取]输入文件
    while 1:
        dl_info_txt = input("请拖入/复制粘贴文本文件(或输入路径): ").strip('\'\" ')
        if dl_info_txt.endswith(".txt") and file_exam(dl_info_txt):
            print(f"{dl_info_txt}: 文件存在且可读")
            break
        else:
            print("输入的文件路径不合法，请重新输入")

    # 重命名文件：
    # 原始获得: dl_info_txt: path\xxx.txt
    # [获取]安全文件名: dl_instruction: xxx.txt
    dl_instruction = os.path.basename(name_rectify(dl_info_txt))
    # [获取]媒体文件名将会设置为: media_name: xxx
    media_name = dl_instruction.removesuffix(".txt")
    # [获取]根目录: root_folder: path
    root_folder = os.path.dirname(dl_info_txt)
    # [执行]os.system: ren: ren [drive:][path]filename1 filename2
    os.system(f"ren \"{os.path.join(dl_info_txt)}\" \"{dl_instruction}\"")
    # [设置]此时完成重命名，变量失效
    del dl_info_txt

    # 切换到新建文件夹：
    # [设置]设置工作目录为: path
    os.chdir(root_folder)
    # [获取]存放媒体和文本的文件夹完整路径: working_dir
    working_dir = os.path.join(root_folder, media_name)
    # [新建]新建上述文件夹: working_dir
    os.makedirs(media_name, exist_ok=True)
    # [获取]新的文件完整路径: new_dl_instruction: path\xxx\xxx.txt
    new_dl_instruction = os.path.join(working_dir, dl_instruction)
    # [移动] path\xxx.txt -> path\xxx\xxx.txt
    shutil.move(dl_instruction, f"{working_dir}")
    # [设置]新工作目录: path\xxx\
    os.chdir(working_dir)

    # 下载：
    # [修改]修改文件内的媒体名称
    update_dl_info(new_dl_instruction, media_name)
    # [执行]aria2c下载
    os.system(f"aria2c -i \"{media_name}.txt\"")

    # 合并：
    # [获取]下载的媒体文件列表
    media_files = find_media_files(working_dir)
    # [获取]下载的媒体对
    media_pairs = find_file_pairs(media_files)
    # [合并]
    for media_pair in media_pairs:
        merge_files(media_pair)

    # [合并]清理
    os.remove(new_dl_instruction)
    os.system(f"explorer.exe {working_dir}")
