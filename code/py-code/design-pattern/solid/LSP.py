#!/usr/bin/python
# coding=utf-8

"""
solid设计原则
"""

""" 
里氏代换原则（Liskov Substitution Principle）：

描述：当你使用继承时，子类（派生类）对象应该可以在程序中替代父类（基类）对象使用，而不破坏程序原本的功能；

内涵解释：
    继承：继承的父子类之间要具有'is-a'关系，尤其是行为是否具有is-a的关系；
    替换：父类出现的地方，都可以使用子类替换，前提是不影响原本功能的正确性，如果影响了，即违反里氏替换原则；
    符合里氏替换原则的类之间的继承建模关系才是合理的。
    对象的行为才是软件真正所关注的问题。
    优点：
        1. LSP原则是实现OCP原则的重要保障之一
        2. 降低继承带来的复杂性，继承只能扩展基类的功能
        3. 在决定使用继承前，可以更好地判别两者是否具有is-a的关系

生活中的例子：
    运动员是健康的，举重员继承自运动员，那么举重运动员也是健康的；
    
违反原则的坏处：
    1. 程序运行出错，逻辑出错，结果出错。
    
违反原则后的修复方法：
    1. 重新设计类之间的继承关系。
        如果 “对象不能支持某种操作” 本身就是这个类型的 核心特征 之一，那我们在进行父类设计时，就应该把这个 核心特征 设计进去。
    2. 抽取公共代码
        将父子公共的代码提取出来作为新的抽象类，让父子变为兄弟都继承该类，或者以组合的方式继承抽取出来的代码。
    3. 大类拆分为更小的类，使用组合或依赖注入的方式使用
        
代码举例：
    1. 子类修改方法返回值
        我们一定得让子类方法和父类返回同一类型的结果，支持同样的操作。或者更进一步，返回支持更多种操作的子类型结果也是可以接受的。

    2. 方法参数与 L 原则
        让子类的方法参数签名和父类完全一致，或者更宽松
    

"""