#!/usr/bin/python
# coding=utf-8

__doc__ = """
多臂赌博机试验
实现多个选择动作算法：rand/uniform/e-greedy/ucb/ts
并对这些算法的运行结果进行比较
算法实现在action_choice_algorithms方法里
总体说来，e-greedy算法泛化性最好，ucb算法在获得最大回报时可能表现得更好，但方差也较大，
ts算法在奖励为0到1之间时，平均表现是最好的，同样，方差也较大，介于e-greedy方法和ucb方法之间
"""

import matplotlib.pyplot as plt
import numpy as np
from scipy import stats as st


class ArmsBandit(object):
    def __init__(self):
        self.rand_seed = 100
        self.steps = 1000
        self.learn_alpha = 0.1
        self.epsilon = 0.1
        self.uniform_steps = 0.4
        self.q_value_init = 0
        self.mean_std = [[.3, 1], [.4, 1], [.6, 1], [.5, 1], [.2, 1]]
        self.arms = [chr(97+i) for i in range(len(self.mean_std))]
        self.actions = ["action_" + act for act in self.arms]
        self.rewards_distribution = {}
        [self.rewards_distribution.update({self.actions[i]: {"mean": self.mean_std[i][0], "std": self.mean_std[i][1]}})
         for i in range(len(self.mean_std))]
        self.best_action = self.actions[np.argmax(np.array(self.mean_std)[..., 0])]
        self.best_reward = self.rewards_distribution[self.best_action]["mean"]
        self.rand_rewards = np.random.randn(self.steps + 1)
        self.q_values = []
        self.algorithms = ["rand", "uniform", "e-greedy", "ucb", "ts"]
        self.results_keys = ["average_rewards", "sum_rewards", "sum_regrets", "actions", "optimal_action"]
        self.results = {}

    def generate_rewards(self, mean=0, std=1, step=0):
        reward = std * self.rand_rewards[step] + mean
        return reward

    def action_choice_algorithms(self, algorithms='rand'):
        # print("algorithm is: %s" % algorithms)
        if algorithms not in self.algorithms:
            return "algorithms not existed!"
        # define result
        self.results.update({algorithms: {}})
        for ret in self.results_keys:
            self.results[algorithms].update({ret: [0]})
        # define q-value of actions
        self.q_values = self.q_value_init * np.ones(len(self.actions))
        # define feedback of ts algorithm
        if algorithms == "ts":
            positive_feedback = np.ones(len(self.actions))
            negative_feedback = np.ones(len(self.actions))
        # choose action one by one before iterating
        self.results[algorithms]["actions"].clear()
        self.results[algorithms]["actions"] += range(len(self.actions))
        # iterating
        for t in range(self.steps):
            # print("----------step: %s -----------" % t)
            # choose action
            action_index = np.argmax(self.q_values)
            action_index_rand = np.random.choice(range(len(self.actions)))
            actions_count = np.bincount(self.results[algorithms]["actions"])
            if algorithms == "rand":
                action_index = action_index_rand
            if algorithms == "uniform" and t < self.uniform_steps * self.steps:
                action_index = action_index_rand
            if algorithms == "e-greedy" and np.random.rand() < self.epsilon:
                action_index = action_index_rand
            if algorithms == "ucb":
                action_index = np.argmax(self.q_values + np.sqrt(2.0 * np.log(t + len(self.actions)) / actions_count))
            if algorithms == "ts":
                action_index = np.argmax(st.beta(positive_feedback, negative_feedback).rvs())
            action = self.actions[action_index]
            # apply action and observe reward
            mean = self.rewards_distribution[action]["mean"]
            std = self.rewards_distribution[action]["std"]
            reward = self.generate_rewards(mean=mean, std=std, step=t)
            # update estimated model
            q_action = self.q_values[action_index]
            # self.q_values[action_index] += (reward - q_action) / actions_count[action_index] # 增量平均
            self.q_values[action_index] += self.learn_alpha * (reward - q_action)   # 指数平均，适用于非平稳问题
            if algorithms == "ts":
                ts_mean = st.beta.mean(positive_feedback, negative_feedback)[action_index]
                q_action = self.q_values[action_index]
                positive_feedback[action_index] += (q_action >= ts_mean)
                negative_feedback[action_index] += (q_action < ts_mean)
            # record results
            average_reward = self.results[algorithms]["average_rewards"][-1]
            average_reward += (reward - average_reward) / (t + 1)
            self.results[algorithms]["average_rewards"].append(average_reward)
            regret = self.best_reward - self.rewards_distribution[action]["mean"]
            self.results[algorithms]["sum_regrets"].append(self.results[algorithms]["sum_regrets"][-1] + regret)
            self.results[algorithms]["sum_rewards"].append(self.results[algorithms]["sum_rewards"][-1] + reward)
            self.results[algorithms]["actions"].append(action_index)
            optimal_action = self.results[algorithms]["optimal_action"][-1]
            optimal_action += ((action == self.best_action) - optimal_action) / (t + 1)
            self.results[algorithms]["optimal_action"].append(optimal_action)

    def compare_results(self):
        # rewards distribution
        print("----------------- rewards distribution ----------------------")
        [self.rewards_distribution.update({self.actions[i]: {"mean": self.mean_std[i][0], "std": self.mean_std[i][1]}})
         for i in range(len(self.mean_std))]
        print("action\treward_mean\treward_std")
        fig, axs = plt.subplots()
        for ak in self.rewards_distribution.keys():
            print("%s\t%s\t%s\t" % (ak, self.rewards_distribution[ak]["mean"], self.rewards_distribution[ak]["std"]))
            mean = self.rewards_distribution[ak]["mean"]
            std = self.rewards_distribution[ak]["std"]
            x = np.linspace(st.norm(loc=mean, scale=std).ppf(0.1), st.norm(loc=mean, scale=std).ppf(0.99), 100)
            y = st.norm(loc=mean, scale=std).pdf(x)
            axs.plot(x, y, label="%s:%s-%s" % (ak, mean, std), alpha=0.6)
        axs.set(title="pdf of rewards")
        axs.legend()
        # table of sum reward and regret
        print("----------------- compare results ----------------------")
        print("algorithm\tsum_reward\tsum_regret")
        for alg in self.results.keys():
            print("%s\t%s\t%s" % (alg, self.results[alg]["sum_rewards"][-1], self.results[alg]["sum_regrets"][-1]))
            pass
        print("--------------------------------------------------------")
        # plot results
        algorithms = self.results.keys()
        for ret in self.results_keys:
            fig, axs = plt.subplots()
            for alg in algorithms:
                if ret == "actions":
                    axs.scatter(range(len(self.results[alg][ret])), self.results[alg][ret], label=alg, alpha=0.6)
                    continue
                axs.plot(range(len(self.results[alg][ret])), self.results[alg][ret], label=alg, alpha=0.6)
            axs.set(title=ret)
            axs.legend()
        # show
        plt.show()


