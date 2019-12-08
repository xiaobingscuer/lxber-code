#!/usr/bin/python
# coding=utf-8

__doc__ = """
遗传算法
"""

import matplotlib.pyplot as plt
import numpy as np
from scipy import stats as st
import random as rd
import copy as cp


class GA(object):
    def __init__(self):
        # 控制参数
        self.iters = 3
        self.mut_prob = 0.1
        self.cross_prob = 0.1
        # 解的表示 - 个体与pops
        self.pop_nums = 4
        self.dims = 30
        self.scale = [[-5.12, 5.12] for _ in range(self.dims)]
        self.dist = [scale[1] - scale[0] for scale in self.scale]
        self.origin = [scale[0] for scale in self.scale]
        self.pops = []
        self.tmp_pops = []
        self.pops_fitness = []
        self.tmp_pops_fitness = []
        self.best_ans = np.random.rand(self.dims) * self.dist + self.origin     # 采用实数编码
        self.best_ans_fitness = 1234567890
        # 解对应的函数
        self.function = lambda 个体: np.sum(np.array(个体) ** 2 - 10 * np.cos(np.array(个体) * 2 * np.pi) + 10)  # 多峰函数
        # self.function = lambda 个体: np.sum(np.array(个体) ** 2)  # 单峰函数
        pass

    def initiation(self):
        np.random.seed(65536)
        self.pops = np.random.rand(self.pop_nums, self.dims) * self.dist + self.origin
        self.pops[np.random.randint(self.pop_nums)] = cp.deepcopy(self.best_ans)
        self.tmp_pops = cp.deepcopy(self.pops)
        self.pops_fitness = np.zeros(self.pop_nums)
        self.tmp_pops_fitness = np.zeros(self.pop_nums)
        # print("initiation时的pops")
        # print(self.pops)
        # print("initiation时的tmp_pops")
        # print(self.tmp_pops)
        pass

    def mutation(self, mut_strategy="rand+rand-rand"):
        # 变异
        prob_mut_seq = np.random.rand(self.pop_nums, self.dims) < self.mut_prob  # 按概率变异
        prob_pops = np.random.rand(self.pop_nums, self.dims) * self.dist + self.origin
        # 变异 - 均匀随机点替换
        # for index in range(self.pop_nums):
        #     for dim in range(self.dims):
        #         if prob_mut_seq[index][dim]:
        #             self.tmp_pops[index][dim] = prob_pops[index][dim]
        #             pass
        # 变异 - 正太随机点替换
        for index in range(self.pop_nums):
            for dim in range(self.dims):
                if prob_mut_seq[index][dim]:
                    rand_p = np.random.normal(loc=self.tmp_pops[index][dim], scale=0.1)
                    if rand_p < self.scale[dim][0] or rand_p > self.scale[dim][1]:
                        # self.tmp_pops[index][dim] = prob_pops[index][dim]
                        pass
                    else:
                        self.tmp_pops[index][dim] = rand_p
                        pass
        # 变异 - 交换两个维度值
        for index in range(self.pop_nums):
            change_index = sorted(np.random.choice(self.dims, 2, replace=False))
            i, j = change_index[0], change_index[1]
            self.tmp_pops[index][i], self.tmp_pops[index][j] = self.tmp_pops[index][j], self.tmp_pops[index][i]
        # print("mut_groups:%s" % mut_groups)
        # print("mutation生成的tmp_pops")
        # print(self.tmp_pops)
        pass

    def crossover(self):
        # 选择父母
        parents_groups = self.select_parents()
        # 交叉基因位
        certain_cross_seq = np.random.randint(0, self.dims, self.pop_nums)  # 保证每个父本个体有一个等位基因被交叉
        prob_cross_seq = np.random.rand(self.pop_nums, self.dims) < self.cross_prob  # 按概率交叉
        # 交叉
        for index in range(self.pop_nums):
            parents = parents_groups[index]
            dad, mom = self.pops[parents[0]], self.pops[parents[1]]
            prob_cross_seq[index][certain_cross_seq[index]] = True
            # 交叉 - 等位点基因交换
            dad_ga = dad * prob_cross_seq[index]
            mom_ga = mom * (1 - prob_cross_seq[index])
            child = dad_ga + mom_ga
            # 交叉 - 等位点基因求均值
            # mean_parent = ((dad + mom) / 2) * prob_cross_seq[index]
            # mom_ga = mom * (1 - prob_cross_seq[index])
            # child = mean_parent + mom_ga
            # 直接求均值
            # child = ((dad + mom) / 2)
            # 交叉 - 差分向量方式进行交叉
            # child = mom + 0.1 * (dad - mom) * prob_cross_seq[index]
            #
            self.tmp_pops[index] = child
        #
        # print(certain_cross_seq)
        # print(ga)
        # print("crossover后的tmp_pops")
        # print(self.tmp_pops)
        pass

    def select_parents(self):
        # 评估种群
        self.pops_evaluation()
        # 记录当前最优个体
        best_ans_index = np.argmin(self.pops_fitness)
        best_fitness = self.pops_fitness[best_ans_index]
        if best_fitness < self.best_ans_fitness:
            self.best_ans = cp.deepcopy(self.pops[best_ans_index])
            self.best_ans_fitness = best_fitness
        else:
            # 保留当前最好个体  - 替换最差个体
            bad_index = np.argmax(self.pops_fitness)
            self.pops[bad_index] = cp.deepcopy(self.best_ans)
        # 选择父母组
        cross_groups = []
        # 随机选择父母组
        # cross_groups = [np.random.choice(self.pop_nums, 2, replace=False) for _ in range(self.pop_nums)]
        # 轮盘赌选择父母组
        fitness = cp.deepcopy(self.pops_fitness)
        fitness = 1 - (fitness / np.sum(fitness))
        fitness = fitness / np.sum(fitness)
        prob_fitness = np.random.rand(self.pop_nums, 2)
        # print(fitness)
        # print(np.sum(fitness))
        # print(prob_fitness)
        for p_index in range(self.pop_nums):
            parents = np.random.choice(self.pop_nums, size=2, replace=False, p=fitness)
            # parents = []
            # prob_sum = 0
            # for f_index in range(self.pop_nums):
            #     prob_sum += fitness[f_index]
            #     if prob_sum > prob_fitness[p_index][0]:
            #         parents.append(f_index)
            #         break
            # prob_sum = 0
            # for f_index in range(self.pop_nums):
            #     prob_sum += fitness[f_index]
            #     if prob_sum > prob_fitness[p_index][1]:
            #         parents.append(f_index)
            #         break
            dad_index, mom_index = parents[0], parents[1]
            if self.pops_fitness[dad_index] < self.pops_fitness[mom_index]:
                parents[0], parents[1] = parents[1], parents[0]
            cross_groups.append(parents)
        return cross_groups

    def update_pops(self):
        # 评估交叉变异后的临时种群 - 不需要
        # self.tmp_pops_evaluation()
        # 将交叉变异后的临时种群作为当前种群
        self.pops = cp.deepcopy(self.tmp_pops)
        pass

    def pops_evaluation(self):
        for index in range(self.pop_nums):
            self.pops_fitness[index] = self.function(self.pops[index])
        # print("pops_fitness: %s " % self.pops_fitness)
        # print("tmp_pops_fitness: %s " % self.tmp_pops_fitness)
        pass

    def tmp_pops_evaluation(self):
        for index in range(self.pop_nums):
            self.tmp_pops_fitness[index] = self.function(self.tmp_pops[index])
        # print("pops_fitness: %s " % self.pops_fitness)
        # print("tmp_pops_fitness: %s " % self.tmp_pops_fitness)
        pass

    def generate(self):
        """
        交叉变异操作
        """
        self.crossover()
        self.mutation()

    def iteration(self):
        """
        当前解，生成的下一步解，在生成的下一步解和当前解之间进行selection
        生成下一步解：引导方向，行走步长
        selection：控制方向，避免搜索已经被搜索过的差解，这是比随机方法好的原因
        """
        self.initiation()
        for iter_i in range(self.iters):
            # print("--------- iter_i: %s ---------" % iter_i)
            self.select_parents()
            self.generate()
            self.update_pops()
            # print("最优值")
            # print(self.best_ans_fitness)
        # print("iteration后的pops")
        # print(self.pops)
        # print("best_ans")
        # print(self.best_ans)
        print("最优值")
        print(self.best_ans_fitness)
        pass
    pass


