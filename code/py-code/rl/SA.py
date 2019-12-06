#!/usr/bin/python
# coding=utf-8

__doc__ = """
模拟退火算法
模拟退火算法对于连续函数优化问题不能很好地收敛,因为连续搜索空间较大，另外没有方向引导，会重复搜索，因此搜索效率低
在离散问题中表现较好，比如tsp问题，因为搜索空间较小，且每一次产生的新解都是一个不同的解
对于离散问题，每次降温后不需要从当前最优解出发，因为整个算法过程就是逐渐收敛到最优解
"""

import numpy as np
import copy as cp


class SA(object):
    def __init__(self):
        # 控制参数
        self.T = 1000 * 1e0   # 初始温度
        self.T_DELTA = 0.981    # 温度衰变因子
        self.T_END = 1e-1   # 终止温度
        self.L = 300   # 每个温度下循环的次数
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
        self.energy = lambda x: np.sum(np.array(x) ** 2)
        # self.energy = lambda x: np.sum(np.array(x) ** 2 - 10 * np.cos(np.array(x) * 2 * np.pi) + 10)
        pass

    def simulate_anneal(self):
        """
        模拟退火主方法
        """
        # 初始化
        t = self.T
        self.best_ans = self.cur_ans
        self.best_energy = self.cur_energy = self.energy(self.cur_ans)
        dec_cnt = 0
        # sa
        while t >= self.T_END:
            # 外部循环，降温过程，直到温度降到比终止温度低为止
            dec_cnt += 1
            # 从当前最好解开始搜索
            # self.cur_ans = self.best_ans
            # self.cur_energy = self.best_energy
            for _ in range(self.L):
                # 内部循环，每个温度尝试一定的次数
                next_ans = self.get_next_ans()  # 获取新解
                next_energy = self.energy(next_ans)  # 计算新解的能量
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

    def get_next_ans(self):
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


class SaTsp(SA):
    """
    使用模拟退火算法求解旅行商问题(TSP)
    """
    def __init__(self):
        super().__init__()
        # 控制参数
        self.T = 1000
        self.T_DELTA = 0.92
        self.T_END = 1e-1
        self.L = 100 * self.dims
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
        self.dims = len(self.citys)  # 解的维度
        self.cur_ans = np.arange(self.dims)  # 当前解
        self.citys_distance = np.zeros((self.dims, self.dims))
        self.energy = self.value_func

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
        # print(dist)
        return dist

    def get_next_ans(self):
        # 通过交换城市生成邻域解
        # change_index = sorted(np.random.randint(0, self.dims, 2))
        change_index = sorted(np.random.choice(self.dims, 2, replace=False))
        next_ans = cp.deepcopy(self.cur_ans)
        # print(self.cur_ans)
        i = change_index[0]
        j = change_index[1]
        while True:
            next_ans[i], next_ans[j] = next_ans[j], next_ans[i]
            i += 1
            j -= 1
            if i >= j:
                break
        # print(next_ans)
        return next_ans
    pass


if __name__ == "__main__":
    print("hello world!")
    # sa = SA()
    # sa.simulate_anneal()
    # print("最好解：%s " % sa.best_ans)
    # print("最优值： %s " % sa.best_energy)

    sa = SaTsp()
    sa.get_citys_distance()
    sa.simulate_anneal()
    print("最好解：%s " % sa.best_ans)
    print("最优值： %s " % sa.best_energy)
