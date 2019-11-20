#!/usr/bin/python
# coding=utf-8

__doc__ = """
多臂赌博机试验
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
        print("algorithm is: %s" % algorithms)
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
            self.q_values[action_index] += (reward - q_action) / actions_count[action_index]
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
        print("action\treward_mean\treward_std")
        for ak in self.rewards_distribution.keys():
            print("%s\t%s\t%s\t" % (ak, self.rewards_distribution[ak]["mean"], self.rewards_distribution[ak]["std"]))
            # plot distribution
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
                axs.plot(range(len(self.results[alg][ret])), self.results[alg][ret], label=alg)
            axs.set(title=ret)
            axs.legend()
        # show
        plt.show()


if __name__ == "__main__":
    print("hello world!")
    ab = ArmsBandit()
    ab.steps = 1000 * 3
    N_CMP = 100
    # 对比100次运行后的算法效果，当具有相同方差,不同均值时
    # define result
    compare_results = {
        "ts": {"sum_reward": [], "sum_regret": [], "optimal_action": []},
        "ucb": {"sum_reward": [], "sum_regret": [], "optimal_action": []},
        "e-greedy": {"sum_reward": [], "sum_regret": [], "optimal_action": []}
    }
    for n in range(N_CMP):
        print(" ------------- N_CMP: %s -------------" % n)
        # generate standard normal rand rewards
        ab.rand_rewards = np.random.randn(ab.steps + 1)
        # run ts algorithm
        ab.action_choice_algorithms("ts")
        # record result
        compare_results["ts"]["sum_reward"].append(ab.results["ts"]["sum_rewards"][-1])
        compare_results["ts"]["sum_regret"].append(ab.results["ts"]["sum_regrets"][-1])
        compare_results["ts"]["optimal_action"].append(ab.results["ts"]["optimal_action"][-1])
        # run ts algorithm
        ab.action_choice_algorithms("ucb")
        # record result
        compare_results["ucb"]["sum_reward"].append(ab.results["ucb"]["sum_rewards"][-1])
        compare_results["ucb"]["sum_regret"].append(ab.results["ucb"]["sum_regrets"][-1])
        compare_results["ucb"]["optimal_action"].append(ab.results["ucb"]["optimal_action"][-1])
        # run ts algorithm
        ab.action_choice_algorithms("e-greedy")
        # record result
        compare_results["e-greedy"]["sum_reward"].append(ab.results["e-greedy"]["sum_rewards"][-1])
        compare_results["e-greedy"]["sum_regret"].append(ab.results["e-greedy"]["sum_regrets"][-1])
        compare_results["e-greedy"]["optimal_action"].append(ab.results["e-greedy"]["optimal_action"][-1])

    rets = {}
    for alg in compare_results.keys():
        for ret in compare_results[alg].keys():
            ret_mean = np.mean(compare_results[alg][ret])
            ret_std = np.std(compare_results[alg][ret])
            if ret not in rets:
                rets.update({ret: {}})
            if alg not in rets[ret]:
                rets[ret].update({alg: {}})
            rets[ret][alg] = {"mean": ret_mean, "std": ret_std}

    print("alg\t\tmean\t\tstd")
    for ret in rets.keys():
        print("--- %s ----------" % ret)
        for alg in rets[ret].keys():
            print("%s " % alg + " mean: %s" % rets[ret][alg]["mean"] + "  std: %s" % rets[ret][alg]["std"])

    ab.compare_results()
