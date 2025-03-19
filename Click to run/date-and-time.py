# pyright: reportUnknownMemberType=false
# pyright: reportUnknownArgumentType=false
# pyright: reportUnknownParameterType=false
# pyright: reportMissingParameterType=false
# pyright: reportAttributeAccessIssue=false
# pyright: reportUnknownVariableType=false
from datetime import datetime

import obspython as obs

# 全局变量
source_name: str = ""
interval: int = 500  # 更新间隔，毫秒
time_format: str = "%Y-%m-%d %H:%M:%S"  # 默认的时间格式


def script_description() -> str:
    """
    返回脚本的描述信息。
    :return: 脚本描述字符串
    """
    return "显示当前日期和时间在选定的文本源上。\n修改源名称后请重载脚本并选择。"


def script_update(settings) -> None:
    """
    更新脚本设置。
    :param settings: OBS 脚本设置对象
    """
    global source_name, time_format
    source_name = obs.obs_data_get_string(settings, "source")
    time_format = obs.obs_data_get_string(settings, "time_format")


def script_defaults(settings) -> None:
    """
    设置脚本的默认值。
    :param settings: OBS 脚本设置对象
    """
    obs.obs_data_set_default_int(settings, "interval", 1000)
    obs.obs_data_set_default_string(
        settings, "time_format", "%Y-%m-%d %H:%M:%S")


def script_properties():
    """
    定义脚本属性界面。
    :return: OBS 属性对象
    """
    props = obs.obs_properties_create()

    # 添加文本源选择器
    p = obs.obs_properties_add_list(
        props, "source", "文本源", obs.OBS_COMBO_TYPE_LIST, obs.OBS_COMBO_FORMAT_STRING)
    sources = obs.obs_enum_sources()
    if sources is not None:
        for source in sources:
            source_id = obs.obs_source_get_id(source)
            if source_id == "text_gdiplus_v2":  # 确保使用正确的ID
                name = obs.obs_source_get_name(source)
                obs.obs_property_list_add_string(p, name, name)
        obs.source_list_release(sources)

    # 添加时间格式输入框，附带格式写法和显示样例的提示
    obs.obs_properties_add_text(
        props, "time_format", "时间格式", obs.OBS_TEXT_DEFAULT)
    obs.obs_property_set_long_description(obs.obs_properties_get(props, "time_format"),
                                          "输入strftime格式字符串，例如：\n"
                                          "%Y - 年 (2024)\n"
                                          "%m - 月 (05)\n"
                                          "%d - 日 (30)\n"
                                          "%H - 小时\n"
                                          "%M - 分钟\n"
                                          "%S - 秒")

    return props


def update_text() -> None:
    """
    更新文本源中的日期和时间。
    """
    global source_name, time_format

    source = obs.obs_get_source_by_name(source_name)
    if source is not None:
        now = datetime.now()
        date_time = now.strftime(time_format)
        settings = obs.obs_data_create()
        obs.obs_data_set_string(settings, "text", date_time)
        obs.obs_source_update(source, settings)
        obs.obs_data_release(settings)
        obs.obs_source_release(source)


def script_load(settings) -> None:
    """
    脚本加载时调用。
    :param settings: OBS 脚本设置对象
    """
    obs.timer_add(update_text, interval)


def script_unload() -> None:
    """
    脚本卸载时调用。
    """
    obs.timer_remove(update_text)
