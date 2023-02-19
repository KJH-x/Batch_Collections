# encoding=utf-8
'''
Filename :生成二维码_make_QRcode.py
Datatime :2022/12/02
Author :KJH-x
'''
import sys
from traceback import print_exc
import pyperclip
import os
import qrcode
import datetime


name = "QR_maker_"+datetime.datetime.now().strftime("%y-%m-%d_%H-%M-%S")
SAVE_PATH = ".\\QR_maker\\"
os.chdir(sys.argv[0][0:sys.argv[0].rfind("\\")])
os.system("chcp 65001")
para = sys.argv
if not os.path.exists(SAVE_PATH):
    os.mkdir(SAVE_PATH)

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
    img.save(SAVE_PATH+name+".png")
    print("Success!Exiting")
except Exception:
    print_exc()
    input()
