#!/usr/bin/python
# coding=utf-8

"""
抽象工厂：
1. 与工厂模式类似，主要解决多个不同类型的工厂接口选择问题,同样遵循开闭原则
2. 抽象工厂是对不同类型的工厂的聚合，不同抽象工厂的实例具有相同的接口，只是实现方式不同
"""


class Frog:
    def __init__(self, name):
        self.name = name

    def __str__(self):
        return self.name

    def interact_with(self, obstacle):
        print('{} the Frog encounters {} and {}!'.format(self, obstacle, obstacle.action()))


class Bug:
    def __str__(self):
        return 'a bug'

    def action(self):
        return 'eats it'


class FrogWorld:
    """ 抽象工厂 """
    def __init__(self, name):
        print(self)
        self.player_name = name

    def __str__(self):
        return '\n\n\t------ Frog World-------'

    def make_character(self):
        return Frog(self.player_name)

    def make_obstacle(self):
        return Bug()


class Wizard:
    def __init__(self, name):
        self.name = name

    def __str__(self):
        return self.name

    def interact_with(self, obstacle):
        print('{} the Wizard battles against {} and {}!'.format(self, obstacle, obstacle.action()))


class Ork:
    def __str__(self):
        return 'an evil ork'

    def action(self):
        return 'kills it'


class WizardWorld:
    """ 抽象工厂 """
    def __init__(self, name):
        print(self)
        self.player_name = name

    def __str__(self):
        return '\n\n\t------ Wizard World -------'

    def make_character(self):
        return Wizard(self.player_name)

    def make_obstacle(self):
        return Ork()


class GameEnvironment:
    def __init__(self, factory):
        self.hero = factory.make_character()
        self.obstacle = factory.make_obstacle()

    def play(self):
        self.hero.interact_with(self.obstacle)


def validate_age(name):
    try:
        age = input('Welcom {}. How old are you? '.format(name))
        age = int(age)
    except ValueError as err:
        print("Age {} is invalid, please try again...".format(age))
        return False, age
    return True, age


def game_factory_procedure(age):
    game_factory = FrogWorld if age < 18 else WizardWorld
    return game_factory


if __name__=='__main__':
    name = input("Hello, What's your name? ")
    valid_input = False
    while not valid_input:
        valid_input, age = validate_age(name)
    game = game_factory_procedure(age)
    environment = GameEnvironment(game(name))
    environment.play()
    pass
