# coding:utf-8
import os
import psutil
import GPUtil
import time
import win32gui
import win32con


# def cpu_percent():
#     cp = psutil.cpu_percent(interval=1, percpu=True)
#     print(f"|{cp[0]:2.0f}|{cp[1]:2.0f}|{cp[2]:2.0f}|{cp[3]:2.0f}|")
#     print(f"|{cp[4]:2.0f}|{cp[5]:2.0f}|{cp[6]:2.0f}|{cp[7]:2.0f}|")
#     return


def get_status(mode=False):
    global monitor_qbit, interval
    print("Initializing!\n")
    try:
        float(interval)
        print(f"Interval: {interval} s\n")
        interval -= 1
    except ValueError:
        input("Wrong parameter")
        exit()
    print(f"Monitor Qbit:{monitor_qbit}\n")
    connect_threads = 0
    if monitor_qbit:
        qb_pid = get_qbit_status()
        if qb_pid != 0:
            qbit_alive = True
        else:
            qbit_alive = False
    while True:
        time.sleep(interval)
        sent_before = psutil.net_io_counters().bytes_sent
        recv_before = psutil.net_io_counters().bytes_recv
        # cpup_before = psutil.cpu_percent(interval=None, percpu=True)
        # cpuo_before = psutil.cpu_percent(interval=None, percpu=False)
        time.sleep(1)

        sent_now = psutil.net_io_counters().bytes_sent
        recv_now = psutil.net_io_counters().bytes_recv
        cpup = psutil.cpu_percent(interval=None, percpu=True)
        cpuo = psutil.cpu_percent(interval=None, percpu=False)
        cpuchi = max(cpup)
        # co80 = len([x for x in cpup if x > 80])
        mem_usd = psutil.virtual_memory().used
        mem_avi = psutil.virtual_memory().total
        mem_pct = mem_usd/mem_avi*100
        mem_usd = fdata(mem_usd, format=1)
        # mem_avi = fdata(mem_avi, format=2)

        sent = fdata((sent_now - sent_before), suffix="Byte/s")
        recv = fdata((recv_now - recv_before), suffix="Byte/s")

        gpuo = float(GPUtil.getGPUs()[0].load)*100
        if monitor_qbit:
            if not qbit_alive:
                qb_pid = get_qbit_status()
                if qb_pid != 0:
                    qbit_alive = True
                else:
                    qbit_alive = False
            else:
                connect_threads = 0
                netstat = psutil.net_connections()
                for i, sconn in enumerate(netstat):
                    if sconn.pid == qb_pid and len(sconn.raddr) != 0:
                        connect_threads += 1
                if connect_threads == 0:
                    qbit_alive = False
        if not mode:
            os.system("cls")
        print(f"CPU: {cpuchi:5.1f}%  |{cpuo:5.1f}%")
        print(f"GPU:         |{gpuo:5.1f}%")
        # print(f" - core 80+:{co80:2d}")
        print(f"RAM: {mem_usd}|{mem_pct:5.1f}%")
        print(f"Net: {sent}↑")
        print(f"     {recv}↓")
        if monitor_qbit:
            if qbit_alive:
                print(f"Qbit: {qb_pid:6d} | ~{connect_threads:4d}")
            else:
                print(f"Qbit not on")


def get_qbit_status():
    pidlist = psutil.pids()

    qb_pid = 0
    for pid in pidlist:
        try:
            process = psutil.Process(pid)
            if "qbit" in process.name():
                qb_pid = pid
                break
        except Exception:
            pass
    return qb_pid


def fdata(data: int,
          cal_base=1024, show_base=1000, baselevel=0,
          suffix="b", format=1):
    """
    data: the number to process
    base: base for proccesssing
    baselevel: [0:-][1:k][2:M][3:G][4:T][5:P][6:E]
    suffix: after the processed number
    """
    symbols = ("k", "M", "G", "T", "P", "E")
    prefix = {}
    show_scale = {}
    data *= pow(cal_base, baselevel)
    for i, p_index in enumerate(symbols):
        prefix[p_index] = pow(cal_base, i+1)
        show_scale[p_index] = pow(show_base, i+1)
    for p_index in reversed(symbols):
        if data >= show_scale[p_index]:
            value = float(data)/prefix[p_index]
            if format == 1:
                returnS = f"{value:6.02f}{p_index:s}{suffix:s}"
            elif format == 2:
                returnS = f"{value:4.02f}{p_index:s}{suffix:s}"
            return returnS

    if format == 1:
        returnS = f"{data:6.02f} {suffix:s}"
    elif format == 2:
        returnS = f"{data:4.02f} {suffix:s}"
    return returnS


if __name__ == "__main__":
    debug = 0
    monitor_qbit = True
    # float
    interval = 2.5
    if not debug:
        os.system("title SMAC| color 0A")
        if monitor_qbit:
            os.system("mode con:cols=20 lines=7")
        else:
            os.system("mode con:cols=20 lines=6")

        os.system("cls")
        win32gui.SetWindowPos(
            win32gui.FindWindow(None, "SMAC"),
            win32con.HWND_TOPMOST,
            0, 0, 0, 0,
            win32con.SWP_NOMOVE |
            win32con.SWP_NOSIZE |
            win32con.SWP_NOREPOSITION
        )
    try:

        win32gui.SetWindowPos(
            win32gui.FindWindow(None, "SMAC"),
            win32con.HWND_TOPMOST,
            0, 0, 0, 0,
            win32con.SWP_NOMOVE |
            win32con.SWP_NOSIZE
        )
        get_status(mode=debug)
    except Exception as e:
        input(e)
