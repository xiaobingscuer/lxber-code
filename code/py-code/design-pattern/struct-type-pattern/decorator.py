#!/usr/bin/python
# coding=utf-8

"""
装饰器模式

1. 解决 动态扩展一个对象的功能

问题：无论何时我们想对一个对象添加额外的功能，都有下面这些不同的可选方法。
 a.如果合理，可以直接将功能添加到对象所属的类（例如，添加一个新的方法）
 b.使用组合
 c.使用继承
    与继承相比，通常应该优先选择组合，因为继承使得代码更难复用，继承关系是静态的，并
    且应用于整个类以及这个类的所有实例
 d. 设计模式为我们提供第四种可选方法，以支持动态地（运行时）扩展一个对象的功能，这种
    方法就是修饰器。修饰器（Decorator）模式能够以透明的方式（不会影响其他对象）动态地将功
    能添加到一个对象中

问题：当用于实现横切关注点（cross-cutting concerns）时，修饰器模式会大显神威
    一般来说，应用中有些部件是通用的，可应用于其他部件，这样的部件被看作横切关注点
    以下是横切关注点的一些例子。
    a.数据校验
    b.事务处理（这里的事务类似于数据库事务，意味着要么所有步骤都成功完成，要么事务失败）
    c.缓存
    d.日志
    e. 监控
    f. 调试
    g. 业务规则
    h. 压缩
    i. 加

问题：修饰器的另一个有趣的特性是可以使用多个修饰器来修饰一个函数。多个修饰器会以什么次序执行？

python特性：我们使用修饰器模式来扩展一个对象的行为，无需使用继承，非常方便。
    Python进一步扩展了修饰器的概念，允许我们无需使用继承或组合就能扩展任意可调用对象（函数、方法或类）的行为。
    我们可以使用Python内置的修饰器特性。

"""

import functools


def printfunc(is_print=False):
    print('printfunc decorator')

    def outer(func):
        print('outer')
        @functools.wraps(func)
        def inner(*args, **kwargs):
            print('inner')
            if is_print:
                print(func)
            return func(*args, **kwargs)

        return inner

    return outer


def memoize(fn):
    print('memoize decorator')
    known = dict()

    @functools.wraps(fn)
    def memoizer(*args, **kwargs):
        if args not in known:
            known[args] = fn(*args, **kwargs)
            return known[args]

    return memoizer


@memoize
@printfunc(True)
def nsum(n):
    '''返回前n个数字的和'''
    assert (n >= 0), 'n must be >= 0'
    return 0 if n == 0 else n + nsum(n - 1)


@printfunc
@memoize
def fibonacci(n):
    '''返回斐波那契数列的第n个数'''
    assert (n >= 0), 'n must be >= 0'
    return n if n in (0, 1) else fibonacci(n - 1) + fibonacci(n - 2)


if __name__ == '__main__':
    from timeit import Timer

    print(nsum(5))


    # measure = [{'exec': 'fibonacci(100)', 'import': 'fibonacci', 'func': fibonacci}, {'exec': 'nsum(200)', 'import': 'nsum', 'func': nsum}]
    # for m in measure:
    #     t = Timer('{}'.format(m['exec']), 'from __main__ import{}'.format(m['import']))
    #     print('name: {}, doc: {}, executing: {}, time:{}'.format(m['func'].__name__, m['func'].__doc__, m['exec'],
    #                                                              t.timeit()))
