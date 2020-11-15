#!/usr/bin/python
# coding=utf-8

"""
外观模式

1. 解决 使用外观模式的最常见理由是为一个复杂系统提供单个简单的入口点

问题：
    系统会随着演化变得非常复杂，最终形成大量的（并且有时是令人迷惑的）类和交互，这种情况并不少见。
    许多情况下，我们并不想把这种复杂性暴露给客户端。
    外观设计模式有助于隐藏系统的内部复杂性，并通过一个简化的接口向客户端暴露必要的部分。
    本质上，外观（Facade）是在已有复杂系统之上实现的一个抽象层。

问题：
    如果你的系统包含多层，外观模式也能派上用场。你可以为每一层引入一个外观入口点，
    并让所有层级通过它们的外观相互通信。这提高了层级之间的松耦合性，尽可能保持层级独立

"""

from enum import Enum
from abc import ABCMeta, abstractmethod

State = Enum('State', 'new running sleeping restart zombie')


class User:
    pass


class Process:
    pass


class File:
    pass


class Server(metaclass=ABCMeta):
    @abstractmethod
    def __init__(self):
        pass

    def __str__(self):
        return self.name

    @abstractmethod
    def boot(self):
        pass

    @abstractmethod
    def kill(self, restart=True):
        pass


class FileServer(Server):
    def __init__(self):
        '''初始化文件服务进程要求的操作'''
        self.name = 'FileServer'
        self.state = State.new

    def boot(self):
        print('booting the {}'.format(self))
        '''启动文件服务进程要求的操作'''
        self.state = State.running

    def kill(self, restart=True):
        print('Killing {}'.format(self))
        '''终止文件服务进程要求的操作'''
        self.state = State.restart if restart else State.zombie

    def create_file(self, user, name, permissions):
        '''检查访问权限的有效性、用户权限等'''
        print("trying to create the file '{}' for user '{}' with permissions{}".format(name, user, permissions))


class ProcessServer(Server):
    def __init__(self):
        '''初始化进程服务进程要求的操作'''
        self.name = 'ProcessServer'
        self.state = State.new

    def boot(self):
        print('booting the {}'.format(self))
        '''启动进程服务进程要求的操作'''
        self.state = State.running

    def kill(self, restart=True):
        print('Killing {}'.format(self))
        '''终止进程服务进程要求的操作'''
        self.state = State.restart if restart else State.zombie

    def create_process(self, user, name):
        '''检查用户权限和生成PID等'''
        print("trying to create the process '{}' for user '{}'".format(name, user))


class WindowServer:
    pass


class NetworkServer:
    pass


class OperatingSystem:
    '''外观'''

    def __init__(self):
        self.fs = FileServer()
        self.ps = ProcessServer()

    def start(self):
        [i.boot() for i in (self.fs, self.ps)]

    def create_file(self, user, name, permissions):
        return self.fs.create_file(user, name, permissions)

    def create_process(self, user, name):
        return self.ps.create_process(user, name)


def main():
    os = OperatingSystem()
    os.start()
    os.create_file('foo', 'hello', '-rw-r-r')
    os.create_process('bar', 'ls /tmp')


if __name__ == '__main__':
    main()
