import os


def print_directory_contents(path, prefix=''):
    try:
        contents = os.listdir(path)
    except FileNotFoundError:
        print("输入有误")
        return
    for i, item in enumerate(contents):
        full_path = os.path.join(path, item)
        if os.path.isdir(full_path):
            if i == len(contents) - 1:
                print(prefix + "└── " + item)
                print_directory_contents(full_path, prefix + "    ")
            else:
                print(prefix + "├── " + item)
                print_directory_contents(full_path, prefix + "│   ")
        else:
            if i == len(contents) - 1:
                print(prefix + "└── " + item)
            else:
                print(prefix + "├── " + item)


path = input("请输入路径：")
print_directory_contents(path)

input("按任意键退出")
