import os
import random


def rename_files(directory):
    # 获取目录下的所有文件
    files = os.listdir(directory)
    file_count = len(files)
    used_numbers = set()  # 用于存储已经使用的随机数

    for filename in files:
        # 生成随机数，确保不重复
        random_number = random.randint(file_count+1, 2*file_count)
        while random_number in used_numbers:
            random_number = random.randint(file_count+1, 2*file_count)

        # 构建新的文件名
        new_filename = str(random_number) + os.path.splitext(filename)[1]

        # 重命名文件
        old_path = os.path.join(directory, filename)
        new_path = os.path.join(directory, new_filename)
        os.rename(old_path, new_path)

        used_numbers.add(random_number)

    files = os.listdir(directory)
    file_count = len(files)
    used_numbers = set()  # 用于存储已经使用的随机数

    for filename in files:
        # 生成随机数，确保不重复
        random_number = random.randint(1, file_count)
        while random_number in used_numbers:
            random_number = random.randint(1, file_count)

        # 构建新的文件名
        new_filename = str(random_number) + os.path.splitext(filename)[1]

        # 重命名文件
        old_path = os.path.join(directory, filename)
        new_path = os.path.join(directory, new_filename)
        os.rename(old_path, new_path)

        used_numbers.add(random_number)


# 输入目录路径
directory = input("请输入目录路径：")
rename_files(directory)
