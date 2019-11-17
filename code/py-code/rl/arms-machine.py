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
        self.rand_seed = 0
        self.steps = 10
        self.learn_alpha = 0.1
        self.epsilon = 0.1
        self.uniform_steps = 0.4
        self.q_value_init = 0
        self.arms = ["a", "b", "c", "d", "e", "f"]
        self.actions = ["action_a", "action_b", "action_c", "action_d", "action_e", "action_f"]
        self.rewards_normal_distribution = {
            "action_a": {"mean": 0, "std": 1},
            "action_b": {"mean": 0, "std": 1},
            "action_c": {"mean": 0, "std": 1},
            "action_d": {"mean": 0, "std": 1},
            "action_e": {"mean": 0, "std": 1},
            "action_f": {"mean": 0, "std": 1}
        }
        self.best_action = "action_a"
        self.best_reward = self.rewards_normal_distribution[self.best_action]["mean"]
        self.rand_rewards = []
        self.q_values = []
        self.algorithms = ["rand", "uniform", "e-greedy", "ucb", "ts"]
        self.results_keys = ["average_rewards", "sum_rewards", "sum_regrets", "actions", "optimal_action"]
        self.results = {}
        pass

    def generate_normal_distribution_rewards(self, mean=0, std=1, step=0):
        # np.random.seed(self.rand_seed)
        # norms = std * st.norm.rvs(size=self.steps+1) + mean
        reward = std * self.rand_rewards[step] + mean
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
        # iterating
        for t in range(self.steps):
            # print("----------step: %s -----------" % t)
            # choose action
            action_index = np.argmax(self.q_values)
            action_index_rand = np.random.choice(len(self.actions))
            if algorithms == "rand":
                action_index = action_index_rand
            if algorithms == "uniform" and t < self.uniform_steps * self.steps:
                action_index = action_index_rand
            if algorithms == "e-greedy" and np.random.rand() < self.epsilon:
                action_index = action_index_rand
            if algorithms == "ucb":
                action_index = (
                    t if t < len(self.actions)
                    else np.argmax(self.q_values + 2.0 * np.sqrt(np.log(t + 1) / np.bincount(self.results["ucb"]["actions"])))
                )
            if algorithms == "ts":
                action_index = np.argmax(st.beta(positive_feedback, negative_feedback).rvs())
            action = self.actions[action_index]
            # apply action and observe reward
            mean = self.rewards_normal_distribution[action]["mean"]
            std = self.rewards_normal_distribution[action]["std"]
            reward = self.generate_normal_distribution_rewards(mean=mean, std=std, step=t)
            # update estimated model
            q_action = self.q_values[action_index]
            self.q_values[action_index] = q_action + (reward - q_action) / (t + 1)
            if algorithms == "ts":
                positive_feedback[action_index] += (1 if reward >= q_action else 0)
                negative_feedback[action_index] += (1 if reward < q_action else 0)
            # record results
            average_reward = self.results[algorithms]["average_rewards"][-1]
            average_reward += (reward - average_reward) / (t + 1)
            self.results[algorithms]["average_rewards"].append(average_reward)
            regret = self.best_reward - self.rewards_normal_distribution[action]["mean"]
            self.results[algorithms]["sum_regrets"].append(self.results[algorithms]["sum_regrets"][-1] + regret)
            self.results[algorithms]["sum_rewards"].append(self.results[algorithms]["sum_rewards"][-1] + reward)
            self.results[algorithms]["actions"].append(action_index)
            optimal_action = self.results[algorithms]["optimal_action"][-1]
            optimal_action += ((1 if action == self.best_action else 0) - optimal_action) / (t + 1)
            self.results[algorithms]["optimal_action"].append(optimal_action)
        pass

    def compare_results(self):
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
            if ret == "actions":
                pass
            for alg in algorithms:
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
    ab.steps = 10
    for algs in ab.algorithms:
        ab.action_choice_algorithms(algs)
    ab.action_choice_algorithms("ts")
    ab.compare_results()
