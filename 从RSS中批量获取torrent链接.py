import pyperclip
paste_data = list(pyperclip.paste().split("\n"))
remove_lsit = []
for item in paste_data:
    if".torrent" not in item:
        remove_lsit.append(item)
for item in remove_lsit:
    paste_data.remove(item)

copy_list = []
for item in paste_data:
    copy_list.append(item.replace("<link>", "").replace("</link>\r", ""))
print(copy_list)
pyperclip.copy("\n".join(copy_list))
