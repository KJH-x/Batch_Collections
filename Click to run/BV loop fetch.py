import pyperclip
import os
import sys
import re
from time import sleep
os.chdir(sys.path[0])
pattern = re.compile(r"/(BV.*?)/")
with open(".\\BVR.txt", "a+", encoding="utf-8") as record:
    while True:
        clipboard = pyperclip.paste()
        result = pattern.search(clipboard)
        if result:
            BVC = result.group(1)
            record.write(f"{BVC}\n")
            print(f"record: {BVC}")
            pyperclip.copy("")
        else:
            sleep(0.5)
