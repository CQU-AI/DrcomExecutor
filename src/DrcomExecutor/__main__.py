import time
import traceback

from DrcomExecutor.config import config
from DrcomExecutor.core import empty_socket_buffer, keep_alive, login, keep_alive1
from DrcomExecutor.info import welcome
from DrcomExecutor.utils import check_user, reset_config
from DrcomExecutor.version import __version__


def main():
    username, password = check_user()
    server = config["cqu_server"]["server"]

    welcome(username, password)
    while True:
        try:
            tail, salt = login(username, password, server)
        except Exception as e:
            print(e)
            traceback.print_exc()
            time.sleep(30)
            continue
        empty_socket_buffer()
        keep_alive1(salt, tail, password, server)
        keep_alive(salt, tail, password, server)


def console_main():
    import argparse

    def parse_args() -> argparse.Namespace:
        """Parse the command line arguments for the `drcom executor` binary.

        :return: Namespace with parsed arguments.
        """
        parser = argparse.ArgumentParser(prog="de", description="第三方 重庆大学 Dr.COM 登录器", )

        parser.add_argument(
            "-v", "--version", action="version", version=f"DrcomExecutor {__version__}", help="显示版本号",
        )

        parser.add_argument(
            "-r", "--reset", help="重置配置项", action="store_true",
        )
        parser.add_argument(
            "-u",
            "--username",
            help="学号",
            type=int,
            default=config["user_info"]["username"],
        )
        parser.add_argument(
            "-p",
            "--password",
            help="密码",
            type=str,
            default=config["user_info"]["password"],
        )

        return parser.parse_args()

    args = parse_args()
    if args.reset:
        reset_config()

    config.dump()
