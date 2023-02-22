import argparse
import sys
import hmac
from requests import Session
from hashlib import sha1
import json
import os
from enum import Enum
import math
from base64 import b64encode
from html.parser import HTMLParser
from urllib.parse import parse_qs, urlparse
import requests
from datetime import datetime
from getpass import getpass

# 鸣谢：https://github.com/Aloxaf/10_0_0_55_login


class Action(Enum):
    LOGIN = "login"
    LOGOUT = "logout"


class AlreadyOnlineException(Exception):
    pass


class AlreadyLoggedOutException(Exception):
    pass


class UsernameUnmatchedException(Exception):
    pass


class UnreachableError(SyntaxError):
    """Branch that should not be reached
    """

    def __init__(self, msg):
        self.msg = msg

    def __str__(self):
        return repr(self.msg)
    pass


def report_time() -> str:
    return datetime.now().strftime(TLF)


def read_config() -> tuple[str, str]:
    """从脚本所在文件夹读取用户信息
    
    Return:
        Username, Password
    """
    try:
        config_file=open(".\\bit_user_detail.json", "r", encoding="utf8") 
        config = json.load(config_file)
        return config["username"], config["password"]
    except FileNotFoundError:
        print(f"[{report_time()}] 未找到配置文件，正在创建...")
        return write_config()
    except json.decoder.JSONDecodeError:
        print(f"[{report_time()}] 文件错误，正在重写...")
        return write_config()



def write_config() -> tuple[str, str]:
    with open(".\\bit_user_detail.json", "w", encoding="utf8") as config_file:
        username = input(f"[{report_time()}] 请输入账号:")
        password = getpass(f"[{report_time()}] 请输入密码:",)
        config_file.write(
            f"{{\"username\":\"{username}\",\"password\":\"{password}\"}}"
        )
    return username, password


API_BASE = "http://10.0.0.55"
TYPE_CONST = 1
N_CONST = 200
TLF = "%H:%M:%S"


class User:
    def __init__(self, username: str, password: str) -> None:
        """初始化变量
        """
        self.username = username
        self.password = password

        self.ip, self.acid = parse_homepage()
        self.session = Session()

    def log_action(self, action: Action) -> dict:
        """检查当前登录情况
        
        Raises:
            - AlreadyOnlineException: 重复登录
            - AlreadyLoggedOutException: 重复登出
            - UsernameUnmatchedException: 登出用户名错误

        Returns:
            - json: response
        """
        is_logged_in, username = get_user_info()

        if is_logged_in and action is Action.LOGIN:
            raise AlreadyOnlineException(f"[{report_time()}] {username}重复登录")

        elif not is_logged_in and action is Action.LOGOUT:
            raise AlreadyLoggedOutException(f"[{report_time()}] {username}重复登出")

        elif username and username != self.username:
            raise UsernameUnmatchedException(
                f"[{report_time()}] 当前在线用户:{username}与尝试操作用户:{self.username}账号不同"
            )

        # 检查通过，开始执行登录登出
        params = self._make_params(action)
        response = self.session.get(
            API_BASE + "/cgi-bin/srun_portal",
            params=params
        )
        res=dict(json.loads(response.text[6:-1]))
        res["username"]=self.username
        return res

    def _get_token(self) -> str:
        """获取token

        Returns:
            - str: token
        """
        params = {
            "callback": "jsonp",
            "username": self.username,
            "ip": self.ip
        }

        response = self.session.get(
            API_BASE + "/cgi-bin/get_challenge", params=params
        )
        result = json.loads(response.text[6:-1])
        return result["challenge"]

    def _make_params(self, action: Action) -> dict:
        """制作请求参数

        Returns:
            - dict: params
        """
        token = self._get_token()

        params = {
            "callback": "jsonp",
            "username": self.username,
            "action": action.value,
            "ac_id": self.acid,
            "ip": self.ip,
            "type": TYPE_CONST,
            "n": N_CONST,
        }

        data = {
            "username": self.username,
            "password": self.password,
            "acid": self.acid,
            "ip": self.ip,
            "enc_ver": "srun_bx1",
        }

        hmd5 = hmac.new(token.encode(), b"", "MD5").hexdigest()
        json_data = json.dumps(data, separators=(",", ":"))
        info = "{SRBX1}" + fkbase64(xencode(json_data, token))
        chksum = sha1(
            "{0}{1}{0}{2}{0}{3}{0}{4}{0}{5}{0}{6}{0}{7}".format(
                token, self.username, hmd5, self.acid, self.ip, N_CONST, TYPE_CONST, info
            ).encode()
        ).hexdigest()

        params.update(
            {
                "password": "{MD5}" + hmd5,
                "chksum": chksum,
                "info": info
            }
        )

        return params


def parse_homepage():
    """解析并获取ip与acid

    Raises:
        - Exception: Throw exception if acid not present in the redirected URL
        - Exception: Throw exception if response text does not contain IP

    Returns:
        - tuple[str, str]: ip, ac_id
    """

    res = requests.get(API_BASE)

    # ac_id appears in the url query parameter of the redirected URL
    query = parse_qs(urlparse(res.url).query)
    ac_id = query.get("ac_id")

    if not ac_id:
        raise Exception("failed to get acid")

    # ip appears in the response HTML
    class IPParser(HTMLParser):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.ip = None

        def handle_starttag(self, tag, attrs):
            if tag == "input":
                attr_dict = dict(attrs)
                if attr_dict.get("name") == "user_ip":
                    self.ip = attr_dict["value"]

        def feed(self, *args, **kwargs):
            super().feed(*args, **kwargs)
            return self.ip

    parser = IPParser()
    ip = parser.feed(res.text)

    if not ip:
        raise Exception("failed to get ip")

    return ip, ac_id[0]


