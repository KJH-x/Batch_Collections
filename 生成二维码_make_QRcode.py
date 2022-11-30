import sys
from traceback import print_exc
import pyperclip
import os
import qrcode
import datetime
name = datetime.datetime.now().strftime("%y-%m-%d_%H-%M-%S")
SAVE_PATH = ".\\"
os.chdir(SAVE_PATH)
os.system("chcp 65001")
para = sys.argv

try:
    if len(para) > 1 and para[1] == "--request_name":
        content = str(para[2])
        name = str(para[3])
    else:
        content = pyperclip.paste()

    qr = qrcode.QRCode(border=1)
    qr.add_data(content)
    qr.make(True)
    img = qr.make_image()
    img.save(".\\"+name+".png")
except Exception:
    print_exc()
    # input()
