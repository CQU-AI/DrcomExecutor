import binascii
import struct
import sys
import time
import traceback
from datetime import datetime
from hashlib import md5

from DrcomExecutor.config import config, Config

ERROR_COUNT = 0


def exit():
    print("[{}]  遭遇不可抗的错误，程序完全退出".format(datetime.now()))
    sys.exit(1)


def md5sum(s):
    m = md5()
    m.update(s)
    return m.digest()


def dump(n):
    s = "%x" % n
    if len(s) & 1:
        s = "0" + s
    return binascii.unhexlify(bytes(s, "ascii"))


def checksum(s):
    ret = 1234
    for i in [x * 4 for x in range(0, -(-len(s) // 4))]:
        ret ^= int(binascii.hexlify(s[i: i + 4].ljust(4, b"\x00")[::-1]), 16)
    ret = (1968 * ret) & 0xFFFFFFFF
    return struct.pack("<I", ret)


def check_user():
    if (
            config["user_info"]["username"] is None
            or config["user_info"]["password"] is None
    ):
        print("未找到有效的帐号和密码，请输入你的上网帐号和密码，它们将被保存在你的电脑上以备下次使用")
        try:
            config["user_info"]["username"] = input("帐号>>>")
            config["user_info"]["password"] = input("密码>>>")
        except (KeyboardInterrupt, EOFError):
            log("需要输入你的上网帐号和密码，它们将被保存在你的电脑上以备下次使用")
            exit()
        config.dump()
    return config["user_info"]["username"], config["user_info"]["password"]


def ror(md5, pwd):
    ret = b""
    for i in range(len(pwd)):
        x = md5[i] ^ ord(pwd[i])
        ret += bytes(((x << 3) & 0xFF) + (x >> 5))
    return ret


def reset_config():
    Config.reset()
    print("已重置配置文件")


def log(msg, error=False, warning=False):
    global ERROR_COUNT
    if error:
        print("[{}]  {} - {}".format(datetime.now(), msg, ERROR_COUNT))
        if config["behavior"]["print_traceback"]:
            traceback.print_exc()
        time.sleep(min(2 ** ERROR_COUNT, config["behavior"]["exp_backoff_limit"]))
        ERROR_COUNT += 1
    elif warning:
        print("[{}]  {}".format(datetime.now(), msg))
    else:
        print("[{}]  {}".format(datetime.now(), msg))
        reset_error_count()


def reset_error_count():
    global ERROR_COUNT
    ERROR_COUNT = 0
