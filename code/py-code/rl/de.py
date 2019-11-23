#!/usr/bin/python
# coding=utf-8

__doc__ = """
差分进化算法
"""

import matplotlib.pyplot as plt
import numpy as np
from scipy import stats as st
import random as rd
import copy as cp


class DE(object):
    def __init__(self):
        # 控制参数
        self.迭代次数 = 3
        self.变异因子 = 0.1
        self.交叉概率 = 0.1
        # 解的表示 - 个体与种群
        self.种群规模 = 4
        self.维度 = 30
        self.范围 = [[-5.12, 5.12] for _ in range(self.维度)]
        self.种群 = []
        self.过渡种群 = []
        self.种群的适应度 = []
        self.过渡种群的适应度 = []
        self.最好个体 = None
        # 解对应的函数
        # self.值函数 = lambda 个体: np.sum(np.array(个体) ** 2)
        self.值函数 = lambda 个体: np.sum(np.array(个体) ** 2 - 10 * np.cos(np.array(个体) * 2 * np.pi) + 10)
        pass

    def 初始化(self):
        self.种群 = np.random.rand(self.种群规模, len(self.范围)) * [某范围[1] - 某范围[0] for 某范围 in self.范围]
        self.种群 += [某范围[0] for 某范围 in self.范围]
        self.过渡种群 = cp.deepcopy(self.种群)
        self.种群的适应度 = np.zeros(self.种群规模)
        self.过渡种群的适应度 = np.zeros(self.种群规模)
        # print("初始化时的种群")
        # print(self.种群)
        # print("初始化时的过渡种群")
        # print(self.过渡种群)
        pass

    def 变异(self, 变异策略="随机+随机-随机"):
        # 变异策略="随机+随机-随机" 要求：随机选择3个互不相同的个体，且与当前个体也不相同
        变异组 = []
        for 个体编号 in range(self.种群规模):
            while True:
                变异组员 = rd.sample(range(self.种群规模), 3)
                if 个体编号 not in 变异组员:
                    变异组.append(变异组员)
                    break
        for 个体编号 in range(self.种群规模):
            变异组员 = 变异组[个体编号]
            变异个体 = self.种群[变异组员[0]] + self.变异因子 * (self.种群[变异组员[1]] - self.种群[变异组员[2]])
            self.过渡种群[个体编号] = 变异个体
            pass
        # print("变异组:%s" % 变异组)
        # print("变异生成的过渡种群")
        # print(self.过渡种群)
        pass

    def 交叉(self):
        过渡种群必交叉序列 = np.random.randint(0, len(self.范围), self.种群规模)    # 保证每个变异个体有一个等位基因被交叉
        过渡种群是否交叉序列 = np.random.rand(self.种群规模, len(self.范围)) < self.交叉概率    # 按概率交叉
        for 个体编号 in range(self.种群规模):
            for 维度编号 in range(len(self.范围)):
                if 过渡种群是否交叉序列[个体编号][维度编号] or 维度编号 == 过渡种群必交叉序列[个体编号]:
                    if self.过渡种群[个体编号][维度编号] > self.范围[维度编号][1] or self.过渡种群[个体编号][维度编号] < self.范围[维度编号][0]:    # 对变异后的个体进行范围检查
                        self.过渡种群[个体编号][维度编号] = np.random.rand() * (self.范围[维度编号][1] - self.范围[维度编号][0]) + self.范围[维度编号][0]
                else:
                    self.过渡种群[个体编号][维度编号] = self.种群[个体编号][维度编号]
        # print(过渡种群必交叉序列)
        # print(过渡种群是否交叉序列)
        # print("交叉后的过渡种群")
        # print(self.过渡种群)
        pass

    def 种群适应度评估(self):
        for 个体编号 in range(self.种群规模):
            self.种群的适应度[个体编号] = self.值函数(self.种群[个体编号])
        # print("种群的适应度: %s " % self.种群的适应度)
        # print("过渡种群的适应度: %s " % self.过渡种群的适应度)
        pass

    def 过渡种群适应度评估(self):
        for 个体编号 in range(self.种群规模):
            self.过渡种群的适应度[个体编号] = self.值函数(self.过渡种群[个体编号])
        # print("种群的适应度: %s " % self.种群的适应度)
        # print("过渡种群的适应度: %s " % self.过渡种群的适应度)
        pass

    def 选择(self, 极值类型="极大"):
        for 个体编号 in range(self.种群规模):
            if 极值类型 == "极大" and self.过渡种群的适应度[个体编号] > self.种群的适应度[个体编号]:
                self.种群[个体编号] = cp.deepcopy(self.过渡种群[个体编号])
                self.种群的适应度[个体编号] = self.过渡种群的适应度[个体编号]
            if 极值类型 == "极小" and self.过渡种群的适应度[个体编号] < self.种群的适应度[个体编号]:
                self.种群[个体编号] = cp.deepcopy(self.过渡种群[个体编号])
                self.种群的适应度[个体编号] = self.过渡种群的适应度[个体编号]
            pass
        if 极值类型 == "极大":
            self.最好个体 = np.argmax(self.种群的适应度)
        if 极值类型 == "极小":
            self.最好个体 = np.argmin(self.种群的适应度)
        # print("选择后的种群")
        # print(self.种群)
        pass

    def 迭代(self):
        self.初始化()
        self.种群适应度评估()
        for 迭代编号 in range(self.迭代次数):
            print("--------- 迭代编号: %s ---------" % 迭代编号)
            self.变异()
            self.交叉()
            self.过渡种群适应度评估()
            self.选择("极小")
        # print("迭代后的种群")
        # print(self.种群)
        print("最好个体")
        print(self.种群[self.最好个体])
        print("最优值")
        print(self.种群的适应度[self.最好个体])
        pass
    pass


if __name__ == "__main__":
    print("hello world!")
    de = DE()
    de.迭代次数 = 1000
    de.种群规模 = 100
    de.迭代()
