#!/usr/bin/python
# coding=utf-8

"""
原型模式：
1. 解决对象拷贝的问题，创建对象的克隆，python中简单方式可以使用内置模块方法copy.copy()（浅拷贝），copy.deepcopy()（深拷贝）
2. 当我们想复制一个复杂对象时，使用原型模式会很方便
3. 创建一个对象的副本可以指代以下两件事情:
    1)当创建一个浅副本时，副本依赖引用
    2)当创建一个深副本时，副本复制所有东西
    第一种情况中，我们关注提升应用性能和优化内存使用，在对象之间引入数据共享，
        但需要小心地修改数据，因为所有变更对所有副本都是可见的。
    第二种情况中，我们希望能够对一个副本进行更改而不会影响其他对象。
        这一特性是很有用的。这里不会进行数据共享，所以需要关注因对象克隆而引入的资源耗用问题。
"""

import copy
from collections import OrderedDict


class Book:
    def __init__(self, name, authors, price, **rest):
        '''rest的例子有：出版商、长度、标签、出版日期'''
        self.name = name
        self.authors = authors
        self.price = price  # 单位为美元
        self.__dict__.update(rest)

    def __str__(self):
        mylist = []
        ordered = OrderedDict(sorted(self.__dict__.items()))
        for i in ordered.keys():
            mylist.append('{}: {}'.format(i, ordered[i]))
            if i == 'price':
                mylist.append('$')
            mylist.append('\n')
        return ''.join(mylist)


class Prototype:
    """ 原型模式 """
    def __init__(self):
        self.objects = dict()

    def register(self, identifier, obj):
        self.objects[identifier] = obj

    def unregister(self, identifier):
        del self.objects[identifier]

    def clone(self, identifier, **attr):
        found = self.objects.get(identifier)
        if not found:
            raise ValueError('Incorrect object identifier: {}'.format(identifier))
        obj = copy.deepcopy(found)
        obj.__dict__.update(attr)
        return obj


def main():
    b1 = Book('The C Programming Language', ('Brian W. Kernighan', 'Dennis M.Ritchie'),
              price=118, publisher='Prentice Hall', length=228, publication_date='1978-02-22',
              tags=('C', 'programming', 'algorithms', 'data structures'))
    prototype = Prototype()
    cid = 'k&r-first'
    prototype.register(cid, b1)
    b2 = prototype.clone(cid, name='The C Programming Language(ANSI)', price=48.99, length=274,
                         publication_date='1988-04-01', edition=2)
    for i in (b1, b2):
        print(i)
    print("ID b1 : {} != ID b2 : {}".format(id(b1), id(b2)))


if __name__ == '__main__':
    main()
    pass
