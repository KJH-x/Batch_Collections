import time
import win32gui
import os
import sys


class WindowInfo:
    def __init__(self, hwnd: int, window_text: str, class_name: str, rect: tuple) -> None:
        self.hwnd = hex(hwnd)
        self.window_text = window_text
        self.class_name = class_name
        self.rect = rect

    def __str__(self) -> str:
        return f"hwnd: {self.hwnd}, window_text: {self.window_text}, class_name: {self.class_name}, rect: {self.rect}"


def get_visible_window() -> list[WindowInfo]:
    visible_window = []

    def enum_windows_proc(hwnd, lparam):
        if win32gui.IsWindowVisible(hwnd):
            window_text = win32gui.GetWindowText(hwnd)
            class_name = win32gui.GetClassName(hwnd)
            rect = win32gui.GetWindowRect(hwnd)
            visible_window.append(WindowInfo(
                hwnd, window_text, class_name, rect))

    win32gui.EnumWindows(enum_windows_proc, 0)
    return visible_window


def abbr_str(s: str, max_length=25) -> str:
    if len(s) <= max_length:
        return s
    else:
        return s[:12] + '...' + s[-12:]


def refresh_window_list():
    global last, present, song_name, artists
    window_info = get_visible_window()
    for info in window_info:
        if info.class_name == "OrpheusBrowserHost":
            song_name, artists = info.window_text.split(" - ", 1)
            song_name = abbr_str(song_name)
            artists = "/ ".join([abbr_str(x) for x in artists.split("/")])
            break
    present = f"正在播放: {song_name}, {artists}"
    if last != present:
        print(song_name, artists)
        with open(".\\netease_now_playing.txt", mode="w", encoding="utf-8") as file:
            file.write(f"正在播放: 曲名{song_name}, 艺术家{artists}")
    last = present


if __name__ == "__main__":
    last = present = song_name = artists = ""
    os.chdir(sys.path[0])
    while True:
        refresh_window_list()
        time.sleep(3)
