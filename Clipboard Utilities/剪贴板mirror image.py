from io import BytesIO

import win32clipboard
from PIL import Image, ImageOps
from PIL.Image import Image as ImageClass
from PIL.Image import Resampling
from win32.win32clipboard import CF_BITMAP, CF_DIB, CF_DIBV5

# Format Constent     | value  | inWin32? | Description
# CF_BITMAP,          | 2      |    √     | 位图 (HBITMAP) 的句柄。
# CF_DIB,             | 8      |    √     | 包含 BITMAPINFO 结构的内存对象，后跟位图位。
# CF_DIBV5,           | 17     |    √     | 包含 BITMAPV5HEADER 结构的内存对象，后跟位图颜色空间信息和位图位。
# CF_DIF,             | 5      |    √     | Software Arts 的数据交换格式。
# CF_DSPBITMAP,       | 130    |    √     | 与专用格式关联的位图显示格式。 hMem 参数必须是可以以位图格式显示的数据的句柄，而不是专用格式的数据。
# CF_DSPENHMETAFILE,  | 142    |    √     | 与专用格式关联的增强型图元文件显示格式。 hMem 参数必须是可以以增强型图元文件格式显示的数据的句柄，而不是专用格式的数据。
# CF_DSPMETAFILEPICT, | 131    |    √     | 与专用格式关联的图元文件图片显示格式。 hMem 参数必须是可以以图元文件图片格式显示的数据的句柄，而不是专用格式的数据。
# CF_DSPTEXT,         | 129    |    √     | 与专用格式关联的文本显示格式。 hMem 参数必须是可以以文本格式显示的数据的句柄，而不是专用格式的数据。
# CF_ENHMETAFILE,     | 14     |    √     | 增强型图元文件的句柄 (HENHMETAFILE) 。
# CF_GDIOBJFIRST      | 0x0300 |    ?     | 应用程序定义的 GDI 对象剪贴板格式的整数值范围的开头。 范围的末尾为 CF_GDIOBJLAST。清空剪贴板时，不会使用 GlobalFree 函数自动删除与此范围内剪贴板格式关联的句柄。 此外，在此范围内使用值时， hMem 参数不是 GDI 对象的句柄，而是由 GlobalAlloc 函数使用 GMEM_MOVEABLE 标志分配的句柄。
# CF_GDIOBJLAST       | 0x03FF |    ?     | 请参阅 CF_GDIOBJFIRST。
# CF_HDROP,           | 15     |    √     | 类型 HDROP 的句柄，用于标识文件列表。 应用程序可以通过将句柄传递给 DragQueryFile 函数来检索有关文件的信息。
# CF_LOCALE,          | 16     |    √     | 数据是 HGLOBAL () 与剪贴板中的文本关联的区域设置标识符 (LCID) 的句柄。 关闭剪贴板时，如果剪贴板包含 CF_TEXT 数据但没有 CF_LOCALE 数据，系统会自动将 CF_LOCALE 格式设置为当前输入语言。 可以使用 CF_LOCALE 格式将不同的区域设置与剪贴板文本相关联。从剪贴板粘贴文本的应用程序可以检索此格式，以确定用于生成文本的字符集。请注意，剪贴板不支持多个字符集中的纯文本。 若要实现此目的，请改用带格式的文本数据类型，例如 RTF。系统使用与 CF_LOCALE 关联的代码页从 CF_TEXT 隐式转换为 CF_UNICODETEXT。 因此，使用正确的代码页表进行转换。
# CF_MAX,             | 18     |    √     | ?
# CF_METAFILEPICT,    | 3      |    √     | METAFILEPICT 结构定义的图元文件图片格式的句柄。 通过 DDE 传递 CF_METAFILEPICT 句柄时，负责删除 hMem 的应用程序还应释放 CF_METAFILEPICT 句柄引用的图元文件。
# CF_OEMTEXT,         | 7      |    √     | 包含 OEM 字符集中字符的文本格式。 每行以回车符/换行符 (CR-LF) 组合结束。 null 字符表示数据结束。
# CF_OWNERDISPLAY,    | 128    |    √     | 所有者显示格式。 剪贴板所有者必须显示和更新剪贴板查看器窗口，并接收 WM_ASKCBFORMATNAME、 WM_HSCROLLCLIPBOARD、 WM_PAINTCLIPBOARD、 WM_SIZECLIPBOARD和 WM_VSCROLLCLIPBOARD 消息。 hMem 参数必须为 NULL。
# CF_PALETTE,         | 9      |    √     | 调色板的句柄。 每当应用程序在依赖于或假定调色板的剪贴板中放置数据时，它也应该将调色板放在剪贴板上。如果剪贴板包含 CF_PALETTE (逻辑调色板) 格式的数据，则应用程序应使用 SelectPalette 和 RealizePalette 函数实现 (剪贴板中) 任何其他数据与该逻辑调色板进行比较。显示剪贴板数据时，剪贴板始终使用剪贴板上采用 CF_PALETTE 格式的任何对象作为其当前调色板。
# CF_PENDATA,         | 10     |    √     | Microsoft Windows for Pen Computing 的笔扩展的数据。
# CF_PRIVATEFIRST,    | 0x0200 |    ?     | 专用剪贴板格式的整数值范围的开头。 范围以 CF_PRIVATELAST结尾。 与专用剪贴板格式关联的句柄不会自动释放;剪贴板所有者必须释放此类句柄，通常是为了响应 WM_DESTROYCLIPBOARD 消息。
# CF_PRIVATEFIRST,    | 0x02FF |    ?     | 请参阅 CF_PRIVATEFIRST。
# CF_RIFF,            | 11     |    √     | 表示的音频数据比以 CF_WAVE 标准波形格式表示的音频数据更为复杂。
# CF_SYLK,            | 4      |    √     | Microsoft 符号链接 (SYLK) 格式。
# CF_TEXT,            | 1      |    √     | 文本格式。 每行以回车符/换行符 (CR-LF) 组合结束。 null 字符表示数据结束。 将此格式用于 ANSI 文本。
# CF_TIFF,            | 6      |    √     | 标记图像文件格式。
# CF_UNICODETEXT,     | 13     |    √     | Unicode 文本格式。 每行以回车符/换行符 (CR-LF) 组合结束。 null 字符表示数据结束。
# CF_WAVE,            | 12     |    √     | 表示其中一种标准波形的音频数据，例如 11 kHz 或 22 kHz PCM。
# UNICODE,            | True   |    √     | ?

