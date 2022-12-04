# encoding=utf-8
'''
Filename :小鸟五小时计算.py
Datatime :2022/12/02
Author :KJH-x
'''
from time import strftime
from time import gmtime
import datetime
# print(datetime.strftime("",datetime.localtime()))


def finishTime(timeString1: str) -> list:
    timing = []
    if timeString1.find(":") == -1:
        if len(timeString1) == 5:
            timing.append(timeString1[0:1])
            timing.append(timeString1[1:3])
            timing.append(timeString1[3:5])
        elif len(timeString1) == 6:
            timing.append(timeString1[0:2])
            timing.append(timeString1[2:4])
            timing.append(timeString1[4:6])
    return timing


suffix = datetime.datetime.strftime(datetime.datetime.now(), "%Y-%m-%d ")
"""'2022-11-30'"""
# time1 = "9:12:34"
# time2 = "4:14:37"

time1 = ":".join(finishTime(input("[INPUT] input an countdown : ")))
print(f"[INFO] TIME 1 RECORDED: {time1}")
time2 = ":".join(finishTime(input("[INPUT]input the other countdown : ")))
print(f"[INFO] TIME 2 RECORDED: {time2}")


fivehour = datetime.datetime.strptime(suffix+"5:00:00", "%Y-%m-%d %H:%M:%S")
zerotime = datetime.datetime.strptime(suffix+"0:00:00", "%Y-%m-%d %H:%M:%S")
caltime1 = datetime.datetime.strptime(suffix+time1, "%Y-%m-%d %H:%M:%S")
caltime2 = datetime.datetime.strptime(suffix+time2, "%Y-%m-%d %H:%M:%S")


if (caltime1-caltime2).total_seconds() >= 0:
    slower = (caltime1-zerotime).total_seconds()
    faster = (caltime2-zerotime).total_seconds()
else:
    slower = (caltime2-zerotime).total_seconds()
    faster = (caltime1-zerotime).total_seconds()

targettime = (fivehour-zerotime).total_seconds()

acctime_slow = slower - targettime
acctime_fast = faster / slower * acctime_slow

a = strftime("%H:%M:%S", gmtime(targettime))
b = strftime("%H:%M:%S", gmtime(slower))
c = strftime("%H:%M:%S", gmtime(acctime_slow))
d = strftime("%H:%M:%S", gmtime(faster))
e = strftime("%H:%M:%S", gmtime(acctime_fast))
r = faster / slower

print(f"[INFO] {b} - {a} -> {c}")
print(f"[INFO] ratio : {d} / {b} = {r:.3f}")

print(43*"-")
print("[RESULT]:\n[acclerate time equivalent]")
print(strftime(" - %H:%M:%S", gmtime(acctime_slow)))
print("[acclerate time]\n[USE THIS TO SET YOUR COUNTDOWN] ")
print(strftime(" - %H:%M:%S", gmtime(acctime_fast)))
print(43*"-")
input()
