import re
from typing import Dict
from urllib import parse

import requests
from bs4 import BeautifulSoup

from DrcomExecutor.config import config


def welcome(sid: str, passwd: str):
    print(
        """
      _____                          ______                     _
     |  __ \                        |  ____|                   | |
     | |  | |_ __ ___ ___  _ __ ___ | |__  __  _____  ___ _   _| |_ ___  _ __
     | |  | | '__/ __/ _ \| '_ ` _ \|  __| \ \/ / _ \/ __| | | | __/ _ \| '__|
     | |__| | | | (_| (_) | | | | | | |____ >  <  __/ (__| |_| | || (_) | |
     |_____/|_|  \___\___/|_| |_| |_|______/_/\_\___|\___|\__,_|\__\___/|_|
    """
    )

    if config["behavior"]["info"]:
        info = get_account_details(sid, passwd)
        print(
            "\n".join(
                [
                    "".join(["账号　　　　", "  -  ", info["账号"]]),
                    "".join(["姓名　　　　", "  -  ", info["姓名"]]),
                    "".join(["套餐组　　　", "  -  ", info["套餐组"]]),
                    "".join(["使用时长　　", "  -  ", info["使用时长"]]),
                    "".join(["使用流量　　", "  -  ", info["使用流量"]]),
                    "".join(["预存款余额　", "  -  ", info["预存款余额"]]),
                    "".join(["本月实用费用", "  -  ", info["本月实用费用"]]),
                    "".join(["账户实际余额", "  -  ", info["账户实际余额"]]),
                ]
            )
        )


def get_account_details(sid: str, passwd: str) -> Dict[str, str]:
    """
    从 user.cqu.edu.cn 获取用户信息
    :param sid: 学号
    :param passwd: 密码
    :return: 用户信息
    """
    session = requests.Session()

    # Get authenticity token
    response = session.get("http://user.cqu.edu.cn/login/sign_in")
    token = re.findall('<meta content=".*" name="csrf-token" />', response.text)[0][
        15:-22
    ]

    # Prepare HTTP package
    headers = {
        "Content-Type": "application/x-www-form-urlencoded;charset=utf-8",
        "User-Agent": "Mozilla/5.0.html (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko)",
    }
    data = parse.urlencode(
        {
            "utf8": "\342\234\223",
            "authenticity_token": token,
            "account_num": sid,
            "inputtext": "password",
            "account_pass": passwd,
        }
    )

    # Send login form
    session.post("http://user.cqu.edu.cn/t_account/check", headers=headers, data=data)

    # Get account details
    page = session.get("http://user.cqu.edu.cn/userbaseinfo")
    soup = BeautifulSoup(page.content, features="html.parser")
    p1s = soup.find_all(id="p1")
    p2s = soup.find_all(id="p2")
    rtn = {p1s[i].text: p2s[i].text for i in range(len(p1s))}
    return rtn