fmtlst: list[tuple[int, str]] = [
    (win32clipboard.CF_BITMAP, "CF_BITMAP"),
    (win32clipboard.CF_DIB, "CF_DIB"),
    (win32clipboard.CF_DIBV5, "CF_DIBV5"),
    (win32clipboard.CF_DIF, "CF_DIF"),
    (win32clipboard.CF_DSPBITMAP, "CF_DSPBITMAP"),
    (win32clipboard.CF_DSPENHMETAFILE, "CF_DSPENHMETAFILE"),
    (win32clipboard.CF_DSPMETAFILEPICT, "CF_DSPMETAFILEPICT"),
    (win32clipboard.CF_DSPTEXT, "CF_DSPTEXT"),
    (win32clipboard.CF_ENHMETAFILE, "CF_ENHMETAFILE"),
    (win32clipboard.CF_HDROP, "CF_HDROP"),
    (win32clipboard.CF_LOCALE, "CF_LOCALE"),
    (win32clipboard.CF_MAX, "CF_MAX"),
    (win32clipboard.CF_METAFILEPICT, "CF_METAFILEPICT"),
    (win32clipboard.CF_OEMTEXT, "CF_OEMTEXT"),
    (win32clipboard.CF_OWNERDISPLAY, "CF_OWNERDISPLAY"),
    (win32clipboard.CF_PALETTE, "CF_PALETTE"),
    (win32clipboard.CF_PENDATA, "CF_PENDATA"),
    (win32clipboard.CF_RIFF, "CF_RIFF"),
    (win32clipboard.CF_SYLK, "CF_SYLK"),
    (win32clipboard.CF_TEXT, "CF_TEXT"),
    (win32clipboard.CF_TIFF, "CF_TIFF"),
    (win32clipboard.CF_UNICODETEXT, "CF_UNICODETEXT"),
    (win32clipboard.CF_WAVE, "CF_WAVE"),
    (win32clipboard.UNICODE, "UNICODE"),
]


def midclip(fmt_code: int) -> str | int | bytes | tuple:
    return win32clipboard.GetClipboardData(fmt_code)


def readClipboard() -> None:
    win32clipboard.OpenClipboard()
    # print(win32clipboard.())
    # print(win32clipboard.CountClipboardFormats())
    for (fmt_code, fmt_name) in fmtlst:
        if win32clipboard.IsClipboardFormatAvailable(fmt_code):
            if isinstance((content := midclip(fmt_code)), str):
                print(f"Type {fmt_name:9s} | str | len = {len(content)}")
            elif isinstance(content, int):
                print(f"Type {fmt_name:9s} | int | value = {content}")
            elif isinstance(content, bytes):
                print(f"Type {fmt_name:9s} |bytes| len = {len(content)}")
                print(f"{content.decode()}")
            elif isinstance(content, tuple):
                print(f"Type {fmt_name:9s} |tuple| len = {len(content)}")
                for i in content:
                    if isinstance(i, str):
                        print(f"    subitems |str| len = {len(i)} |{i}")
                    else:
                        print(f"    subitems {type(i)}")
            else:
                print(f"Type {fmt_name} | Uno | type is {type(content)}")
    win32clipboard.CloseClipboard()


win32clipboard.OpenClipboard()
if win32clipboard.IsClipboardFormatAvailable(CF_DIB):
    if isinstance((data := midclip(CF_DIB)), bytes):
        dib_data: bytes = data
win32clipboard.CloseClipboard()

if dib_data:
    image: ImageClass = Image.open(BytesIO(dib_data))

    # image.show()
    # original_width, original_height = image.size
    mirrored_image = ImageOps.mirror(image)
    mirrored_image.show()
    # resized_image.show()

    with BytesIO() as output1:
        mirrored_image.convert("RGB").save(output1, "DIB")
        new_dib_data = output1.getvalue()
        output1.close()

    win32clipboard.OpenClipboard()
    win32clipboard.EmptyClipboard()
    # win32clipboard.SetClipboardData(CF_BITMAP, new_dib_data)
    win32clipboard.SetClipboardData(CF_DIB, new_dib_data)
    win32clipboard.CloseClipboard()

    # -----------------------------------------------------------
    # Sharpness Experiment
    # -----------------------------------------------------------
    # from PIL import ImageEnhance

    # enhancer = ImageEnhance.Sharpness(resized_image)
    # images:list[ImageClass] = []
    # for i in range(8):
    #     factor = i / 4.0
    #     images.append(enhancer.enhance(factor))

    # total_width, max_height = new_size
    # total_width *= 8
    # new_image = Image.new('RGB', (total_width, max_height))

    # x_offset = 0
    # for img in images:
    #     new_image.paste(img, (x_offset, 0))
    #     x_offset += img.width

    # new_image.show()
    # -----------------------------------------------------------
    # Experiment conclusion: Lanczos method has the best quality
    # already. (Most chosen 5th (4/4.0=1.0 original) as the best)
    # -----------------------------------------------------------
