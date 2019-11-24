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


class SA(object):
    def __init__(self):
        # 控制参数
        self.ts = 1000 * 4
        self.delta = 0.98
        self.te = .1
        self.alpha = 0.9
        # 解的约束与表示
        self.dims = 30
        self.scale = [[-5.12, 5.12] for _ in range(self.dims)]
        self.dist = [s[1] - s[0] for s in self.scale]
        self.origin = [s[0] for s in self.scale]
        self.cur_ans = np.random.rand(self.dims) * self.dist + self.origin
        self.cur_value = 0
        self.best_ans = self.cur_ans
        self.bets_value = 0
        # 解的约束
        # self.value_func = lambda x: np.sum(np.array(x) ** 2)
        self.value_func = lambda x: np.sum(np.array(x) ** 2 - 10 * np.cos(np.array(x) * 2 * np.pi) + 10)
        pass

    def simulate_anneal(self):
        t = self.ts
        self.bets_value = self.cur_value = self.value_func(self.cur_ans)
        while True:
            next_ans = self.get_next_ans(t)
            value_next = self.value_func(next_ans)
            deleta_energy = value_next - self.cur_value
            if deleta_energy < 0: # 接受新解
                self.cur_ans = next_ans
                self.cur_value = value_next
                if self.cur_value < self.bets_value:
                    self.bets_value = self.cur_value
                    self.best_ans = self.cur_ans

            else:   # 以概率接收差解
                prob = np.exp(-1.0 * deleta_energy / t)
                print("当前温度：%s 概率为： %s " % (t, prob))
                if np.random.rand() < prob:
                    self.cur_ans = next_ans
                    self.cur_value = value_next
                pass

            if t < self.te:
                break
            t *= self.delta

            print("最优值： %s " % sa.bets_value)

            pass
        pass

    def get_next_ans(self, t):
        next_ans = self.cur_ans + np.random.rand(self.dims) * 2
        return next_ans


if __name__ == "__main__":
    print("hello world!")
    sa = SA()
    sa.simulate_anneal()
    print("最好解：")
    print(sa.best_ans)
    print("最优值： %s " % sa.bets_value)
