# obs-netease-now-playing
# pyright: reportAttributeAccessIssue=false


import obspython as obs
import win32gui
from pywintypes import error as pytError

target_name: str = ""
interval: int = 500
info_format: str = "正在播放:[%A]《%T》"
artists_split: str = "、"
title: str = ""
artist: str = ""
match_hwnd_name: list[str] = ["OrpheusBrowserHost", "TXGuiFoundation"]
match_type_list: list[str] = ["网易云音乐/Netease Cloud Music", "QQ音乐/QQ Music"]
match_type: str = "网易云音乐/Netease Cloud Music"
match_type_check: list[tuple[str, str]] = list(
    zip(match_hwnd_name, match_type_list))


def script_description() -> str:
    msg = "A Script for Obtaining Song Titles/Artists from [NetEase Cloud Music] Based on Process Class Lookups \n\n" +\
    "Reload this Script if you can't find your text source (or you have changed the name of the source)"
    return msg


def script_defaults(settings) -> None:
    obs.obs_data_set_default_int(settings, "interval", interval)
    obs.obs_data_set_default_string(settings, "info_format", info_format)
    obs.obs_data_set_default_string(settings, "artists_split", "、")
    obs.obs_data_set_default_string(
        settings, "match_type", "网易云音乐/Netease Cloud Music")


def script_update(settings) -> None:
    global target_name, info_format, artists_split, match_type
    target_name = obs.obs_data_get_string(settings, "target_name")
    info_format = obs.obs_data_get_string(settings, "info_format")
    artists_split = obs.obs_data_get_string(settings, "artists_split")
    match_type = obs.obs_data_get_string(settings, "match_type")


def script_properties():
    props = obs.obs_properties_create()

    target_select_box = obs.obs_properties_add_list(
        props, "target_name", "Info Output", obs.OBS_COMBO_TYPE_LIST, obs.OBS_COMBO_FORMAT_STRING)
    targets = obs.obs_enum_sources()
    if targets is not None:
        for target in targets:
            target_id = obs.obs_source_get_id(target)
            if target_id in ["text_gdiplus_v3", "text_gdiplus_v2"]:
                name = obs.obs_source_get_name(target)
                obs.obs_property_list_add_string(target_select_box, name, name)
        # obs.obs_source_release(targets)

    obs.obs_properties_add_text(
        props, "info_format", "display style", obs.OBS_TEXT_DEFAULT)
    obs.obs_property_set_long_description(obs.obs_properties_get(props, "info_format"),
                                          "%A = artists list\n%T = title")

    obs.obs_properties_add_text(
        props, "artists_split", "split string for artists list", obs.OBS_TEXT_DEFAULT)

    match_type_box = obs.obs_properties_add_list(
        props, "match_type", "match", obs.OBS_COMBO_TYPE_LIST, obs.OBS_COMBO_FORMAT_STRING)
    for types in match_type_list:
        obs.obs_property_list_add_string(match_type_box, types, types)
    return props


def update_text() -> None:

    global target_name, info_format, artists_split
    target = obs.obs_get_source_by_name(target_name)
    if target is not None:
        np_text = get_now_playing_info(info_format, artists_split)
        settings = obs.obs_data_create()
        obs.obs_data_set_string(settings, "text", np_text)
        obs.obs_source_update(target, settings)
        obs.obs_data_release(settings)

        obs.obs_source_release(target)


def script_load(settings) -> None:
    obs.timer_add(update_text, interval)


def script_unload() -> None:
    obs.timer_remove(update_text)


class WindowInfo:
    def __init__(self, hwnd: int, window_text: str, class_name: str, rect: tuple[int, int, int, int]) -> None:
        self.hwnd = hex(hwnd)
        self.window_text = window_text
        self.class_name = class_name
        self.rect = rect

    def __str__(self) -> str:
        return f"hwnd: {self.hwnd}, window_text: {self.window_text}, class_name: {self.class_name}, rect: {self.rect}"


def get_visible_window() -> list[WindowInfo]:
    visible_window: list[WindowInfo] = []

    def enum_windows_proc(hwnd: int, lparam: ...):
        if win32gui.IsWindowVisible(hwnd):
            window_text = win32gui.GetWindowText(hwnd)
            class_name = win32gui.GetClassName(hwnd)
            rect = win32gui.GetWindowRect(hwnd)
            visible_window.append(WindowInfo(
                hwnd, window_text, class_name, rect))

    win32gui.EnumWindows(enum_windows_proc, 0)
    return visible_window


def abbr_str(s: str, max_length: int = 25) -> str:
    if len(s) <= max_length:
        return s
    else:
        return s[:12] + '...' + s[-12:]


def get_now_playing_info(info_format: str, artists_split: str = "、") -> str:
    global title, artist, match_type, match_type_check

    flag = False
    try:
        window_info = get_visible_window()
        for info in window_info:
            if (info.class_name, match_type) in match_type_check:
                try:
                    title, artist = info.window_text.split(" - ", 1)
                    title = abbr_str(title).strip()
                    artist = artists_split.join(
                        [abbr_str(x) for x in artist.split("/")]).strip()
                except ValueError:
                    print("Window found, but no infomation")
                finally:
                    flag = True
                    break
            else:
                pass
        if not flag:
            print(
                "No window matched, make sure you have open the window (not just in tray)")
    except pytError:
        pass

    return info_format.replace("%A", artist).replace("%T", title)
