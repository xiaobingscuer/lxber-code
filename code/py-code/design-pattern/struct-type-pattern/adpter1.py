#!/usr/bin/python
# coding=utf-8

"""
1. 解决实现两个不兼容接口之间的兼容
2. 遵从开放/封闭原则
3. 适配器让一件产品在制造出来之后需要应对新需求之时还能工作，
    无需修改不兼容模型的源代码就能获得接口的一致性
4. 虽然在Python中我们可以沿袭传统方式使用子类（继承）来实现适配器模式，
    但这种使用python内置字典的技术是一种很棒的替代方案。

"""


class External:
    class Synthesizer:
        def __init__(self, name):
            self.name = name

        def __str__(self):
            return 'the {} synthesizer'.format(self.name)

        def play(self):
            return 'is playing an electronic song'

    class Human:
        def __init__(self, name):
            self.name = name

        def __str__(self):
            return '{} the human'.format(self.name)

        def speak(self):
            return 'says hello'


class Computer:
    def __init__(self, name):
        self.name = name

    def __str__(self):
        return 'the {} computer'.format(self.name)

    def execute(self):
        return 'executes a program'


class Adapter:
    def __init__(self, obj, adapted_methods):
        self.obj = obj
        self.__dict__.update(adapted_methods)

    def __str__(self):
        return str(self.obj)


def main():
    objects = [Computer('Asus')]
    synth = External.Synthesizer('moog')
    objects.append(Adapter(synth, dict(execute=synth.play)))
    human = External.Human('Bob')
    objects.append(Adapter(human, dict(execute=human.speak)))
    for i in objects:
        print('{} {}'.format(str(i), i.execute()))


if __name__ == "__main__":
    main()
