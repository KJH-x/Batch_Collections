import random


def get_random_chinese_string(n):
    zh_cn = ""
    start = int("4e00", 16)
    end = int("9fa5", 16)
    for ic in range(n):
        code = random.randint(start, end)
        str = chr(code)
        zh_cn += str

    print(f"生成的随机汉字为：{zh_cn}")
    return zh_cn


get_random_chinese_string(20)
