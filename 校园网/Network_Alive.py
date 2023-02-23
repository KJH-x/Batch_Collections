# 100055keepalive
import sys
import os
from datetime import datetime
from time import sleep, time


debug = 0
if not debug:
    os.system("")


def report_time() -> str:
    return datetime.now().strftime("%H:%M:%S.%f")


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



if __name__ == "__main__":
    t1, t2 = 0, 0
    log_op(1)
    while 1:
        try:
            print(
                f"[INFO][{report_time()}] Pinging...[Ctrl+C] to force re-login")

            try:
                t1 = time()
                os.popen("ping bilibili.com -n 2").readlines()
                t2 = time()

            except KeyboardInterrupt:
                print(
                    f"[WARN][{report_time()}] User: [Ctrl+C] Skip Pingand re-login")
                relogin()
                continue

            if t2-t1 > 4.5:
                print(f"[WARN][{report_time()}] Network status: Offline")
                relogin()

            else:
                print(f"[INFO][{report_time()}] Network status: Normal")
                print(
                    f"[INFO][{report_time()}] Sleep for 600s, [Ctrl+C] to force re-login\n")
                sleep(600)
                print(f"[INFO][{report_time()}] Awake from normal sleep")

        except KeyboardInterrupt:
            print(
                f"[WARN][{report_time()}] User: [Ctrl+C] Skip sleep and re-login")
            relogin()
            continue

        except Exception as e:
            input(e)
