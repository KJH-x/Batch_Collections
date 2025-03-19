import time
from io import BytesIO

import win32clipboard
from PIL import Image
from PIL.Image import Image as ImageClass
from PIL.Image import Resampling
from pywintypes import error
from win32.win32clipboard import CF_DIB, CF_DIBV5

win32clipboard.OpenClipboard()
current_data = win32clipboard.GetClipboardData(CF_DIB)
win32clipboard.CloseClipboard()


# Open the clipboard
def setup_CF_DIB():
    global current_data
    win32clipboard.OpenClipboard()
    win32clipboard.EmptyClipboard()
    win32clipboard.SetClipboardData(CF_DIB, current_data)
    win32clipboard.CloseClipboard()


def resize_clipboard_CF_DIB():
    win32clipboard.OpenClipboard()
    if win32clipboard.IsClipboardFormatAvailable(CF_DIB):
        dib_data = win32clipboard.GetClipboardData(CF_DIB)
        # dibV5_data = win32clipboard.GetClipboardData(CF_DIBV5)
    win32clipboard.CloseClipboard()

    if dib_data:
        image: ImageClass = Image.open(BytesIO(dib_data))

        original_width, original_height = image.size
        resized_image = image.resize(
            (original_width // 2, original_height // 2),
            Resampling.LANCZOS
        )

        with BytesIO() as output:
            resized_image.convert("RGB").save(output, "DIB")
            new_dib_data = output.getvalue()
            output.close()

        win32clipboard.OpenClipboard()
        win32clipboard.EmptyClipboard()
        win32clipboard.SetClipboardData(CF_DIB, new_dib_data)
        win32clipboard.CloseClipboard()
    # print("done")


times = 1000
total_time = 0
for _ in range(times):
    try:
        setup_CF_DIB()
        start_time = time.time()
        resize_clipboard_CF_DIB()
        end_time = time.time()
        total_time += (end_time - start_time)
    except error:
        print("skip")
        pass
print(total_time/times)
# avg = 0.1491169472 s
