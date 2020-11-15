#!/usr/bin/python
# coding=utf-8

"""
策略模式

1. 解决 鼓励使用多种算法来解决一个问题，其杀手级特性是能够在运行时透明地切换算法（客户端代码对变化无感知）

2. 不论何时希望动态、透明地应用不同算法，策略模式都是可行之路。这里所说不同算法的意思是，目的相同但实现方案不同的一类算法。
    这意味着算法结果应该是完全一致的，但每种实现都有不同的性能和代码复杂性

3. 策略模式并不限于排序问题，也可用于创建各种不同的资源过滤器（身份验证、日志记录、数据压缩和加密等）
    策略模式的另一个应用是创建不同的样式表现，为了实现可移植性（例如，不同平台之间断行的不同）或动态地改变数据的表现。
    另一个值得一提的应用是模拟；例如模拟机器人，一些机器人比另一些更有攻击性，一些机器人速度更快，等等。
    机器人行为中的所有不同之处都可以使用不同的策略来建模

菜鸟教程中的策略模式与状态模式的区别那边文章讲的很清楚,
与状态模式最大的不同就是，策略模式需要透明地可选择地使用不同算法。
状态模式的状态切换是自动发生的，不需要客户关系其变化。
"""

import time

SLOW = 3  # 单位为秒
LIMIT = 5  # 字符数
WARNING = 'too bad, you picked the slow algorithm :('


def pairs(seq):
    n = len(seq)
    for i in range(n):
        yield seq[i], seq[(i + 1) % n]


def allUniqueSort(s):
    if len(s) > LIMIT:
        print(WARNING)
        time.sleep(SLOW)
    srtStr = sorted(s)
    for (c1, c2) in pairs(srtStr):
        if c1 == c2:
            return False
    return True


def allUniqueSet(s):
    if len(s) < LIMIT:
        print(WARNING)
        time.sleep(SLOW)
    return True if len(set(s)) == len(s) else False


def allUnique(s, strategy):
    return strategy(s)


def main():
    while True:
        word = None
        while not word:
            word = input('Insert word (type quit to exit)> ')
        if word == 'quit':
            print('bye')
            return
        strategy_picked = None
        strategies = {'1': allUniqueSet, '2': allUniqueSort}
        while strategy_picked not in strategies.keys():
            strategy_picked = input('Choose strategy: [1] Use a set, [2] Sort andpair> ')
            try:
                strategy = strategies[strategy_picked]
                print('allUnique({}): {}'.format(word, allUnique(word, strategy)))
            except KeyError as err:
                print('Incorrect option: {}'.format(strategy_picked))
                print()


if __name__ == '__main__':
    main()
