import threading
from typing import Callable


class _Thread(threading.Thread):    # px 线程类 继承 threading.Thread
    def __init__(self, func: Callable, daemon: bool, args, kwargs):
        super().__init__()  # px 父类init构造
        self.__func = func  # px 传进 __func 线程要执行的函数
        self.__args = args  # px __func 的参数 __args
        self.__kwargs = kwargs  # px __func 的参数 __kwargs
        self.res = None     # px res __func 返回值
        self.daemon = daemon    # px bool daemon
        self.done = False   # px done 一开始是 FALSE

    def run(self) -> None:  # px 线程创建后直接运行 run()
        self.res = self.__func(*self.__args, **self.__kwargs)   # px 跑 __func res接收返回值
        self.done = True    # px 跑完了 done 标为True


class _Promise(object):
    def __init__(self, thread: _Thread):
        self.__thread = thread
        self.__thread.start()

    def get(self):
        self.__thread.join()
        return self.__thread.res

    # property 作装饰器 done()获取只读属性 __thread.done
    @property
    def done(self):
        return self.__thread.done


# 装饰器: https://www.runoob.com/w3cnote/python-func-decorators.html
def go(daemon: bool = False):
    def decorator(func: Callable):
        def wrapper(*args, **kwargs) -> _Promise:
            return _Promise(_Thread(func, daemon, args, kwargs))

        return wrapper

    return decorator
