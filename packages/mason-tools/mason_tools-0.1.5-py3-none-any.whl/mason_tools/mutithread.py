from concurrent.futures import ThreadPoolExecutor
from multiprocessing import cpu_count
from functools import wraps


class Mutithread:
    """
    多线程装饰器(线程池实现)
    """

    maxthreads = cpu_count() * 2

    def __init__(self, max_workers=None):
        """初始化线程池"""
        if not max_workers:
            max_workers = self.maxthreads
        self.executor = ThreadPoolExecutor(max_workers=cpu_count() * 2)

    def to_pool(self):
        """装饰器函数"""

        def decorate(func):
            @wraps(func)
            def wrapper(*args, **kwargs):
                return self.executor.submit(func, *args, **kwargs)

            return wrapper

        return decorate

    def close(self):
        self.executor.shutdown()
