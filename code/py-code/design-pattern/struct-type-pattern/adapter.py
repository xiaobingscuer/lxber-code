#!/usr/bin/python
# coding=utf-8

"""
1. 解决实现两个不兼容接口之间的兼容
2. 遵从开放/封闭原则
3. 适配器让一件产品在制造出来之后需要应对新需求之时还能工作，
    无需修改不兼容模型的源代码就能获得接口的一致性

"""


class Target(object):
    def request(self):
        print("普通请求")


class Adaptee(object):
    def specific_request(self):
        print("特殊请求")


class Adapter(Target):

    def __init__(self):
        self.adaptee = Adaptee()

    def request(self):
        self.adaptee.specific_request()


if __name__ == "__main__":
    target = Adapter()
    target.request()