class GATsp(GA):
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
        self.dims = len(self.citys)  # 解的dims
        self.function = self.value_func  # 评估function
        self.best_ans = None
        # 获取城市间的距离
        self.dims = self.dims
        self.citys_distance = np.zeros((self.dims, self.dims))  # 两两城市之间的距离
        self.get_citys_distance()

    def initiation(self):
        np.random.seed(65536)
        self.best_ans = np.arange(self.dims) if self.best_ans is None else self.best_ans
        self.best_ans_fitness = self.function(self.best_ans)
        self.pops = np.array([np.random.choice(self.dims, self.dims, replace=False) for _ in range(self.pop_nums)])
        self.pops[np.random.randint(self.pop_nums)] = cp.deepcopy(self.best_ans)
        self.tmp_pops = cp.deepcopy(self.pops)
        self.pops_fitness = np.zeros(self.pop_nums)
        self.tmp_pops_fitness = np.zeros(self.pop_nums)

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
        # next_ans[i], next_ans[j] = next_ans[j], next_ans[i]   # 两点交换
        while i < j:
            # 片段内的所有点交换
            next_ans[i], next_ans[j] = next_ans[j], next_ans[i]
            i += 1
            j -= 1
        # print(next_ans)
        return next_ans

    def mutation(self):
        """
        对tmp_pops个体进行mutation
        """
        # 对每个个体进行变异，方式为：交换解片段中的城市
        for index in range(self.pop_nums):
            mut_individual = self.get_next_ans(self.tmp_pops[index])
            self.tmp_pops[index] = mut_individual

    def crossover(self):
        """
        从pops中selection两个个体进行crossover到tmp_pops，需要避免多个城市重复问题
        """
        # 选择父母
        parents_groups = self.select_parents()
        # 交叉基因位
        prob_cross_seq = np.random.rand(self.pop_nums, self.dims) < self.cross_prob     # 以概率交叉
        # crossover
        for index in range(self.pop_nums):
            parents = parents_groups[index]
            dad, mom = self.pops[parents[0]], self.pops[parents[1]]
            dad_ga = np.array(list(set((dad + 1) * prob_cross_seq[index]) - set([0]))) - 1
            mom_ga = [mom[i] for i in range(self.dims) if mom[i] not in dad_ga]
            for dim in range(self.dims):
                if prob_cross_seq[index][dim]:
                    self.tmp_pops[index][dim] = dad[dim]
                else:
                    self.tmp_pops[index][dim] = mom_ga.pop(0)
            # print(dad)
            # print(mom)
            # print(self.tmp_pops[index])
        pass


    pass


if __name__ == "__main__":
    print("hello world!")
    ga = GA()
    ga.iters = 1000
    ga.pop_nums = 10
    SN = 30  # 多轮搜索，每次从上一次最优解开始搜索,因为一般一轮是不能很好地收敛到最优
    for si in range(SN):
        ga.iteration()

    # ga = GATsp()
    # ga.iters = 100 * ga.dimsss
    # ga.pop_nums = 5
    # SN = 3  # 多轮搜索，每次从上一次最优解开始搜索,因为一般一轮是不能很好地收敛到最优
    # for si in range(SN):
    #     ga.iteration()
    # print("best_ans")
    # print(ga.best_ans)
    # print("最优值")
    # print(ga.best_ans_fitness)
    # print(len(list(set(ga.best_ans))))
