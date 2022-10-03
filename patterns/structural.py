# Декоратор, структурный паттерн
import inspect
import logging
from time import time

from log.log_config import LOGGER


class Router:
    def __init__(self, routes, url):
        self.routes = routes
        self.url = url

    def __call__(self, cls):
        self.routes[self.url] = cls()


class Debug:
    def __init__(self, name):
        self.name = name

    def __call__(self, cls):
        def timeit(method):
            def timed(*args, **kwargs):
                start_time = time()
                result = method(*args, **kwargs)
                delta = start_time - time()

                LOGGER.debug(f'{self.name} ran for {delta:2.2f} ms')
                return result

            return timed

        return timeit(cls)

# class Log:
#     def __init__(self, func):
#         self.func = func
#
#     def __call__(self, *args, **kwargs):
#         code_object_name = inspect.currentframe().f_back.f_code.co_name
#
#         logger = logging.getLogger('Log_file.log')
#         logger.info(f'Function {self.func.__name__} is called from method {code_object_name}')
#
#         return self.func(*args, **kwargs)
