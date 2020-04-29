#!/usr/bin/python
# coding=utf-8

__doc__ = """
采样 
"""

import matplotlib.pyplot as plt
import numpy as np
from scipy import stats as st
import random as rd
import copy as cp


class 蒙特卡洛模拟采样():
    def __init__(self):
        pass

    def 求π(self):
        """
        通过求在边长为1的方形里的圆面积的方式，来确定差分进化算的在解空间里的种群规模
        """
        实验次数 = 3
        采样点数 = 300
        采样点维度 = 2
        采样点集 = np.random.rand(实验次数, 采样点数, 采样点维度) * 2 - 1
        实验结果 = np.zeros((实验次数, 采样点数))
        for 实验编号 in range(实验次数):
            在圆内次数 = 0
            for 采样编号 in range(采样点数):
                采样点 = 采样点集[实验编号][采样编号]
                在圆内次数 += (np.sum(采样点 ** 2) < 1)
                实验结果[实验编号][采样编号] = np.abs(1.0 * 在圆内次数 / (采样编号 + 1) - np.pi / 4)
                pass
        print(实验结果[..., -1])

        # print(实验结果)
        平均实验结果 = np.mean(实验结果, axis=0)

        # print(平均实验结果)

        差分实验结果 = cp.deepcopy(平均实验结果[..., 0:采样点数-1])
        差分实验结果 = 差分实验结果 - 平均实验结果[..., 1:采样点数]
        # 画出图形
        fig, axs = plt.subplots()
        # for 结果 in 差分实验结果:
        #     axs.plot(range(len(结果)), 结果, label="", alpha=0.6)
        axs.plot(range(len(平均实验结果)), 平均实验结果, alpha=0.6)
        axs.plot(range(len(差分实验结果)), 差分实验结果, alpha=0.6)
        axs.set(title='p = pi/4')
        plt.show()

        pass

    def markov_chain(self, P, k):
        Pij = cp.copy(P)
        Pij = np.matrix(Pij)
        for i in range(k):
            Pij = Pij * Pij
        print(Pij)
        return Pij


if __name__ == "__main__":
    print("hello world!")
    蒙特卡洛 = 蒙特卡洛模拟采样()
    # 蒙特卡洛.求π()
    P = [[0.5, 0.5, 0],
         [0, 0, 1],
         [1, 0, 0]]
    P = [[0., 0.5, 0.5],
         [1, 0., 0.],
         [1, 0., 0.]]
    Pij = 蒙特卡洛.markov_chain(P, 1000)
    print(Pij)