def get_user_info():
    """获取当前登录用户信息

    Returns:
        - tuple[bool, str|None]: is_logged_in, username
    """

    is_logged_in = True
    username = None

    resp = requests.get(API_BASE + "/cgi-bin/rad_user_info")
    data = resp.text

    if data == "not_online_error":
        is_logged_in = False
    else:
        username = data.split(",")[0]

    return is_logged_in, username


def fkbase64(raw_s: str) -> str:
    """base64掩码加密
    
    Returns:
        - str: encoded string
    """
    trans = str.maketrans(
        "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/",
        "LVoJPiCN2R8G90yg+hmFHuacZ1OWMnrsSTXkYpUq/3dlbfKwv6xztjI7DeBE45QA",
    )
    ret = b64encode(bytes(ord(i) & 0xFF for i in raw_s))
    return ret.decode().translate(trans)


def xencode(msg, key):
    """这是碰都不能碰的函数

    Returns:
        - str: 看不懂
    """
    def sencode(msg, key):
        def ordat(msg, idx):
            if len(msg) > idx:
                return ord(msg[idx])
            return 0

        msg_len = len(msg)
        pwd = []
        for i in range(0, msg_len, 4):
            pwd.append(ordat(msg, i) | ordat(msg, i + 1) << 8 |
                       ordat(msg, i + 2) << 16 | ordat(msg, i + 3) << 24)
        if key:
            pwd.append(msg_len)
        return pwd

    def lencode(msg, key):
        msg_len = len(msg)
        ll = (msg_len - 1) << 2
        if key:
            m = msg[msg_len - 1]
            if m < ll - 3 or m > ll:
                return ""
            ll = m
        for i in range(0, msg_len):
            msg[i] = chr(msg[i] & 0xFF) + chr(msg[i] >> 8 & 0xFF) + \
                chr(msg[i] >> 16 & 0xFF) + chr(msg[i] >> 24 & 0xFF)
        if key:
            return "".join(msg)[0:ll]
        return "".join(msg)

    if msg == "":
        return ""
    pwd = sencode(msg, True)
    pwdk = sencode(key, False)
    if len(pwdk) < 4:
        pwdk = pwdk + [0] * (4 - len(pwdk))
    n = len(pwd) - 1
    z = pwd[n]
    y = pwd[0]
    c = 0x86014019 | 0x183639A0
    m = 0
    e = 0
    d = 0
    p = 0
    q = math.floor(6 + 52 / (n + 1))
    while 0 < q:
        d = d + c & (0x8CE0D9BF | 0x731F2640)
        e = d >> 2 & 3
        p = 0
        while p < n:
            y = pwd[p + 1]
            m = z >> 5 ^ y << 2
            m = m + ((y >> 3 ^ z << 4) ^ (d ^ y))
            m = m + (pwdk[(p & 3) ^ e] ^ z)
            pwd[p] = pwd[p] + m & (0xEFB8D130 | 0x10472ECF)
            z = pwd[p]
            p = p + 1
        y = pwd[0]
        m = z >> 5 ^ y << 2
        m = m + ((y >> 3 ^ z << 4) ^ (d ^ y))
        m = m + (pwdk[(p & 3) ^ e] ^ z)
        pwd[n] = pwd[n] + m & (0xBB390742 | 0x44C6F8BD)
        z = pwd[n]
        q = q - 1
    return lencode(pwd, False)


def main() -> None:
    """读取命令，分析参数，回报执行状态

    Returns:
        - None
    """
    USNM, PSWD = read_config()
    parser = argparse.ArgumentParser(description="Login to BIT network")
    parser.add_argument(
        "-a", "--action",
        choices=["login", "logout", "登录", "登陆", "上线", "登出", "下线", "退出"],
        help="login or logout"
    )

    # sys.argv.append("-a")
    # sys.argv.append("LOGin")

    for arg in sys.argv:
        sys.argv[sys.argv.index(arg)]=arg.lower()
    args = parser.parse_args()

    try:
        if str(args.action) in ["login", "登录", "登陆", "上线"]:
            while 1:
                user = User(USNM, PSWD)
                res = user.log_action(Action.LOGIN)
                if res.get('error_msg')=="Password is error.":
                    print(f"[{report_time()}] 密码错误，请重新输入账号密码")
                    write_config()
                else:
                    break
            print(f"[{report_time()}] 用户{res.get('username')} IP({res.get('online_ip')}) 登录成功")
        elif str(args.action) in ["logout", "登出", "下线", "退出"]:
            while 1:
                user = User(USNM, PSWD)
                res = user.log_action(Action.LOGOUT)
                if res.get('error_msg')=="Password is error.":
                    print(f"[{report_time()}] 密码错误，请重新输入账号密码")
                    write_config()
                else:
                    break
            print(
                f"[{report_time()}] 用户{res.get('username')} IP({res.get('online_ip')}) 现已登出"
                )

        else:
            raise UnreachableError(f"[Cannot Resolve Para]{args.action}")

    except UnreachableError as e:
        print(e)
        exit(1)

    except Exception as e:
        print(e)
        exit(2)

    except KeyboardInterrupt:
        print(f"[{report_time()}] 手动退出")
        exit(3)

    exit(0)


if __name__ == "__main__":
    os.system("chcp 65001>nul")
    os.chdir(sys.path[0])
    main()
