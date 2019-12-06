#!/usr/bin/python
# coding=utf-8

__doc__ = """
模拟退火算法
模拟退火算法对于连续函数优化问题不能很好地收敛,因为搜索空间较大，另外没有方向引导，会重复搜索，因此搜索效率低
"""

import numpy as np


class SA(object):
    def __init__(self):
        # 控制参数
        self.T = 1000 * 1   # 初始温度
        self.T_DELTA = 0.981    # 温度衰变因子
        self.T_END = 1e-2   # 终止温度
        self.L = 200   # 每个温度下循环的次数
        self.cur_t = self.T     # 当前温度
        # 解的约束与表示
        self.dims = 30  # 解的维度
        self.scale = [[-5.12, 5.12] for _ in range(self.dims)]  # 解的每个维度变量值空间范围
        self.dist = [s[1] - s[0] for s in self.scale]
        self.origin = [s[0] for s in self.scale]
        self.cur_ans = np.random.rand(self.dims) * self.dist + self.origin  # 当前解
        self.cur_energy = 1234567890  # 当前解对应的能量
        self.best_ans = self.cur_ans    # 最优解
        self.best_energy = 1234567890     # 最优解对应的能量
        # 值函数
        self.value_func = lambda x: np.sum(np.array(x) ** 2)
        # self.value_func = lambda x: np.sum(np.array(x) ** 2 - 10 * np.cos(np.array(x) * 2 * np.pi) + 10)
        pass

    def simulate_anneal(self):
        """
        模拟退火主方法
        """
        # 初始化
        t = self.T
        self.best_ans = self.cur_ans
        self.best_energy = self.cur_energy = self.value_func(self.cur_ans)
        dec_cnt = 0
        # sa
        while t >= self.T_END:
            # 外部循环，降温过程，直到温度降到比终止温度低为止
            dec_cnt += 1
            # 从当前最好解开始搜索
            self.cur_ans = self.best_ans
            self.cur_energy = self.best_energy
            for loop in range(self.L):
                # 内部循环，每个温度尝试一定的次数
                next_ans = self.get_next_ans(t)  # 获取新解
                next_energy = self.value_func(next_ans)  # 计算新解的能量
                delta_energy = next_energy - self.cur_energy  # 计算能量差，因为是求最小值，能量差 = 新解的能量 - 当前解的能量
                if delta_energy < 0:
                    # 直接接受比当前解较好的新解
                    self.cur_ans = next_ans
                    self.cur_energy = next_energy
                    if self.cur_energy < self.best_energy:
                        # 更新当前最好的解
                        self.best_ans = self.cur_ans
                        self.best_energy = self.cur_energy

                else:
                    # 以概率接收较差的新解
                    prob = np.exp(-1.0 * delta_energy / t)
                    print("当前温度：%s dE:%s 接受概率：%s 最优值: %s" % (t, delta_energy, prob, self.best_energy))
                    if np.random.rand() < prob:
                        self.cur_ans = next_ans
                        self.cur_energy = next_energy

            t *= self.T_DELTA   # 降温
            self.cur_t = t  # 记录当前温度

            print("最优值： %s " % self.best_energy)
        pass

    def get_next_ans(self, t):
        # 生成邻域解
        next_ans = np.random.rand(self.dims) * self.dist + self.origin
        for di in range(self.dims):
            # if np.random.rand() > 0.3:
            #     continue
            ans_di = self.cur_ans[di]
            scale_min = self.scale[di][0]
            scale_max = self.scale[di][1]
            d_min = ans_di - scale_min
            d_max = scale_max - ans_di
            delta_ans = np.random.rand() * 0.2 - 0.1
            if delta_ans < 0:
                ans_di += delta_ans * d_min
            else:
                ans_di += delta_ans * d_max
            if ans_di < scale_min or ans_di > scale_max:
                raise ("out range")
            next_ans[di] = ans_di
        return next_ans


if __name__ == "__main__":
    print("hello world!")
    sa = SA()
    sa.simulate_anneal()
    print("最好解：%s " % sa.best_ans)
    print("最优值： %s " % sa.best_energy)
