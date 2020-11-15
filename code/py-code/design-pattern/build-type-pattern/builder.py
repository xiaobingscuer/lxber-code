#!/usr/bin/python
# coding=utf-8

"""
构造器模式：
1. 我们想要创建一个由多个部分构成的对象，而且它的构成需要一步接一步地完成。
    只有当各个部分都创建好，这个对象才算是完整的。这正是建造者设计模式（Builder design
    pattern）的用武之地。

2. 建造者模式将一个复杂对象的构造过程与其表现分离，这样，同一个构造过程可用于创建多个不同的表现

3. 到建造者模式也可用于解决可伸缩构造函数问题。
    当我们为支持不同的对象创建方式而不得不创建一个新的构造函数时，可伸缩构造函数问题就发生了，
    这种情况最终产生许多构造函数和长长的形参列表，难以管理。
    除了使用构造器模式，在python中可以使用 命名形参 以及 实参列表展开 来避免

4. 链式地调用建造者方法，通过将建造者本身定义为内部类并从其每个设置器方法返回自身来实现。
    方法build()返回最终的对象。这个模式被称为流利的建造者。

5. 建造者模式和工厂模式的差别并不太明确。主要的区别在于：
    1）工厂模式以单个步骤创建对象，而建造者模式以多个步骤创建对象，并且几乎始终会使用一个指挥者。
    2） 在工厂模式下，会立即返回一个创建好的对象；而在建造者模式下，仅在需要时客户端代码才显式地请求指挥者返回最终的对象

6. 在以下几种情况下，与工厂模式相比，建造者模式是更好的选择。
    1）想要创建一个复杂对象（对象由多个部分构成，且对象的创建要经过多个不同的步骤，这些步骤也许还需遵从特定的顺序）
    2）要求一个对象能有不同的表现，并希望将对象的构造与表现解耦
    3）想要在某个时间点创建对象，但在稍后的时间点再访问

"""

from enum import Enum
import time

PizzaProgress = Enum('PizzaProgress', 'queued preparation baking ready')
PizzaDough = Enum('PizzaDough', 'thin thick')
PizzaSauce = Enum('PizzaSauce', 'tomato creme_fraiche')
PizzaTopping = Enum('PizzaTopping', 'mozzarella double_mozzarella bacon ham mushroomsred_onion oregano')
STEP_DELAY = 3  # 考虑到这是示例，单位为秒


class Pizza:
    """ 实体类 """

    def __init__(self, name):
        self.name = name
        self.dough = None
        self.sauce = None
        self.topping = []

    def __str__(self):
        return self.name

    def prepare_dough(self, dough):
        self.dough = dough
        print('preparing the {} dough of your {}...'.format(self.dough.name, self))
        time.sleep(STEP_DELAY)
        print('done with the {} dough'.format(self.dough.name))


class MargaritaBuilder:
    """ 构造器 """

    def __init__(self):
        self.pizza = Pizza('margarita')
        self.progress = PizzaProgress.queued
        self.baking_time = 5  # 考虑是示例，单位为秒

    def prepare_dough(self):
        self.progress = PizzaProgress.preparation
        self.pizza.prepare_dough(PizzaDough.thin)

    def add_sauce(self):
        print('adding the tomato sauce to your margarita...')
        self.pizza.sauce = PizzaSauce.tomato
        time.sleep(STEP_DELAY)
        print('done with the tomato sauce')

    def add_topping(self):
        print('adding the topping (double mozzarella, oregano) to your margarita')
        self.pizza.topping.append([i for i in
                                   (PizzaTopping.double_mozzarella, PizzaTopping.oregano)])
        time.sleep(STEP_DELAY)
        print('done with the topping (double mozzarrella, oregano)')

    def bake(self):
        self.progress = PizzaProgress.baking
        print('baking your margarita for {} seconds'.format(self.baking_time))
        time.sleep(self.baking_time)
        self.progress = PizzaProgress.ready
        print('your margarita is ready')


class CreamyBaconBuilder:
    """ 构造器 """

    def __init__(self):
        self.pizza = Pizza('creamy bacon')
        self.progress = PizzaProgress.queued
        self.baking_time = 7  # 考虑是示例，单位为秒

    def prepare_dough(self):
        self.progress = PizzaProgress.preparation
        self.pizza.prepare_dough(PizzaDough.thick)

    def add_sauce(self):
        print('adding the crème fraîche sauce to your creamy bacon')
        self.pizza.sauce = PizzaSauce.creme_fraiche
        time.sleep(STEP_DELAY)
        print('done with the crème fraîche sauce')

    def add_topping(self):
        print('adding the topping (mozzarella, bacon, ham, mushrooms, red onion, oregano) to your creamy bacon')
        self.pizza.topping.append([t for t in
                                   (PizzaTopping.mozzarella, PizzaTopping.bacon,
                                    PizzaTopping.ham, PizzaTopping.mushrooms,
                                    PizzaTopping.red_onion, PizzaTopping.oregano)])
        time.sleep(STEP_DELAY)
        print('done with the topping (mozzarella, bacon, ham, mushrooms, red onion, oregano)')

    def bake(self):
        self.progress = PizzaProgress.baking
        print('baking your creamy bacon for {} seconds'.format(self.baking_time))
        time.sleep(self.baking_time)
        self.progress = PizzaProgress.ready
        print('your creamy bacon is ready')


class Waiter:
    """ 指挥者"""

    def __init__(self):
        self.builder = None

    def construct_pizza(self, builder):
        self.builder = builder
        [step() for step in (builder.prepare_dough, builder.add_sauce, builder.add_topping, builder.bake)]

    @property
    def pizza(self):
        return self.builder.pizza


def validate_style(builders):
    try:
        pizza_style = input('What pizza would you like, [m]argarita or [c]reamy bacon?')
        builder = builders[pizza_style]()
        valid_input = True
    except KeyError as err:
        print('Sorry, only margarita (key m) and creamy bacon (key c) are available')
        return (False, None)
    return (True, builder)


def main():
    builders = dict(m=MargaritaBuilder, c=CreamyBaconBuilder)
    valid_input = False
    while not valid_input:
        valid_input, builder = validate_style(builders)
    print()
    waiter = Waiter()
    waiter.construct_pizza(builder)
    pizza = waiter.pizza
    print()
    print('Enjoy your {}!'.format(pizza))


class Pizza:
    """ 变体：流利构造器模式
    实体类
    """

    def __init__(self, builder):
        self.garlic = builder.garlic
        self.extra_cheese = builder.extra_cheese

    def __str__(self):
        garlic = 'yes' if self.garlic else 'no'
        cheese = 'yes' if self.extra_cheese else 'no'
        info = ('Garlic: {}'.format(garlic), 'Extra cheese: {}'.format(cheese))
        return '\n'.join(info)

    class PizzaBuilder:
        """ 构造器 """

        def __init__(self):
            self.extra_cheese = False
            self.garlic = False

        def add_garlic(self):
            self.garlic = True
            return self

        def add_extra_cheese(self):
            self.extra_cheese = True
            return self

        def build(self):
            return Pizza(self)


if __name__ == '__main__':
    # main()

    pizza = Pizza.PizzaBuilder().add_garlic().add_extra_cheese().build()
    print(pizza)
