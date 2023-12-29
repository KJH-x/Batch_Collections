import zlib
import os
from concurrent.futures import ThreadPoolExecutor
import threading
from builtins import FileNotFoundError, FileExistsError


def get_valid_folder_path():
    while True:
        folder_path = input("请输入文件夹路径: ")
        if os.path.exists(folder_path) and os.path.isdir(folder_path):
            return folder_path
        else:
            print("路径不存在，请重新输入。")


def list_files_in_folder(folder_path, include_subfolders=True):
    file_paths = []
    for root, dirs, files in os.walk(folder_path):
        if include_subfolders:
            for file in files:
                file_paths.append(os.path.join(root, file))
        else:
            for file in files:
                file_paths.append(os.path.join(root, file))
            break  # 如果不包括子文件夹，就在第一层循环后退出

    return file_paths


def hash_value(file_name: str, block_size: int, file_size: int) -> int:
    with open(file_name, "rb") as openfile:
        crc = 0
        while True:
            data = openfile.read(block_size)
            if not data:
                break
            crc = zlib.crc32(data, crc)

    os.rename(
        file_name, f"{os.path.dirname(file_name)}\\{hex(crc).removeprefix('0x')}{os.path.splitext(file_name)[1]}")

    return 0


def process_file(file_name):
    try:
        block_size = 8192
        file_size = os.path.getsize(file_name)
        hash_value(file_name, block_size, file_size)

        lock.acquire()
        print(f"Processed file: {file_name}")
        lock.release()
    except FileNotFoundError as fnfe:
        pass
    except FileExistsError as fee:
        os.remove(file_name)
    except Exception as e:
        lock.acquire()
        print(f"Error processing file {file_name}: {e}")
        lock.release()


if __name__ == '__main__':
    # with open("path_filenames.txt", "r", encoding="utf-8") as file:
    #     files = file.read().splitlines()
    files = list_files_in_folder(
        get_valid_folder_path(), include_subfolders=False)

    print(len(files))
    # 设置线程池并发执行
    try:
        with ThreadPoolExecutor(max_workers=16) as executor:
            lock = threading.Lock()
            executor.map(process_file, files)
    except Exception as e:
        input(e)
