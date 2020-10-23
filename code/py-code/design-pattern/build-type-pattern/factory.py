#!/usr/bin/python
# coding=utf-8

"""
工厂方法模式：
1. 主要解决：主要解决接口选择的问题。
2. 何时使用：我们明确地计划可在不同条件下选择（创建）某一抽象类型下不同子类的实例时。
3. 优点：符合开闭原则，对已有代码修改进行关闭，对扩展开放。代码可扩展可维护。
4.      比如新增加一个类型，只需新增加该类型新的子类
"""


class Person(object):
    """ 人 """
    def __init__(self, name, sex):
        self.name = name
        self.sex = sex

    @property
    def get_name(self):
        return self.name

    @property
    def get_sex(self):
        return self.sex

    def print_info(self):
        print('my name is {name}, my sex is {sex}'.format(name=self.name, sex=self.sex))


class Male(Person):
    """ 男性 """
    def __init__(self, name):
        super().__init__(name, 'Male')
        print('male, name is {name}'.format(name=self.name))


class Female(Person):
    """ 女性 """
    def __init__(self, name):
        super().__init__(name, 'Female')
        print('female, name is {name}'.format(name=self.name))


def person_factory(name, sex_type):
    """ 工厂 """
    if sex_type == 'm':
        return Male(name)
    elif sex_type == 'f':
        return Female(name)
    else:
        print('other sex will be supported!')
        return Person(name, 'Other')


if __name__ == '__main__':

    person = person_factory('lxb', 'm')
    person.print_info()

    person = person_factory('xiaoxue', 'f')
    person.print_info()

    pass
