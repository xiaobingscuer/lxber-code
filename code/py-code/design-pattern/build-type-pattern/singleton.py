#!/usr/bin/python
# coding=utf-8

"""
单例设计模式：
1. 一个类只有一个实例，类实例只初始化一次
1. 提供全局访问点
"""

import time
import threading


class Singleton:
    """
    单例类
    """
    def __new__(cls, *args, **kwargs):
        if not hasattr(Singleton, "_instance"):
            Singleton._instance = super().__new__(cls)
        return Singleton._instance

    def __init__(self, *args, **kwargs):
        self.pt = 'private'
        time.sleep(1)
        pass
    pass


class SingletonGet:
    """
    单例类
    """
    _instance_lock = threading.Lock()

    def __init__(self, *args, **kwargs):
        time.sleep(1)
        pass

    @classmethod
    def get_instance(cls, *args, **kwargs):
        if not hasattr(SingletonGet, '_instance'):
            with SingletonGet._instance_lock:
                if not hasattr(SingletonGet, '_instance'):
                    SingletonGet._instance = SingletonGet(*args, **kwargs)
        return SingletonGet._instance

    pass


def singleton(cls):
    """
    单例包装器
    """
    # 单下划线的作用是这个变量只能在当前模块里访问,仅仅是一种提示作用
    # 创建一个字典用来保存类的实例对象
    # 多线程下不是单例？
    _instance = {}

    def _singleton(*args, **kwargs):
        # 先判断这个类有没有对象
        if cls not in _instance:
            # 创建一个对象,并保存到字典当中
            _instance[cls] = cls(*args, **kwargs)
        # 将实例对象返回
        return _instance[cls]

    return _singleton


@singleton
class SingletonWrapper:
    def __init__(self, x):
        self.x = x
        time.sleep(1)
    pass


class SimpleSingletonFactory:
    def __init__(self, instance_type):
        self.instance_type = instance_type

    def create_singleton_instance(self, *args):
        if self.instance_type == 'singleton_new':
            return Singleton()

        if self.instance_type == 'singleton_get':
            return SingletonGet.get_instance()

        if self.instance_type == 'singleton_wrapper':
            return SingletonWrapper(*args)
    pass


class RunDemo:
    """
    演示执行类
    """
    def __init__(self, thread_num=10):
        self.thread_num = thread_num

    @staticmethod
    def task(index, instance_type):
        singleton_instance = SimpleSingletonFactory(instance_type).create_singleton_instance(index)
        print(id(singleton_instance))

    def run(self, instance_type):
        for i in range(self.thread_num):
            t = threading.Thread(target=self.task, args=(i, instance_type))
            t.start()
        print("xxx")
        pass
    pass


if __name__ == "__main__":
    RunDemo().run("singleton_wrapper")
    pass
