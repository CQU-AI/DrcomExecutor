from DrcomExecutor.config import config
from DrcomExecutor.core import empty_socket_buffer, keep_alive, login
from DrcomExecutor.info import welcome
from DrcomExecutor.utils import check_user


def main():
    username, password = check_user()
    server = config["cqu_server"]["server"]

    welcome(username, password)
    while True:
        try:
            package_tail, salt = login(username, password, server)
        except Exception:
            continue
        empty_socket_buffer()
        keep_alive(salt, package_tail, password, server)


main()
