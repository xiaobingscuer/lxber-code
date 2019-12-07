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
        self.最好个体适应度 = 1234567890
        # 解对应的函数
        self.值函数 = lambda 个体: np.sum(np.array(个体) ** 2 - 10 * np.cos(np.array(个体) * 2 * np.pi) + 10)  # 多峰函数
        # self.值函数 = lambda 个体: np.sum(np.array(个体) ** 2)  # 单峰函数
        pass

    def 初始化(self):
        np.random.seed(65536)
        self.种群 = np.random.rand(self.种群规模, self.维度) * self.范围距离 + self.范围起始
        self.种群[np.random.randint(self.种群规模)] = cp.deepcopy(self.最好个体)
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
        过渡种群必交叉序列 = np.random.randint(0, self.维度, self.种群规模)    # 保证每个变异个体有一个等位基因被交叉
        过渡种群是否交叉序列 = np.random.rand(self.种群规模, self.维度) < self.交叉概率    # 按概率交叉
        for 个体编号 in range(self.种群规模):
            for 维度编号 in range(self.维度):
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
        # 过渡种群适应度评估
        self.过渡种群适应度评估()
        # 在过渡个体和种群中的个体之间选择最好的
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

    def 繁殖(self):
        """
        种群繁殖到过渡种群
        """
        self.变异()
        self.交叉()

    def 迭代(self):
        """
        当前解，生成的下一步解，在生成的下一步解和当前解之间进行选择
        生成下一步解：引导方向，行走步长
        选择：控制方向，避免搜索已经被搜索过的差解，这是比随机方法好的原因
        """
        self.初始化()
        self.种群适应度评估()
        for 迭代编号 in range(self.迭代次数):
            # print("--------- 迭代编号: %s ---------" % 迭代编号)
            self.繁殖()
            self.选择("极小")
        # print("迭代后的种群")
        # print(self.种群)
        # print("最好个体")
        # print(self.最好个体)
        print("最优值")
        print(self.最好个体适应度)
        pass
    pass


class DETsp(差分进化算法DE):
    def __init__(self):
        super().__init__()
        # 控制参数
        #
        # 解的约束与表示
        # 最优值 7544.365901904086
        # 最优解：[14  5  3 24 11 27 26 25 46 12 13 51 10 50 32 42  9  8  7 40 18 44 31 48
        #   0 21 30 17  2 16 20 41  6  1 29 22 19 49 28 15 45 43 33 34 35 38 39 36
        #  37 47 23  4]
        self.citys = [[565.0, 575.0], [25.0, 185.0], [345.0, 750.0], [945.0, 685.0], [845.0, 655.0],
                      [880.0, 660.0], [25.0, 230.0], [525.0, 1000.0], [580.0, 1175.0], [650.0, 1130.0],
                      [1605.0, 620.0], [1220.0, 580.0], [1465.0, 200.0], [1530.0, 5.0], [845.0, 680.0],
                      [725.0, 370.0], [145.0, 665.0], [415.0, 635.0], [510.0, 875.0], [560.0, 365.0],
                      [300.0, 465.0], [520.0, 585.0], [480.0, 415.0], [835.0, 625.0], [975.0, 580.0],
                      [1215.0, 245.0], [1320.0, 315.0], [1250.0, 400.0], [660.0, 180.0], [410.0, 250.0],
                      [420.0, 555.0], [575.0, 665.0], [1150.0, 1160.0], [700.0, 580.0], [685.0, 595.0],
                      [685.0, 610.0], [770.0, 610.0], [795.0, 645.0], [720.0, 635.0], [760.0, 650.0],
                      [475.0, 960.0], [95.0, 260.0], [875.0, 920.0], [700.0, 500.0], [555.0, 815.0],
                      [830.0, 485.0], [1170.0, 65.0], [830.0, 610.0], [605.0, 625.0], [595.0, 360.0],
                      [1340.0, 725.0], [1740.0, 245.0]]
        self.维度 = len(self.citys)  # 解的维度
        self.值函数 = self.value_func  # 评估值函数
        self.最好个体 = None
        # 获取城市间的距离
        self.dims = self.维度
        self.citys_distance = np.zeros((self.dims, self.dims))  # 两两城市之间的距离
        self.get_citys_distance()

    def 初始化(self):
        np.random.seed(65536)
        self.最好个体 = np.arange(self.维度) if self.最好个体 is None else self.最好个体
        self.最好个体适应度 = self.值函数(self.最好个体)
        self.种群 = np.array([np.random.choice(self.维度, self.维度, replace=False) for _ in range(self.种群规模)])
        self.种群[np.random.randint(self.种群规模)] = cp.deepcopy(self.最好个体)
        self.过渡种群 = cp.deepcopy(self.种群)
        self.种群的适应度 = np.zeros(self.种群规模)
        self.过渡种群的适应度 = np.zeros(self.种群规模)

    def get_citys_distance(self):
        # 计算两两城市之间的距离
        for i in range(self.dims):
            for j in range(i, self.dims):
                dist = np.sqrt(np.sum(np.subtract(self.citys[i], self.citys[j]) ** 2))
                self.citys_distance[i][j] = self.citys_distance[j][i] = dist

    def value_func(self, ans):
        dist = 0
        for aid in range(self.dims - 1):
            dist += self.citys_distance[ans[aid]][ans[aid + 1]]
        dist += self.citys_distance[ans[self.dims - 1]][ans[0]]
        # print("value_func: %s " % dist)
        return dist

    def get_next_ans(self, cur_ans):
        # 通过交换解片段中的城市生成邻域解
        # change_index = sorted(np.random.randint(0, self.dims, 2))
        change_index = sorted(np.random.choice(self.dims, 2, replace=False))
        next_ans = cp.deepcopy(cur_ans)
        # print(cur_ans)
        i, j = change_index[0], change_index[1]
        while i < j:
            next_ans[i], next_ans[j] = next_ans[j], next_ans[i]
            i += 1
            j -= 1
        # print(next_ans)
        return next_ans

    def 变异(self):
        """
        对过渡种群个体进行变异
        """
        # 对每个个体进行变异，变异方式为：交换解片段中的城市
        for 个体编号 in range(self.种群规模):
            变异个体 = self.get_next_ans(self.种群[个体编号])
            self.过渡种群[个体编号] = 变异个体

    def 交叉(self):
        """
        从种群中选择两个个体进行交叉到过渡种群个
        """
        pass

    def 繁殖(self):
        """
        先交叉再变异
        """
        self.交叉()
        self.变异()
        
    pass


if __name__ == "__main__":
    print("hello world!")
    # 差分进化对象 = 差分进化算法DE()
    # 差分进化对象.迭代次数 = 1000
    # 差分进化对象.种群规模 = 32
    # SN = 10  # 多轮搜索，每次从上一次最优解开始搜索,因为一般一轮是不能很好地收敛到最优
    # for si in range(SN):
    #     差分进化对象.迭代()

    差分进化对象 = DETsp()
    差分进化对象.迭代次数 = 1000
    差分进化对象.种群规模 = 1
    SN = 100  # 多轮搜索，每次从上一次最优解开始搜索,因为一般一轮是不能很好地收敛到最优
    for si in range(SN):
        差分进化对象.迭代()
    print("最好个体")
    print(差分进化对象.最好个体)
    print("最优值")
    print(差分进化对象.最好个体适应度)