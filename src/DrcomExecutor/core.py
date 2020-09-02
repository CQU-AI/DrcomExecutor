import binascii
import random
import socket
import struct
import sys
import time

from DrcomExecutor.config import config
from DrcomExecutor.utils import (
    md5sum,
    dump,
    checksum,
    ror,
    log,
    reset_error_count,
    exit,
)


def build_heartbeat_packet(number, tail, package_type=1, first=False) -> bytes:
    data = b"\x07" + bytes([number]) + b"\x28\x00\x0B" + bytes([package_type])
    data += b"\x0F\x27" if first else config["signal"]["keep_alive"].encode("utf-8")
    data += b"\x2F\x12" + b"\x00" * 6 + tail + b"\x00" * 4

    if package_type == 3:
        foo = b"".join(
            [bytes([int(i)]) for i in config["cqu_server"]["host_ip"].split(".")]
        )
        crc = b"\x00" * 4
        data += crc + foo + b"\x00" * 8
    else:
        data += b"\x00" * 16
    return data


def make_packet(salt, usr, pwd, mac):
    data = b"\x03\x01\x00" + bytes([len(usr) + 20])
    data += md5sum(b"\x03\x01" + salt + pwd.encode())
    data += (usr.encode() + 36 * b"\x00")[:36]
    data += config["signal"]["control_check"].encode("utf-8")
    data += config["signal"]["adapter_num"].encode("utf-8")
    data += dump(int(binascii.hexlify(data[4:10]), 16) ^ mac)[-6:]
    data += md5sum(b"\x01" + pwd.encode() + salt + b"\x00" * 4)
    data += b"\x01"
    data += b"".join(
        [bytes([int(i)]) for i in config["cqu_server"]["host_ip"].split(".")]
    )
    data += b"\00" * 4
    data += b"\00" * 4
    data += b"\00" * 4
    data += md5sum(data + b"\x14\x00\x07\x0B")[:8]
    data += config["signal"]["ip_dog"].encode("utf-8")
    data += b"\x00" * 4
    data += (config["cqu_server"]["host_name"].encode() + 32 * b"\x00")[:32]
    data += b"".join(
        [bytes([int(i)]) for i in config["cqu_server"]["primary_dns"].split(".")]
    )
    data += b"".join(
        [bytes([int(i)]) for i in config["cqu_server"]["dhcp_server"].split(".")]
    )
    data += b"\x00\x00\x00\x00"
    data += b"\x00" * 4
    data += b"\x00" * 4
    data += b"\x94\x00\x00\x00"
    data += b"\x05\x00\x00\x00"
    data += b"\x01\x00\x00\x00"
    data += b"\x28\x0A\x00\x00"
    data += b"\x02\x00\x00\x00"
    data += (config["cqu_server"]["host_os"].encode() + 32 * b"\x00")[:32]
    data += b"\x00" * 96
    data += config["signal"]["auth"].encode("utf-8")
    if config["behavior"]["unlimited_retry"]:
        data += b"\x00"
        data += bytes([len(pwd)])
        data += ror(md5sum(b"\x03\x01" + salt + pwd.encode("utf-8")), pwd)
    data += b"\x02"
    data += b"\x0C"
    data += checksum(data + b"\x01\x26\x07\x11\x00\x00" + dump(mac))
    data += b"\x00\x00"
    data += dump(mac)
    data += b"\x00"
    data += b"\x00"
    data += b"\xE9\x13"
    return data


class DrcomCore:
    def __init__(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        try:
            self.socket.bind(("0.0.0.0", 61440))
        except OSError:
            log("绑定端口失败，是否有其他drcom正在运行？")
            exit()
        self.socket.settimeout(3)

    def __main__(self):
        username = config["user_info"]["username"]
        password = config["user_info"]["password"]
        server = config["cqu_server"]["server"]

        while True:
            try:
                tail, salt = self.login(username, password, server)
            except Exception as e:
                log("登录失败 " + str(e), error=True)
                continue

            # 体面的退出
            try:
                self.empty_socket_buffer()
                self.keep_alive1(salt, tail, password)
                self.keep_alive(salt, tail, password, server)
            except KeyboardInterrupt:
                log("de已完全退出，再见！")
                sys.exit()

    def challenge(self, svr, ran):
        while True:
            t = struct.pack("<H", int(ran) % 0xFFFF)
            self.socket.sendto(b"\x01\x02" + t + b"\x09" + b"\x00" * 15, (svr, 61440))
            try:
                data, address = self.socket.recvfrom(1024)
            except Exception:
                log("尝试与服务器通信失败，物理连接可能出现问题", error=True)
                continue

            if address == (svr, 61440) and data[:1] == b"\x02":
                break
            else:
                log("尝试与服务器通信时发生未知错误", error=True)
                continue
        return data[4:8]

    def send_heartbeat_packet(self, packet, check_start=False) -> bytes:
        heartbeat_error_count = 0
        while True:
            self.socket.sendto(packet, (config["cqu_server"]["server"], 61440))

            if heartbeat_error_count > 10:
                if config['behavior']['unlimited_retry']:
                    raise ConnectionResetError("重新登录")
                else:
                    exit()
            try:
                data, _ = self.socket.recvfrom(1024)
            except socket.timeout:
                log("心跳包发送失败，是否在其他地方登录？", warning=True)
                time.sleep(3)
                heartbeat_error_count += 1

                continue

            if check_start is True:
                if not data.startswith(b"\x07"):
                    log("心跳包发送失败", warning=True)
                    time.sleep(3)
                    heartbeat_error_count += 1

                    continue

            return data[16:20]

    def keep_alive(self, salt, ptail, password, server):
        _ = self.send_heartbeat_packet(
            build_heartbeat_packet(0, b"\x00" * 4, 1, True), check_start=True
        )

        i = 1
        tail = b"\x00" * 4
        for j in (1, 3):
            tail = self.send_heartbeat_packet(
                build_heartbeat_packet(i, tail, j, False), check_start=True
            )
            i += 1

        while True:
            try:
                time.sleep(20)
                self.keep_alive1(salt, ptail, password)
                for j in (1, 3):
                    tail = self.send_heartbeat_packet(
                        build_heartbeat_packet(i, tail, j, False), check_start=False
                    )
                    i = (i + 1) % 127

                socket.gethostbyname("www.taobao.com")
                reset_error_count()

            except Exception:
                log("网络断开，尝试重新登陆", error=True)
                return

    def keep_alive1(self, salt, tail, pwd):
        foo = struct.pack("!H", int(time.time()) % 0xFFFF)
        data = b"\xff" + md5sum(b"\x03\x01" + salt + pwd.encode()) + b"\x00\x00\x00"
        data += tail + foo + b"\x00\x00\x00\x00"
        self.send_heartbeat_packet(data, check_start=True)

    def login(self, usr, pwd, server):
        i = 1
        while True:
            salt = self.challenge(server, time.time() + random.randint(0xF, 0xFF))
            packet = make_packet(salt, usr, pwd, config["cqu_server"]["mac"])

            self.socket.sendto(packet, (server, 61440))
            data, address = self.socket.recvfrom(1024)

            if address == (server, 61440) and data[:1] == b"\x04":
                log("登录成功")
                break
            else:
                log(f"登录失败", error=True)
                i += 1
                if i >= 6 and config["behavior"]["unlimited_retry"] is False:
                    print("登录失败次数过多，程序终止")
                    exit()
                time.sleep(3)

        return data[23:39], salt

    def empty_socket_buffer(self):
        try:
            while True:
                data, _ = self.socket.recvfrom(1024)
                if data == "":
                    break
        except:
            return
