# encoding=utf-8
'''
Filename :哈希计算器.py
Datatime :2022/09/08
Author :KJH-x
'''
from time import localtime, strftime
import zlib
import hashlib
import os
import sys


def main():

    blocksize = 1024 * 1024 * 64

    print(15*"-"+" File Hash "+15*"-")
    text = input("拖入文件（单个）：")

    file_path = str(text)
    print(f"\nFile path: {file_path:s}")

    if (file_path[0] == "\"" and file_path[-1] == "\"") or\
            (file_path[0] == "\'" and file_path[-1] == "\'"):
        file_path = file_path.replace("\"", "").replace("\'", "")

    try:
        file_size = os.path.getsize(file_path)
        print("\n"+5*" "+10*"-"+" File Info "+10*"-"+"\n")
        print(f"Size: {fdata(file_size,format=2,suffix='bytes'):s}")
    except OSError:
        input("\n无法找到的文件路径")
        return 1

    date = strftime("%Y/%m/%d %H:%M:%S",
                    localtime(os.path.getmtime(file_path)))
    print(f"最后修改: {date:s}")

    print("\n"+5*" "+10*"-"+" Hash Info "+10*"-"+"\n")

    [md5, sha_1, sha_256, sha_512, crc32] = hash_value(
        file_path, blocksize, file_size
    )

    print(f"CRC32:  {(crc32 & 0xffffffff):08X}")
    print(f"MD5:    {md5:s}")
    print(f"SHA1:   {sha_1:s}")
    print(f"SHA256: {sha_256:s}")
    print(f"SHA512: {sha_512:s}")

    return print("\n计算完成，Ctrl+C 退出\n")


def hash_value(file_name: str, block_size: int, file_size: int):
    read_count = block_count = int(file_size / block_size)
    md5 = hashlib.md5()
    sha1 = hashlib.sha1()
    sha256 = hashlib.sha256()
    sha512 = hashlib.sha512()
    with open(file_name, "rb") as openfile:
        crc = 0
        block_count += 3
        while True:
            read_count -= 1
            print(
                (read_count % 5 + 1) * "_" + "*" + (5 - read_count % 5) * "_" +
                f" 正在读取{block_count-read_count:8d} of {block_count:8d} (±3)",
                end="\r"
            )
            data = openfile.read(block_size)
            if not data:
                break
            crc = zlib.crc32(data, crc)
            md5.update(data)
            sha1.update(data)
            sha256.update(data)
            sha512.update(data)
    print(60*" ", end="\r")
    hash_md5 = str(md5.hexdigest()).upper()
    hash_sha1 = str(sha1.hexdigest()).upper()
    hash_sha256 = str(sha256.hexdigest()).upper()
    hash_sha512 = str(sha512.hexdigest()).upper()
    return [hash_md5, hash_sha1, hash_sha256, hash_sha512, crc]


def fdata(data: int,
          cal_base=1024, show_base=1000, baselevel=0,
          suffix="b", format=1) -> str:
    """
    data: the number to process
    base: base for proccesssing
    baselevel: [0:-][1:k][2:M][3:G][4:T][5:P][6:E]
    suffix: after the processed number
    """
    symbols = ("k", "M", "G", "T", "P", "E")
    prefix = {}
    show_scale = {}
    returnS = ""
    data *= pow(cal_base, baselevel)
    for i, p_index in enumerate(symbols):
        prefix[p_index] = pow(cal_base, i+1)
        show_scale[p_index] = pow(show_base, i+1)
    for p_index in reversed(symbols):
        if data >= show_scale[p_index]:
            value = float(data)/prefix[p_index]
            if format == 1:
                returnS = f"{value:6.02f}{p_index:s}{suffix:s}"
            elif format == 2:
                returnS = f"{value:4.02f}{p_index:s}{suffix:s}"
            return returnS

    if format == 1:
        returnS = f"{data:6.02f} {suffix:s}"
    elif format == 2:
        returnS = f"{data:4.02f} {suffix:s}"
    return returnS


if __name__ == "__main__":
    os.system("chcp 65001 >nul")
    os.chdir(sys.path[0])
    try:
        while True:
            main()
    except Exception as e:
        print(e)
