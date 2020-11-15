#!/usr/bin/python
# coding=utf-8

"""
模板模式

1. 解决 于抽取一个算法的通用部分，从而提高代码复用

2. 模板设计模式旨在消除代码重复。如果我们发现结构相近的（多个）算法中有重复代码，
    则可以把算法的不变（通用）部分留在一个模板方法/函数中，把易变（不同）的部分移到动作/钩子方法/函数中。


"""


def dots_style(msg):
    msg = msg.capitalize()
    msg = '.' * 10 + msg + '.' * 10
    return msg


def admire_style(msg):
    msg = msg.upper()
    return '!'.join(msg)


def generate_banner(msg, style=dots_style):
    print('-- start of banner --')
    print(style(msg))
    print('-- end of banner --\n\n')


def main():
    msg = 'happy coding'
    [generate_banner(msg, style) for style in (dots_style, admire_style)]


if __name__ == '__main__':
    main()
