# 100055keepalive
import sys
import os
import subprocess
import zlib
from datetime import datetime
from time import sleep


debug = 0
if not debug:
    os.system("")

TLF = "%H:%M:%S.%f"
def report_time()->str:
    return datetime.now().strftime(TLF)

while 1:
    try:
        print(f"[INFO][{report_time()}] Pinging...")
        try:
            reply = os.popen("ping bilibili.com -n 10")
            reply_detail = reply.readlines()
            print(f"[INFO][{report_time()}] Ping End")
            print(f"[INFO][{report_time()}] Result Get")
        except KeyboardInterrupt:
            print(f"[WARN][{report_time()}] Skipped")
            os.system(f"python {sys.path[0]}\\AIO_login.py -a login")
            continue
        for line in reply_detail:
            line=str(line)
            if "loss" in line:
                print(
                    f"[INFO][{report_time()}] string \"loss\" found in line{line.index('loss')}")
                if int(line[line.find("(")+1: line.find("%")]) > 50:
                    print("[WARNING] Low connectivity, ReLogin...")
                    os.popen("python -m 10_0_0_55 login")
                    try:
                        os.system(f"python {sys.path[0]}\\AIO_login.py -a logout")
                        print(
                            f"[INFO][{report_time()}] Command Sent, sleep for command interval")
                        sleep(5)
                        print(f"[INFO][{report_time()}] Awake from command interval")
                        os.system(
                            f"python {sys.path[0]}\\AIO_login.py -a login")
                    except Exception:
                        pass
                    print(f"[INFO][{report_time()}] Command Sent, sleep for interval")
                    sleep(1)
                    print(f"[INFO][{report_time()}] Awake from interval")
                else:
                    print(f"[INFO][{report_time()}] Network status: Normal")
                    print(f"[INFO][{report_time()}] No action, sleep 600s")
                    sleep(600)
                    print(f"[INFO][{report_time()}] Awake from normal sleep")
    except Exception as e:
        input(e)