import threading
from functools import wraps
import time


def new_thread():
    def decorate(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            thread = threading.Thread(target=func, args=args, kwargs=kwargs)
            thread.start()

        return wrapper

    return decorate


if __name__ == "__main__":

    @new_thread()
    def greeting(name):
        print(f"你好啊，{name}！")
        time.sleep(3)
        print(f"再见了，{name}.")

    greeting("老张")
    greeting("小李")
    greeting("老刘")
