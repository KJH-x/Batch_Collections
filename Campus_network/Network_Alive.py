# encoding = utf-8
# Network_Alive

import os
import subprocess
import sys
from datetime import datetime
import time
import logging
import msvcrt


class UnreachableError(SyntaxError):
    """Code Branch that should not be reached
    """

    def __init__(self, msg):
        self.msg = msg

    def __str__(self):
        return repr(self.msg)
    pass


def report_time() -> str:
    """返回：文本：格式化的当前时间
    """
    return datetime.now().strftime("%H:%M:%S")


def date_log() -> int:
    """返回：整数：格式化的日期数字
    """
    return int(datetime.now().strftime("%d"))


def wait_for_keypress(msg: str):
    print(msg)
    msvcrt.getch()


def time_convert() -> str:
    """返回：文本：格式化的持续时间
    """
    duration = datetime.now()-START_TIME
    secs = duration.seconds % 60
    mins = int((duration.seconds) / 60) % 60
    hours = duration.days * 24+int((duration.seconds) / 3600)
    return f"{hours:d}:{mins:02d}:{secs:02d}"


def operation(operation: int):
    """AIO脚本交互函数，通过subprocess 调用

    """
    command = ["python", f"{AIO_PATH}\\AIO_login.py", "-a"]
    match operation:
        case 0:
            command.append("logout")
            try:
                prompt_return = subprocess.run(
                    command, check=True)
                prompt_return_code = prompt_return.returncode
            except subprocess.CalledProcessError as return_not_zero:
                logging.info(f"{report_time()}Expected Error: return_not_zero")
                logging.exception(f"Detail:\n{return_not_zero}")
                prompt_return_code = return_not_zero.returncode

        case 1:
            command.append("login")
            try:
                prompt_return = subprocess.run(
                    command, check=True)
                prompt_return_code = prompt_return.returncode
            except subprocess.CalledProcessError as return_not_zero:
                logging.info(f"{report_time()}Expected Error: return_not_zero")
                logging.exception(f"Detail:\n{return_not_zero}")
                prompt_return_code = return_not_zero.returncode

        case 2:
            # input("operation:start sp:verify")
            command.append("verify")
            try:
                prompt_return = subprocess.run(
                    command, check=True)
                prompt_return_code = prompt_return.returncode
            except subprocess.CalledProcessError as return_not_zero:
                logging.info(f"{report_time()}Expected Error: return_not_zero")
                logging.exception(f"Detail:\n{return_not_zero}")
                prompt_return_code = return_not_zero.returncode

        case _:
            prompt_return_code = -1
    if prompt_return_code == 2:
        wait_for_keypress(
            f"[WARN][{report_time()}]脚本丢失，无法启动，请重新启动脚本并跟随引导重新设置，按任意键退出")
        exit(1)
    elif prompt_return_code == 14:
        command.append("mkjson")
        try:
            prompt_return = subprocess.run(
                command, check=True)
            prompt_return_code = prompt_return.returncode
        except subprocess.CalledProcessError as return_not_zero:
            logging.info(f"{report_time()}Expected Error: return_not_zero")
            logging.exception(f"Detail:\n{return_not_zero}")
            prompt_return_code = return_not_zero.returncode
    return prompt_return_code


def relogin(interval=2):
    """带有两秒钟等待时间的重登
    """
    operation(0)
    time.sleep(interval)
    operation(1)
    time.sleep(interval)


def summary(statistic: dict[str, str], fail_log: list):
    """打印：文本：刷新时的任务总结

    返回：无
    """
    os.system("cls")
    rpd = date_log()

    print(45*'-')
    print(f"[INFO][{report_time()}] 启动至今<{time_convert()}>概况:")
    print(45*'-')
    print(
        f"|失败:{statistic['失败']:^5d}|成功:{statistic['成功']:^5d}|强制:{statistic['强制']:^5d}|跳过:{statistic['跳过']:^5d}|")
    print(45*'-')
    print(f"今日({rpd:02d}日)自动重登记录：")
    chk = 0
    for log in fail_log:
        if log[0] == rpd:
            chk = 1
            print(f"  - {log[1]}")
        else:
            fail_log.remove(log)
    print("  - （无记录）") if not chk else 1
    print(45*'-')
    return


def entrance_protect() -> bool:
    """脚本依赖检查

    返回：布尔：成功
    """
    print(f"[INFO][{report_time()}] 正在检查依赖脚本")
    while not check_component():
        continue
    os.system("cls")
    print(welcome_msg)
    main_loop()
    return True


