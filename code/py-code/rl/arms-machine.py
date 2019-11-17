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
        self.mean_std = [[.1, 1], [.2, 1], [.3, 1], [.4, 1], [.5, 1], [.6, 1]]
        # self.mean_std = [[.1, 1], [.2, 1], [.4, 1]]
        self.arms = [chr(97+i) for i in range(len(self.mean_std))]
        self.actions = ["action_" + act for act in self.arms]
        self.rewards_distribution = {}
        [self.rewards_distribution.update({self.actions[i]: {"mean": self.mean_std[i][0], "std": self.mean_std[i][1]}})
         for i in range(len(self.mean_std))]
        self.best_action = self.actions[np.argmax(np.array(self.mean_std)[..., 0])]
        self.best_reward = self.rewards_distribution[self.best_action]["mean"]
        self.rand_rewards = []
        self.q_values = []
        self.algorithms = ["rand", "uniform", "e-greedy", "ucb", "ts"]
        self.results_keys = ["average_rewards", "sum_rewards", "sum_regrets", "actions", "optimal_action"]
        self.results = {}
        pass

    def generate_rewards(self, mean=0, std=1, step=0):
        # np.random.seed(self.rand_seed)
        # norms = std * st.norm.rvs(size=self.steps+1) + mean
        reward = std * self.rand_rewards[step] + mean
        # reward = std * st.norm.rvs() + mean
        return reward

    def action_choice_algorithms(self, algorithms='rand'):
        print("algorithm is: %s" % algorithms)
        if algorithms not in self.algorithms:
            return "algorithms not existed!"
        # generate standard normal rand rewards
        np.random.seed(self.rand_seed)
        self.rand_rewards = st.norm.rvs(size=self.steps + 1)
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
            rewards_mm = [0, 1]
        # choose action one by one before iterating
        self.results[algorithms]["actions"].clear()
        for action_index in range(len(self.actions)):
            # choose action
            action = self.actions[action_index]
            # apply action and observe reward
            mean = self.rewards_distribution[action]["mean"]
            std = self.rewards_distribution[action]["std"]
            reward = self.generate_rewards(mean=mean, std=std, step=action_index)
            # update estimated model
            self.q_values[action_index] = (reward + self.q_values[action_index]) / 2
            # record results
            self.results[algorithms]["actions"].append(action_index)
            pass
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
                action_index = np.argmax(self.q_values + np.sqrt(2.0 * np.log(t + 1) / actions_count))
            if algorithms == "ts":
                action_index = np.argmax(st.beta(positive_feedback, negative_feedback).rvs())
            action = self.actions[action_index]
            # apply action and observe reward
            mean = self.rewards_distribution[action]["mean"]
            std = self.rewards_distribution[action]["std"]
            reward = self.generate_rewards(mean=mean, std=std, step=t)
            # update estimated model
            q_action = self.q_values[action_index]
            self.q_values[action_index] = q_action + (reward - q_action) / actions_count[action_index]
            if algorithms == "ts":
                ts_mean = st.beta.mean(positive_feedback[action_index], negative_feedback[action_index])
                positive_feedback[action_index] += (1 if q_action >= ts_mean else 0)
                negative_feedback[action_index] += (1 if q_action < ts_mean else 0)
            # record results
            average_reward = self.results[algorithms]["average_rewards"][-1]
            average_reward += (reward - average_reward) / (t + 1)
            self.results[algorithms]["average_rewards"].append(average_reward)
            regret = self.best_reward - self.rewards_distribution[action]["mean"]
            self.results[algorithms]["sum_regrets"].append(self.results[algorithms]["sum_regrets"][-1] + regret)
            self.results[algorithms]["sum_rewards"].append(self.results[algorithms]["sum_rewards"][-1] + reward)
            self.results[algorithms]["actions"].append(action_index)
            optimal_action = self.results[algorithms]["optimal_action"][-1]
            optimal_action += ((1 if action == self.best_action else 0) - optimal_action) / (t + 1)
            self.results[algorithms]["optimal_action"].append(optimal_action)
        # print("q_values is ")
        # print(self.q_values)
        pass

    def compare_results(self):
        # rewards distribution
        print("----------------- rewards distribution ----------------------")
        print("action\treward_mean\treward_std")
        for ak in self.rewards_distribution.keys():
            print("%s\t%s\t%s\t" % (ak, self.rewards_distribution[ak]["mean"], self.rewards_distribution[ak]["std"]))
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
                    axs.scatter(range(len(self.results[alg][ret])), self.results[alg][ret], label=alg)
                    continue
                axs.plot(range(len(self.results[alg][ret])), self.results[alg][ret], label=alg)
            axs.set(title=ret)
            axs.legend()
        # show
        plt.show()
        pass

    pass


if __name__ == "__main__":
    print("hello world!")
    ab = ArmsBandit()
    ab.steps = 1000 * 20
    # for algs in ab.algorithms:
    #     ab.action_choice_algorithms(algs)
    ab.action_choice_algorithms("rand")
    ab.action_choice_algorithms("e-greedy")
    ab.action_choice_algorithms("uniform")
    ab.action_choice_algorithms("ucb")
    ab.action_choice_algorithms("ts")

    ab.compare_results()
