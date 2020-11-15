#!/usr/bin/python
# coding=utf-8

"""
状态机模式

1. 解决 所有可以使用状态机解决的问题都是不错的状态模式应用，本质上相当于实现一个状态机来解决特定领域的一个软件问题

2. 状态机是一个抽象机器，具有两个主要部分：状态和转换。状态是指一个系统的当前状况。
    一个状态机在任意时间点只会有一个激活状态。转换是指从当前状态到一个新状态的切换。在一
    个转换发生之前或之后通常会执行一个或多个动作。状态机可以使用状态图进行视觉上的展现

菜鸟教程中的策略模式与状态模式的区别那边文章讲的很清楚
"""

from abc import ABCMeta, abstractmethod


class Bike(object):
    def __init__(self):
        self.gearState = FirstGear(self)

    def gear_up(self):
        self.gearState.gear_up()

    def gear_down(self):
        self.gearState.gear_down()


class GearState(metaclass=ABCMeta):
    def __init__(self, bike):
        self.bike = bike

    @abstractmethod
    def gear_up(self):
        pass

    @abstractmethod
    def gear_down(self):
        pass


class FirstGear(GearState):
    def __init__(self, bike):
        super().__init__(bike)

    def gear_up(self):
        print('moving up  from first to second gear.')
        self.bike.gearState = SecondGear(self.bike)

    def gear_down(self):
        print('already in first gear, cannot moving down.')


class SecondGear(GearState):
    def __init__(self, bike):
        super().__init__(bike)

    def gear_up(self):
        print('moving up from second to third gear.')
        self.bike.gearState = ThirdGear(self.bike)

    def gear_down(self):
        print('moving down from second to first gear.')
        self.bike.gearState = FirstGear(self.bike)


class ThirdGear(GearState):
    def __init__(self, bike):
        super().__init__(bike)

    def gear_up(self):
        print('already in third gear, cannot moving up.')

    def gear_down(self):
        print('moving down from third to second gear.')
        self.bike.gearState = SecondGear(self.bike)


def main():
    bike = Bike()
    bike.gear_down()
    bike.gear_up()
    bike.gear_up()
    bike.gear_up()
    bike.gear_up()
    bike.gear_down()
    bike.gear_down()
    bike.gear_down()


if __name__ == '__main__':
    main()
