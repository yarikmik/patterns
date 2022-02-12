from memory_profiler import profile, memory_usage
from timeit import default_timer
import inspect


class UrlRoute:
    def __init__(self, routes, url):
        self.routes = routes
        self.url = url

    def __call__(self, cls):
        self.routes[self.url] = cls()


class Debug:
    # def __init__(self, name):
    #     self.name = name

    def __call__(self, cls):
        def decor(method):
            """декортатор для замеров времени и памяти из курса алгоритмов"""

            def wrapper(*args, **kwargs):
                t1 = default_timer()
                m1 = memory_usage()
                res = method(*args, **kwargs)
                m2 = memory_usage()
                t2 = default_timer()
                mem_diff = m2[0] - m1[0]
                time_dif = t2 - t1
                _stack = inspect.stack()[1]
                print(f'Функция - {method.__name__}\n Время заняло: {time_dif}\n Памяти заняло:{mem_diff}\n'
                      f'cls:, {_stack[0].f_locals["self"].__class__.__name__}, func:, {_stack[3]}\n')
                return res

            return wrapper

        return decor(cls)
