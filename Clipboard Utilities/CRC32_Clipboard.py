import pyperclip
import zlib
pyperclip.copy(hex(zlib.crc32(pyperclip.paste().encode(encoding="utf-8"))).upper().replace("0X",""))