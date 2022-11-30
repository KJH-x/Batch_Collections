# encoding=utf-8
'''
Filename :Url2HEX网址中文转换器.py
Datatime :2022/11/30
Author :KJH-x
'''
from urllib.parse import quote
import string
import pyperclip
# Vlist = []
# contentDir = ""
# downloadlink = []
# clipboard = ""
# for v in Vlist:
# url = quote(contentDir+v, safe=string.printable)
# downloadlink.append(url)
# clipboard += f"<a href=\"{url}\" target=\"_blank\">{v}</a><br>"
# print(downloadlink)

pyperclip.copy(quote(pyperclip.paste(), safe=string.printable))
