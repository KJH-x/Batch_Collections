import os
import msvcrt
from io import TextIOWrapper
import datetime
import re


def list_files_and_subfolders(path: str, save_name: str, list_file: bool, indent='') -> int:
    """
    Lists files and subfolders recursively in a given directory and saves the result to a file.

    Args:
        path (str): The path of the directory to be listed.
        save_name (str): The name of the file to save the listing.
        list_file (bool): A flag indicating whether to include files in the listing.
        indent (str, optional): The indentation string for subfolders. Defaults to ''.

    Returns:
        int: The total count of files and subfolders listed.
    """
    global count
    count = 0
    with open(os.path.join(path, save_name), 'w', encoding='utf-8') as file:
        root_folder_name = os.path.basename(path)
        file.write(root_folder_name + '\n')
        list_files_and_subfolders_recursive(path, file, indent, list_file)
    return count


def list_files_and_subfolders_recursive(path: str, file: TextIOWrapper, indent: str, list_file: bool) -> None:
    """
    Recursively lists files and subfolders in a given directory and writes them to a file.

    Args:
        path (str): The path of the directory to be listed.
        file (TextIOWrapper): The file object to write the listing.
        indent (str): The indentation string for subfolders.
        list_file (bool): A flag indicating whether to include files in the listing.

    Returns:
        None
    """
    global count
    file_symbol = '├─'
    folder_symbol = '└─'

    items = sorted(os.listdir(path))
    for index, item in enumerate(items):
        is_last = (index == len(items) - 1)
        item_path = os.path.join(path, item)

        if os.path.isdir(item_path):
            if item not in SKIPS[0]:
                file.write(indent + folder_symbol + item + '\n')
                count += 1
                next_indent = indent + ' 　'
                list_files_and_subfolders_recursive(
                    item_path, file, next_indent, list_file)
        else:
            if list_file:
                symbol = folder_symbol if is_last else file_symbol
                file.write(indent + symbol + item + '\n')
                count += 1
            else:
                pass
    return


def delete_files_with_pattern(path: str, pattern: str) -> None:
    """
    删除当前文件夹下名称符合指定模式的文件。

    Args:
        pattern (str): 匹配模式，支持通配符 * 和 ?。

    Returns:
        None
    """
    current_dir = path
    files = os.listdir(current_dir)
    for file in files:
        if re.match(file, pattern):
            file_path = os.path.join(current_dir, file)
            os.remove(file_path)


def wait_for_keypress(msg: str):
    print(msg)
    msvcrt.getch()


SKIPS = [[".old"], []]
file_path = input("请输入文件夹路径：")
count_s = list_files_and_subfolders(
    file_path, f"文件结构.{datetime.datetime.now().strftime('%y.%m.%d')}.txt", True)
count_s = list_files_and_subfolders(
    file_path, f"目录结构.{datetime.datetime.now().strftime('%y.%m.%d')}.txt", False)
print(f"子文件夹数量:{count_s}")
wait_for_keypress(f"文件结构已经保存到给定的目录,按任意键继续")
