import ctypes
import datetime
import os
import sys
import tkinter
import traceback

import cv2
import keyboard
import pyperclip

import win32con
import win32gui
import win32api
from PIL import ImageGrab
from pyzbar import pyzbar


def detectQR():
    try:
        global mainWindow, new_scan, copy_status, quit_scan, time_info, now

        # scan_time_log = datetime.datetime.now().strftime('%m-%d %H:%M:%S')
        picName = datetime.datetime.now().strftime('%y%m%d_%H%M%S')+".jpg"
        print(picName)
        ImageGrab.grab().save(picName)
        image = cv2.imread(picName)
        QRs = pyzbar.decode(image)
        if len(QRs) == 0:
            # print("\n\tQR NOT FOUND\n")
            # scan_info.configure(text=scan_time_log)
            change_status(0)
        else:
            # print("\n——————NEW WORK——————\n")

            if len(QRs) == 1:
                # print("1 Qrcode detected\n")
                content = QRs[0].data.decode("UTF8")
                # print("[QR_Info]:\n{}\n".format(content))
                pyperclip.copy(content)
                # scan_info.configure(text=scan_time_log)
                change_status(1)
            else:
                # print(str(len(QRs))+" Qrcodes detected\n")
                for eQR in QRs:
                    content = eQR.data.decode("UTF8")
                    # print("[QR_Info]:\n{}\n".format(content))
                    pyperclip.copy(content)
                    # scan_info.configure(text=scan_time_log)
                    change_status(1)
                    # input("Press [Enter] to get another(s?)\n")

        os.system("del .\\"+picName)
        # mainWindow.geometry()
        return

    except Exception:
        pass


def change_status(success):
    global copy_status
    if success:
        copy_status.configure(text=COPY_STATUS_SUCCESS, bg="#89ba3a")
    else:
        copy_status.configure(text=COPY_STATUS_FAIL, bg="#6c0000")

    return


def update_time():
    global time_info, mainWindow
    time_info.config(
        text=datetime.datetime.now().strftime('%m-%d %H:%M:%S')+HINT)
    mainWindow.after(100, update_time)


def window_setup():
    global mainWindow, new_scan, copy_status, quit_scan, time_info

    # mainWindow.geometry("280x330+50+50")

    new_scan = tkinter.Button(mainWindow, text=NEW_SCAN_DEFAULT,
                              command=detectQR, font=FONT_STYLE_2)
    # last_scan_label = tkinter.Label(mainWindow, text="上一次扫描 Last Scan",
    #                                 font=FONT_STYLE_3, bg="#002036", fg="white")
    # scan_info = tkinter.Label(mainWindow, text=SCAN_INFO_DEFAULT,
    #                           font=FONT_STYLE_4, bg="#61afe0", fg="#FFFFFF")
    copy_status = tkinter.Label(mainWindow, text=COPY_STATUS_DEFAULT,
                                font=FONT_STYLE_4, bg="#61afe0", fg="#FFFFFF")
    quit_scan = tkinter.Button(mainWindow, text="❌", bg="#FF0000",
                               fg="white", activebackground="white", command=mainWindow.destroy, font=FONT_STYLE_2)
    time_info = tkinter.Label(mainWindow, fg="white", font=FONT_STYLE_5, bg="#002036",
                              text=datetime.datetime.now().strftime('%m-%d %H:%M:%S')+HINT)
    # text_frame = tkinter.Text(
    #     mainWindow, font=FONT_STYLE_3, fg="white", bg="#002036", height=10)

    time_info.grid(column=0, columnspan=2, row=0, sticky="WNE")
    new_scan.grid(column=0, columnspan=1, row=1, sticky="WNE")
    quit_scan.grid(column=1, columnspan=1, row=1, sticky="WNE")
    copy_status.grid(column=2, columnspan=1, row=0, rowspan=2, sticky="WNS")

    # 窗口拖动
    time_info.bind("<Button-1>", MouseDown)
    time_info.bind("<B1-Motion>", MouseMoveW1)
    copy_status.bind("<Button-1>", MouseDown)
    copy_status.bind("<B1-Motion>", MouseMoveW2)

    mainWindow.configure(bg="#000000")
    (CursorX, CursorY) = win32api.GetCursorPos()
    # 去掉标题栏 设置置顶
    mainWindow.overrideredirect(1)
    mainWindow.attributes("-topmost", 1)
    mainWindow.after(10, update_time)
    mainWindow.geometry(f"+{CursorX}+{CursorY}")
    return


def console_default(console_title, console_color=0, exit_cls=0):
    os.system("chcp 65001")
    os.system("title "+str(console_title))
    os.chdir(sys.path[0])
    if console_color != 0:
        os.system("color "+str(console_color))
    if exit_cls != 0:
        os.system("cls")
    return


def MouseDown(event):
    global mousX, mousY

    mousX = event.x
    mousY = event.y


def MouseMoveW1(event):
    global mainWindow, mousX, mousY

    osx = mousX+time_info.winfo_x()
    osy = mousY+time_info.winfo_y()
    mainWindow.geometry(f'+{event.x_root - osx}+{event.y_root - osy}')


def MouseMoveW2(event):
    global mainWindow, mousX, mousY

    osx = mousX+copy_status.winfo_x()
    osy = mousY+copy_status.winfo_y()
    mainWindow.geometry(f'+{event.x_root - osx}+{event.y_root - osy}')


if __name__ == '__main__':
    try:
        console_default("scan_qr_console")
        ctypes.windll.shcore.SetProcessDpiAwareness(1)

        FONT_STYLE_1 = ("等线 bold", 20)
        FONT_STYLE_2 = ("等线", 20)
        FONT_STYLE_3 = ("等线", 15)
        FONT_STYLE_4 = ("等线 bold", 15)
        FONT_STYLE_5 = ("等线", 10)
        NEW_SCAN_DEFAULT = "🔍"
        SCAN_INFO_DEFAULT = "还未进行扫描"
        COPY_STATUS_DEFAULT = "就\n绪"
        COPY_STATUS_FAIL = "请\n重\n试"
        COPY_STATUS_SUCCESS = "已\n复\n制"
        HINT = "\nctrl_alt_shift_Q"
        now = datetime.datetime.now()

        keyboard.add_hotkey("ctrl+alt+shift+Q", detectQR)

        mainWindow = tkinter.Tk()

        window_setup()

        win32gui.ShowWindow(win32gui.FindWindow(
            0, "scan_qr_console"), win32con.HIDE_WINDOW)
        mainWindow.mainloop()

    except Exception:
        traceback.print_exc()
        input()
