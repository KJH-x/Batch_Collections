# 100055keepalive
import sys
import os
from datetime import datetime
from time import sleep, time


def report_time() -> str:
    return datetime.now().strftime("%H:%M:%S")


def date_log() -> int:
    return int(datetime.now().strftime("%d"))


def time_convert() -> str:
    duration=datetime.now()-start_time
    secs = duration.seconds % 60
    mins = int((duration.seconds) / 60) % 60
    hours = duration.days * 24+int((duration.seconds) / 3600)
    return f"{hours:d}:{mins:02d}:{secs:02d}"


def log_op(operation: int):
    match operation:
        case 0:
            ret = os.system(f"python {sys.path[0]}\\AIO_login.py -a logout")
        case 1:
            ret = os.system(f"python {sys.path[0]}\\AIO_login.py -a login")
        case _:
            ret = -1
    return ret


def relogin(interval=2):
    log_op(0)
    sleep(interval)
    log_op(1)
    sleep(interval)


def summary():
    os.system("cls")
    rpd = date_log()

    print(f"[INFO][{report_time()}]启动至今<{time_convert()}>概况:")
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


PING_TARGET = 'bilibili.com'
if __name__ == "__main__":
    start_time = datetime.now()
    statistic = {'失败': 0, '成功': 0, '强制': 0, '跳过': 0}
    fail_log = []
    t1, t2 = 0, 0
    log_op(1)
    while 1:
        try:
            print(
                f"[INFO][{report_time()}] 正在ping {PING_TARGET}, [Ctrl+C] 强制重登")

            try:
                t1 = time()
                os.popen(f"ping {PING_TARGET} -n 2").readlines()
                t2 = time()

            except KeyboardInterrupt:
                statistic['强制'] += 1
                print(f"[USER][{report_time()}] [Ctrl+C] 强制重登")
                relogin()
                continue

            if t2-t1 > 4.5:
                statistic['失败'] += 1
                fail_log.append([date_log(), report_time()])
                print(f"[WARN][{report_time()}] ping 判定：离线")
                relogin()

            else:
                statistic['成功'] += 1
                print(f"[INFO][{report_time()}] ping 判定：在线")
                if (statistic["失败"]+statistic["成功"]+statistic["强制"]) % 5 == 0:
                    summary()
                print(
                    f"[INFO][{report_time()}] 休眠十分钟， [Ctrl+C] 跳过休眠")
                sleep(600)

        except KeyboardInterrupt:
            statistic['跳过'] += 1
            print(
                f"[USER][{report_time()}] [Ctrl+C] 跳过休眠")
            continue

        except Exception as e:
            input(e)
