import binascii
import struct
from hashlib import md5

from DrcomExecutor.config import config, Config


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
        ret ^= int(binascii.hexlify(s[i : i + 4].ljust(4, b"\x00")[::-1]), 16)
    ret = (1968 * ret) & 0xFFFFFFFF
    return struct.pack("<I", ret)


def check_user():
    if (
        config["user_info"]["username"] is None
        or config["user_info"]["password"] is None
    ):
        print("未找到有效的帐号和密码，请输入你的上网帐号和密码，它们将被保存在你的电脑上以备下次使用")
        config["user_info"]["username"] = input("帐号>>>")
        config["user_info"]["password"] = input("密码>>>")
        config.dump()
    return config["user_info"]["username"], config["user_info"]["password"]


def ror(md5, pwd):
    ret = ""
    for i in range(len(pwd)):
        x = ord(md5[i]) ^ ord(pwd[i])
        ret += struct.pack("B", ((x << 3) & 0xFF) + (x >> 5))
    return ret


def reset_config():
    Config.reset()
    print("已重置配置文件")
