import time
import traceback

from DrcomExecutor.config import config
from DrcomExecutor.core import empty_socket_buffer, keep_alive, login, keep_alive1
from DrcomExecutor.info import welcome
from DrcomExecutor.utils import check_user




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

if __name__ == '__main__':
    main()