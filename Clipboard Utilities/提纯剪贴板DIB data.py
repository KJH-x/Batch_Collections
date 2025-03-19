import win32clipboard
from win32.win32clipboard import CF_BITMAP, CF_DIB, CF_DIBV5

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


win32clipboard.OpenClipboard()
if win32clipboard.IsClipboardFormatAvailable(CF_DIB):
    if isinstance((data := midclip(CF_DIB)), bytes):
        dib_data: bytes = data
win32clipboard.CloseClipboard()

if dib_data:

    win32clipboard.OpenClipboard()
    win32clipboard.EmptyClipboard()
    win32clipboard.SetClipboardData(CF_DIB, dib_data)
    win32clipboard.CloseClipboard()
