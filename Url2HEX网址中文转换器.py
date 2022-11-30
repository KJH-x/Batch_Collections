# Url Converter HEX standard
from urllib.parse import quote
import string
import pyperclip
# Vlist = []
# contentDir = "https://lexue.bit.edu.cn/pluginfile.php/583275/mod_resource/content/0/"
# downloadlink = []
# clipboard = ""
# for v in Vlist:
# url = quote(contentDir+v, safe=string.printable)
# downloadlink.append(url)
# clipboard += f"<a href=\"{url}\" target=\"_blank\">{v}</a><br>"
# print(downloadlink)

pyperclip.copy(quote(pyperclip.paste(), safe=string.printable))
