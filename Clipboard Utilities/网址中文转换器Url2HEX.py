# encoding=utf-8
'''
Filename :Url2HEX网址中文转换器.py
Datatime :2022/11/30
Author :KJH-x
'''
from urllib.parse import quote
import string
import pyperclip

pyperclip.copy(quote(pyperclip.paste().strip().replace(' ','%20'), safe=string.printable))
