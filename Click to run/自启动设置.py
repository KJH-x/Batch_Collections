import argparse
import os
import subprocess
import sys
import ctypes
import time
import colorama

colorama.init()
BG = colorama.Back
FG = colorama.Fore
# print(BG.BLACK + FG.WHITE + 'Hello, world!' + FG.RESET + BG.RESET)
STYLE_NORMAL = f"{colorama.Back.BLACK}{colorama.Fore.LIGHTWHITE_EX}"
STYLE_EMP_ST = f"{colorama.Back.RED}{colorama.Fore.LIGHTWHITE_EX}"
STYLE_EMP_OP = f"{colorama.Back.GREEN}{colorama.Fore.LIGHTWHITE_EX}"
STYLE_RESET = f"{colorama.Back.RESET}{colorama.Fore.RESET}"
print(f"{STYLE_NORMAL}\n\n\t\t脚本自启动管理器\t\t\n\n{STYLE_RESET}")

def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False


def prompt_drag_file():
    print("请将需要设置开机启动的文件拖入此窗口...")
    input_file = input().strip('"')
    while not os.path.isfile(input_file):
        print("文件不存在，请重新拖入文件：")
        input_file = input().strip('"')
    return input_file


def check_task_error(taskname):
    try:
        print(taskname)
        subprocess.run(['schtasks', '/query', '/tn', taskname],
                       check=True, capture_output=True)
        return True

    except subprocess.CalledProcessError as e:
        if e.returncode:
            return False
        else:
            print(f"{STYLE_NORMAL}出现异常，请检查输入。{STYLE_RESET}")
            print(f"{STYLE_NORMAL}错误信息:\n{STYLE_EMP_ST}{e}{STYLE_RESET}")
            input(f"{STYLE_NORMAL}请按 Enter 键退出{STYLE_RESET}")
            exit()


if __name__ == '__main__':
    try:
        if not is_admin():
            current_dir = os.path.dirname(os.path.abspath(__file__))
            script = os.path.join(current_dir, __file__)

            params = " ".join(sys.argv[1:])
            filename = prompt_drag_file()

            try:
                ctypes.windll.shell32.ShellExecuteW(
                    None, "runas", sys.executable, f'"{script}" --file "{filename}" {params}', None, 1)
            except Exception as e:
                ctypes.windll.user32.MessageBoxW(None, str(e), "Error", 0x10)
            print("请在新打开的窗口中进行操作，本窗口将关闭...")
            time.sleep(3)
            sys.exit()

        else:
            print(f"{STYLE_NORMAL}\n\n\t管理员模式\t\t\n\n{STYLE_RESET}")
            parser = argparse.ArgumentParser()
            parser.add_argument(
                '--file', help='The file path to set auto-startup.')
            args = parser.parse_args()

            if not os.path.isfile(args.file):
                print("文件不存在，请检查输入的文件路径是否正确！")
                input("请按 Enter 键退出：")
                sys.exit(1)

            print(f"{STYLE_NORMAL}当前文件：{STYLE_EMP_ST}{args.file}{STYLE_NORMAL}")
            taskname = os.path.splitext(os.path.basename(args.file))[0] + "自启动"
            exist = check_task_error(taskname)

            if exist:
                choice = input(
                    f"{STYLE_NORMAL}文件{STYLE_EMP_ST}已加入{STYLE_NORMAL}任务计划，是否要{STYLE_EMP_OP}移出{STYLE_NORMAL}任务计划？(Y/N)：{STYLE_RESET}\n")
                if choice in ['1', 'y', 'Y']:
                    subprocess.run(
                        ['schtasks', '/delete', '/tn', taskname, '/f'], check=True)
                    print(f"{STYLE_EMP_ST}移出成功{STYLE_RESET}")
                    check_task_error(taskname)
                else:
                    print(f"{STYLE_NORMAL}操作已取消{STYLE_RESET}")

            else:
                choice = input(
                    f"{STYLE_NORMAL}文件{STYLE_EMP_ST}未加入{STYLE_NORMAL}任务计划，是否要{STYLE_EMP_OP}加入{STYLE_NORMAL}任务计划？(Y/N)：{STYLE_RESET}")
                if choice in ['1', 'y', 'Y']:
                    subprocess.run(['schtasks', '/create', '/tn', taskname, '/sc', 'onstart',
                                   '/delay', '0005:00', '/tr', f'"{args.file}"'], check=True)
                    print(f"{STYLE_EMP_ST}添加成功{STYLE_RESET}")
                    check_task_error(taskname)
                else:
                    print(f"{STYLE_NORMAL}操作已取消{STYLE_RESET}")

            print(f"{STYLE_EMP_ST}三秒后退出{STYLE_RESET}")
            time.sleep(3)

    except Exception as e:
        print(f"出现异常：{e}")
        input("请按 Enter 键退出：")
