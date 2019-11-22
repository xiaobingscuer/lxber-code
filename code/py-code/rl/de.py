#!/usr/bin/python
# coding=utf-8

__doc__ = """
差分进化算法
"""

import matplotlib.pyplot as plt
import numpy as np
from scipy import stats as st


class DE(object):
    def __init__(self):
        # 控制参数
        self.迭代次数 = 100
        self.变异因子 = 0.5
        self.交叉概率 = 0.5
        # 解的表示 - 个体与种群
        self.种群规模 = 10
        self.范围 = [[0, 1], [0, 1]]
        self.种群 = []
        self.最好个体 = None
        # 解对应的函数
        self.值函数 = np.exp()
        pass

    def 初始化(self):
        self.种群 = np.random.rand(self.种群规模, len(self.范围)) * [某维度[1] - 某维度[0] for 某维度 in self.维度]
        self.种群 += [某维度[0] for 某维度 in self.维度]
        pass

    def 变异(self, 变异策略="随机+随机-随机"):
        pass

    def 交叉(self):
        pass

    def 选择(self):
        pass

    def 迭代(self):
        pass
    pass


if __name__ == "__main__":
    print("hello world!")
