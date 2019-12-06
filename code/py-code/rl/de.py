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


class 差分进化算法DE(object):
    def __init__(self):
        # 控制参数
        self.迭代次数 = 3
        self.变异因子 = 0.1
        self.交叉概率 = 0.1
        # 解的表示 - 个体与种群
        self.种群规模 = 4
        self.维度 = 30
        self.范围 = [[-5.12, 5.12] for _ in range(self.维度)]
        self.范围距离 = [范围[1] - 范围[0] for 范围 in self.范围]
        self.范围起始 = [范围[0] for 范围 in self.范围]
        self.种群 = []
        self.过渡种群 = []
        self.种群的适应度 = []
        self.过渡种群的适应度 = []
        self.最好个体 = np.random.rand(self.维度) * self.范围距离 + self.范围起始
        self.最好个体适应度 = 0
        # 解对应的函数
        self.值函数 = lambda 个体: np.sum(np.array(个体) ** 2 - 10 * np.cos(np.array(个体) * 2 * np.pi) + 10)  # 多峰函数
        # self.值函数 = lambda 个体: np.sum(np.array(个体) ** 2)  # 单峰函数
        pass

    def 初始化(self):
        np.random.seed(65536)
        self.种群 = np.random.rand(self.种群规模, self.维度) * self.范围距离 + self.范围起始
        self.过渡种群 = cp.deepcopy(self.种群)
        self.种群的适应度 = np.zeros(self.种群规模)
        self.过渡种群的适应度 = np.zeros(self.种群规模)
        self.种群[np.random.randint(self.种群规模)] = cp.deepcopy(self.最好个体)
        self.种群适应度评估()
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
        过渡种群必交叉序列 = np.random.randint(0, self.维度, self.种群规模)    # 保证每个变异个体有一个等位基因被交叉
        过渡种群是否交叉序列 = np.random.rand(self.种群规模, self.维度) < self.交叉概率    # 按概率交叉
        for 个体编号 in range(self.种群规模):
            for 维度编号 in range(self.维度):
                if 过渡种群是否交叉序列[个体编号][维度编号] or 维度编号 == 过渡种群必交叉序列[个体编号]:
                    if self.过渡种群[个体编号][维度编号] > self.范围[维度编号][1] or self.过渡种群[个体编号][维度编号] < self.范围[维度编号][0]:    # 对变异后的个体进行范围检查
                        self.过渡种群[个体编号][维度编号] = np.random.rand() * (self.范围[维度编号][1] - self.范围[维度编号][0]) + self.范围[维度编号][0]
                else:
                    self.过渡种群[个体编号][维度编号] = self.种群[个体编号][维度编号]
        self.过渡种群适应度评估()
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
            最好个体编号 = np.argmax(self.种群的适应度)
        if 极值类型 == "极小":
            最好个体编号 = np.argmin(self.种群的适应度)
        self.最好个体 = cp.deepcopy(self.种群[最好个体编号])
        self.最好个体适应度 = self.种群的适应度[最好个体编号]
        # print("选择后的种群")
        # print(self.种群)
        pass

    def 迭代(self):
        """
        当前解，生成的下一步解，在生成的下一步解和当前解之间进行选择
        生成下一步解：引导方向，行走步长
        选择：控制方向，避免搜索已经被搜索过的差解，这是比随机方法好的原因
        :return:
        """
        self.初始化()
        for 迭代编号 in range(self.迭代次数):
            # print("--------- 迭代编号: %s ---------" % 迭代编号)
            self.变异()
            self.交叉()
            self.选择("极小")
        # print("迭代后的种群")
        # print(self.种群)
        # print("最好个体")
        # print(self.最好个体)
        print("最优值")
        print(self.最好个体适应度)
        pass
    pass


if __name__ == "__main__":
    print("hello world!")
    差分进化对象 = 差分进化算法DE()
    差分进化对象.迭代次数 = 1000
    差分进化对象.种群规模 = 32
    SN = 10  # 多次搜索，每次从上一次最优解开始搜索
    # r = 0.91
    for si in range(SN):
        差分进化对象.迭代()
        # # 缩小搜索的范围
        # for i in range(差分进化对象.维度):
        #     dmin = 差分进化对象.最好个体[i] - 差分进化对象.范围起始[i]
        #     差分进化对象.范围距离[i] *= r
        #     差分进化对象.范围起始[i] = 差分进化对象.最好个体[i] - r * dmin
        # # r *= 0.91

