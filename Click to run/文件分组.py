import os
import shutil
from collections import defaultdict


def organize_files_by_name(directory:str):
    # Step 1: 获取指定目录下的所有文件
    files = [f for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f))]
    
    # Step 2: 通过文件名（不包含扩展名）对文件进行分组
    file_groups:dict[str,list[str]] = defaultdict(list)
    for file in files:
        name, _ = os.path.splitext(file)
        file_groups[name].append(file)
    
    # Step 3: 创建目录并移动文件
    for name, file_list in file_groups.items():
        if len(file_list) > 2:
            new_dir = os.path.join(directory, name)
            os.makedirs(new_dir, exist_ok=True)
            print(f"Moving:\n\t{"\n\t".join(file_list)}\n-> {new_dir}")
            for file in file_list:
                shutil.move(os.path.join(directory, file), os.path.join(new_dir, file))
                # print(f"Moved {file} to {new_dir}")

# 使用方法，指定目录路径
directory_path = input("path:")
organize_files_by_name(directory_path)
