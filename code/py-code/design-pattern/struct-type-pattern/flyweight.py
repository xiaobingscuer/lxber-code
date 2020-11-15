#!/usr/bin/python
# coding=utf-8

"""
享元模式

1. 解决 享元设计模式通过为相似对象引入数据共享来最小化内存使用，提升性能
        哪些数据应该是享元的一部分（不可变的、内部的），哪些数据不应该是（可变的、外部的）。

问题：
    a.由于大量对象创建的开销，面向对象的系统可能会面临内存性能问题。
    b.除内存使用之外，计算性能也是一个考虑点。图形软件，包括计算机游戏，应该能够极快地
    渲染3D信息（例如，有成千上万棵树的森林或满是士兵的村庄）。如果一个3D地带的每个对象都
    是单独创建，未使用数据共享，那么性能将是无法接受的

2. 一个享元（Flyweight）就是一个包含状态独立的不可变（又称固有的）数据的
共享对象。依赖状态的可变（又称非固有的）数据不应是享元的一部分，因为每个对象的这种信
息都不同，无法共享。如果享元需要非固有的数据，应该由客户端代码显式地提供

3. 享元旨在优化性能和内存使用。所有嵌入式系统（手机、平板电脑、游戏终端和微控制器等）
    和性能关键的应用（游戏、3D图形处理和实时系统等）都能从其获益。
    若想要享元模式有效，需要满足GoF的《设计模式》一书罗列的以下几个条件。
    a. 应用需要使用大量的对象。
    b. 对象太多，存储/渲染它们的代价太大。一旦移除对象中的可变状态（因为在需要之时，应
    该由客户端代码显式地传递给享元），多组不同的对象可被相对更少的共享对象所替代。
    c. 对象ID对于应用不重要。对象共享会造成ID比较的失败，所以不能依赖对象ID（那些在
    客户端代`码看来不同的对象，最终具有相同的ID）。

4. 记忆化搜索，memoization与享元模式之间的区别。
    享元则是一种特定于面向对象编程优化的设计模式，关注的是共享对象数据
    memoization是一种优化技术，使用一个缓存来避免重复计算那些在更早的执行步骤中已经计算好的结果。

"""

import random
from enum import Enum

TreeType = Enum('TreeType', 'apple_tree cherry_tree peach_tree')


class Tree:
    pool = dict()

    def __new__(cls, tree_type):
        obj = cls.pool.get(tree_type, None)
        if not obj:
            obj = object.__new__(cls)
            cls.pool[tree_type] = obj
            obj.tree_type = tree_type
        return obj

    def render(self, age, x, y):
        print('render a tree of type {} and age {} at ({}, {})'.format(self.tree_type, age, x, y))


def main():
    rnd = random.Random()
    age_min, age_max = 1, 30  # 单位为年
    min_point, max_point = 0, 100
    tree_counter = 0
    for _ in range(10):
        t1 = Tree(TreeType.apple_tree)
        t1.render(rnd.randint(age_min, age_max),
                  rnd.randint(min_point, max_point),
                  rnd.randint(min_point, max_point))
        tree_counter += 1

    for _ in range(3):
        t2 = Tree(TreeType.cherry_tree)
        t2.render(rnd.randint(age_min, age_max),
                  rnd.randint(min_point, max_point),
                  rnd.randint(min_point, max_point))
        tree_counter += 1

    for _ in range(5):
        t3 = Tree(TreeType.peach_tree)
        t3.render(rnd.randint(age_min, age_max),
                  rnd.randint(min_point, max_point),
                  rnd.randint(min_point, max_point))
        tree_counter += 1

    print('trees rendered: {}'.format(tree_counter))
    print('trees actually created: {}'.format(len(Tree.pool)))

    t4 = Tree(TreeType.cherry_tree)
    t5 = Tree(TreeType.cherry_tree)
    t6 = Tree(TreeType.apple_tree)
    print('{} == {}? {}'.format(id(t4), id(t5), id(t4) == id(t5)))
    print('{} == {}? {}'.format(id(t5), id(t6), id(t5) == id(t6)))


if __name__ == '__main__':
    main()