def check_component() -> bool:
    """
    检查组件的可用性
    :return: 是否所有组件均可用的布尔值
    """
    global AIO_PATH
    # flag=True
    if os.access(f"{AIO_PATH}\\AIO_login.py", os.R_OK):
        pass
    else:
        print(f"[WARN][{report_time()}] 在\"{AIO_PATH}\"")
        print(f"[WARN][{report_time()}] 找不到登录脚本(默认情况下它应该和本脚本在同一个文件夹)")

        print(f"[INFO][{report_time()}] 也许你想手动输入脚本路径？(放在别的地方了)")
        new_path = input(
            f"[INFO][{report_time()}] 新的路径(直接回车以重新检查):").strip().replace("\\\\", "\\")
        if len(new_path) > 12 and new_path[-12:].lower() == 'aio_login.py':
            AIO_PATH = new_path[:-12]
        elif len(new_path) > 2 and new_path[-2:] == '\\':
            AIO_PATH = new_path[-2:]
        elif len(new_path) > 2:
            AIO_PATH = new_path
        elif new_path == '':
            pass
        else:
            raise UnreachableError("无法理解的路径")
        print(AIO_PATH)
        return False
    if not operation(2):
        # input("check_component:operation 2 check pass")
        return True
    else:
        # input("check_component:operation 2 check fail")
        return False


def main_loop() -> None:
    """
    主循环函数，用于进行ping检测和重连操作
    """
    statistic = {'失败': 0, '成功': 0, '强制': 0, '跳过': 0}
    fail_log = []  # 失败日志列表
    t1, t2 = 0.0, 0.0  # 用于记录ping操作的开始时间和结束时间
    command = ["ping", PING_TARGET, "-n", "2"]  # ping命令的参数列表
    while True:
        try:
            print(
                f"[INFO][{report_time()}] 正在ping {PING_TARGET}, [Ctrl+C] 强制重登")
            try:
                t1 = time.time()  # 记录ping操作的开始时间
                # 运行ping命令，将输出定向到垃圾桶，设置检查结果为阻塞
                subprocess.run(command, stdout=subprocess.DEVNULL, check=True)
                t2 = time.time()  # 记录ping操作的结束时间

            except KeyboardInterrupt as e:
                logging.exception(
                    f"[{report_time()}]An exception occurred: {e}")
                statistic['强制'] += 1
                print(f"[USER][{report_time()}] [Ctrl+C] 强制重登")
                time.sleep(0.2)
                sys.stdout.write('\r\033[K')  # 清除控制台输入的^C
                relogin()  # 重新登录
                continue

            except subprocess.CalledProcessError as e:
                logging.info(f"{report_time()}Expected Error: return_not_zero")
                logging.exception(
                    f"[{report_time()}]An exception occurred: {e}")
                t2 = t1 + 5
                pass

            if t2 - t1 > 4.5:  # 如果ping操作超过4.5秒，判定为失败
                statistic['失败'] += 1
                fail_log.append([date_log(), report_time()])
                print(f"[WARN][{report_time()}] ping 判定：离线")
                relogin()  # 重新登录

                if (statistic["失败"] + statistic["成功"] + statistic["强制"]) % 5 == 0:
                    summary(statistic, fail_log)  # 每5次检测，输出统计信息

            else:  # 如果ping操作未超过4.5秒，判定为成功
                statistic['成功'] += 1
                print(f"[INFO][{report_time()}] ping 判定：在线")

                if (statistic["失败"] + statistic["成功"] + statistic["强制"]) % 5 == 0:
                    summary(statistic, fail_log)  # 每5次检测，输出统计信息
                print(
                    f"[INFO][{report_time()}] 休眠十分钟， [Ctrl+C] 跳过休眠")

                time.sleep(600)  # 休眠10分钟（600秒）
        except KeyboardInterrupt as e:
            logging.exception(f"[{report_time()}]An exception occurred: {e}")
            statistic['跳过'] += 1
            print(
                f"[USER][{report_time()}] [Ctrl+C] 跳过休眠")
            continue
        except Exception as e:
            logging.exception(f"[{report_time()}]An exception occurred: {e}")
            print()
            raise e


PING_TARGET = 'bilibili.com'
VERSION = 'v1.1.1'
AIO_PATH = sys.path[0]
START_TIME = datetime.now()
welcome_msg = f"""
---------------------------------------------------------------------
[INFO] 欢迎使用校园网自动重连脚本
---------------------------------------------------------------------
| 当前版本{VERSION}，访问Github仓库以获取最新版脚本
| https://github.com/KJH-x/Batch_Collections/tree/main/Campus_network
---------------------------------------------------------------------
| 在判定期间可通过[Ctrl+C]跳过并强制重新登陆，
| 在睡眠期间可通过[Ctrl+C]打断睡眠开始下一轮ping
| 本消息将在下次概况刷新消失，访问仓库阅读 Readme.md 文件以了解更多
---------------------------------------------------------------------
"""

if __name__ == "__main__":
    os.chdir(sys.path[0])
    logging.basicConfig(filename=".\\NA_1_exceptions.log", level=logging.ERROR)
    while not entrance_protect():
        continue
