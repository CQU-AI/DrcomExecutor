import binascii
import random
import socket
import struct
import sys
import time

from DrcomExecutor.config import config
from DrcomExecutor.utils import md5sum, dump, checksum, ror

drcom_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
drcom_socket.bind(("0.0.0.0", 61440))
drcom_socket.settimeout(3)


def challenge(svr, ran):
    while True:
        t = struct.pack("<H", int(ran) % 0xFFFF)
        drcom_socket.sendto(b"\x01\x02" + t + b"\x09" + b"\x00" * 15, (svr, 61440))
        try:
            data, address = drcom_socket.recvfrom(1024)

        except Exception as e:
            raise e

        if address == (svr, 61440):
            break
        else:
            continue

    if data[:1] != b"\x02":
        raise Exception("challenge")

    return data[4:8]


def keep_alive_package_builder(number, tail, package_type=1, first=False):
    data = b"\x07" + bytes([number]) + b"\x28\x00\x0B" + bytes([package_type])
    if first:
        data += b"\x0F\x27"
    else:
        data += config["signal"]["keep_alive"]
    data += b"\x2F\x12" + b"\x00" * 6
    data += tail
    data += b"\x00" * 4

    if package_type == 3:
        foo = b"".join(
            [bytes([int(i)]) for i in config["cqu_server"]["host_ip"].split(".")]
        )

        crc = b"\x00" * 4

        data += crc + foo + b"\x00" * 8
    else:
        data += b"\x00" * 16
    return data


def keep_alive(*args):
    ran = random.randint(0, 0xFFFF)
    ran += random.randint(1, 10)

    svr_num = 0
    packet = keep_alive_package_builder(svr_num, b"\x00" * 4, 1, True)
    while True:
        # log("[keep-alive] send1", str(binascii.hexlify(packet))[2:][:-1])
        drcom_socket.sendto(packet, (config["cqu_server"]["server"], 61440))
        data, address = drcom_socket.recvfrom(1024)
        # log("[keep-alive] recv1", str(binascii.hexlify(data))[2:][:-1])
        if data.startswith(b"\x07\x00\x28\x00") or data.startswith(
            b"\x07" + bytes([svr_num]) + b"\x28\x00"
        ):
            break
        elif data[:1] == b"\x07" and data[2:3] == b"\x10":
            # log("[keep-alive] recv file, resending..")
            svr_num = svr_num + 1

            break
        else:
            pass

    for packet in (
        keep_alive_package_builder(svr_num, b"\x00" * 4, 1, False),
        keep_alive_package_builder(svr_num, data[16:20], 3, False),
    ):
        ran += random.randint(1, 10)
        drcom_socket.sendto(packet, (config["cqu_server"]["server"], 61440))
        while True:
            data, address = drcom_socket.recvfrom(1024)
            if data[:1] == b"\x07":
                svr_num = svr_num + 1
                break
            else:
                pass

    tail = data[16:20]

    i = svr_num
    while True:
        try:
            time.sleep(20)
            keep_alive1(*args)
            ran += random.randint(1, 10)
            packet = keep_alive_package_builder(i, tail, 1, False)
            drcom_socket.sendto(packet, (config["cqu_server"]["server"], 61440))
            data, address = drcom_socket.recvfrom(1024)
            tail = data[16:20]
            ran += random.randint(1, 10)
            packet = keep_alive_package_builder(i + 1, tail, 3, False)
            drcom_socket.sendto(packet, (config["cqu_server"]["server"], 61440))

            data, address = drcom_socket.recvfrom(1024)

            tail = data[16:20]
            i = (i + 2) % 127
        except:
            pass


def keep_alive1(salt, tail, pwd, server):
    foo = struct.pack("!H", int(time.time()) % 0xFFFF)
    data = b"\xff" + md5sum(b"\x03\x01" + salt + pwd.encode()) + b"\x00\x00\x00"
    data += tail
    data += foo + b"\x00\x00\x00\x00"

    drcom_socket.sendto(data, (server, 61440))
    while True:
        data, address = drcom_socket.recvfrom(1024)
        if data[:1] == b"\x07":
            break
        else:
            pass


def make_packet(salt, usr, pwd, mac):
    data = b"\x03\x01\x00" + bytes([len(usr) + 20])
    data += md5sum(b"\x03\x01" + salt + pwd.encode())
    data += (usr.encode() + 36 * b"\x00")[:36]
    data += config["signal"]["control_check"]
    data += config["signal"]["adapter_num"]
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
    data += config["signal"]["ip_dog"]
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
    data += config["signal"]["auth"]
    if config["behavior"]["unlimited_retry"]:
        data += b"\x00"
        data += bytes([len(pwd)])
        data += ror(md5sum(b"\x03\x01" + salt + pwd), pwd)
    data += b"\x02"
    data += b"\x0C"
    data += checksum(data + b"\x01\x26\x07\x11\x00\x00" + dump(mac))
    data += b"\x00\x00"
    data += dump(mac)
    data += b"\x00"
    data += b"\x00"
    data += b"\xE9\x13"
    return data


def login(usr, pwd, server):
    i = 0
    while True:
        salt = challenge(server, time.time() + random.randint(0xF, 0xFF))
        packet = make_packet(salt, usr, pwd, config["cqu_server"]["mac"])

        drcom_socket.sendto(packet, (server, 61440))
        data, address = drcom_socket.recvfrom(1024)

        if address == (server, 61440):
            if data[:1] == b"\x04":
                break
            else:
                time.sleep(3)

        else:
            if i >= 5 and config["behavior"]["unlimited_retry"] == False:
                sys.exit(1)
            else:
                continue

    return data[23:39], salt


def empty_socket_buffer():
    try:
        while True:
            data, _ = drcom_socket.recvfrom(1024)
            if data == "":
                break
    except:
        pass