if __name__ == "__main__":
    print("hello world!")
    ab = ArmsBandit()
    ab.steps = 1000 * 3
    N_CMP = 15
    cmp_algs = ["ts", "ucb", "e-greedy"]
    cmp_rets = ["sum_rewards", "sum_regrets", "optimal_action"]
    cmp_mean_std = [[[.3, 1], [.4, 1], [.6, 1], [.5, 1], [.2, 1]],  # 相同方差，不同均值
                    [[.5, 1], [.5, 3], [.5, 5], [.5, 4], [.5, 2]],  # 相同均值，不同方差
                    [[.3, 1], [.4, 3], [.6, 5], [.5, 4], [.2, 2]]]  # 不同均值，不同方差
    # 多次运行后的不同算法对不同分布的奖励的学习效果的均值和方差和对比
    for mean_std in cmp_mean_std[:1]:
        # define compare results & mean_std of rewards
        cmp_results = {}
        ab.mean_std = mean_std
        print("mean_std is: %s" % mean_std)
        for n in range(N_CMP):
            # print(" ------------- N_CMP: %s -------------" % n)
            # generate standard normal rand rewards
            ab.rand_rewards = np.random.randn(ab.steps + 1)
            # run algorithm & record results
            for alg in cmp_algs:
                ab.action_choice_algorithms(alg)
                for ret in cmp_rets:
                    if ret not in cmp_results:
                        cmp_results.update({ret: {}})
                    if alg not in cmp_results[ret]:
                        cmp_results[ret].update({alg: []})
                    cmp_results[ret][alg].append(ab.results[alg][ret][-1])

        # print compare results
        for ret in cmp_results.keys():
            print("--- %s ----------" % ret)
            for alg in cmp_results[ret].keys():
                print("%s " % alg + " mean: %.3f" % np.mean(cmp_results[ret][alg]) + " std: %.3f" % np.std(cmp_results[ret][alg]))

        # ab.compare_results()

    # 对某个算法进行结果观察
    # ab.action_choice_algorithms("ts")
    # ab.compare_results()
