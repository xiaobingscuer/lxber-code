#!/usr/bin/python
# coding=utf-8

"""
抽象工厂：
1. 与工厂模式类似，主要解决多个不同类型的工厂接口选择问题,同样遵循开闭原则
2. 抽象工厂是对不同类型的工厂的聚合，不同抽象工厂的实例具有相同的接口，只是实现方式不同
"""


class Phone:
    def __init__(self, type):
        print('phone type is {type}'.format(type=type))

    def display_movie(self, movie_name):
        print('the movie <<{movie_name}>> is displaying on the phone.'.format(movie_name=movie_name))


class Computer:
    def __init__(self, type):
        print('computer type is {type}'.format(type=type))

    def visitor_network(self, url):
        print('computer is visiting network {url}.'.format(url=url))


class ElectricFactory:
    """ 抽象工厂 """
    @staticmethod
    def make_phone(type):
        return Phone(type)

    @staticmethod
    def make_computer(type):
        return Computer(type)


if __name__=='__main__':
    electric_factory = ElectricFactory()
    phone = electric_factory.make_phone('Axon 20')
    phone.display_movie('yewen')

    computer = electric_factory.make_computer('Apple air')
    computer.visitor_network('www.baidu.com')

    pass