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
        self.steps = 1000
        self.learn_alpha = 0.1
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
        self.rand_rewards = st.norm.rvs(size=self.steps+1)
        self.algorithms = ["rand", "uniform", "e-greedy", "ucb", "ts"]
        self.results = {
            "rand": {"sum_rewards": [0], "average_rewards": [0], "sum_regrets": [0], "actions": [], "optimal_action": [0]},
            "uniform": {"sum_rewards": [0], "average_rewards": [0], "sum_regrets": [0], "actions": [], "optimal_action": [0]},
            "e-greedy": {"sum_rewards": [0], "average_rewards": [0], "sum_regrets": [0], "actions": [], "optimal_action": [0]},
            "ucb": {"sum_rewards": [0], "average_rewards": [0], "sum_regrets": [0], "actions": [], "optimal_action": [0]},
            "ts": {"sum_rewards": [0], "average_rewards": [0], "sum_regrets": [0], "actions": [], "optimal_action": [0]}
        }
        pass

    def generate_normal_distribution_rewards(self, mean=0, std=1, step=0):
        # np.random.seed(self.rand_seed)
        # norms = std * st.norm.rvs(size=self.steps+1) + mean
        reward = std * self.rand_rewards[step] + mean
        return reward

    def action_choice_algorithms(self, algorithms='rand'):
        # define q-value of actions
        q_values = self.q_value_init * np.ones((len(self.actions), 1))
        for t in range(self.steps):
            # choose action
            action_index = np.argmax(self.q_values[..., 0])
            action = self.actions[action_index]
            # apply action and observe reward
            mean = self.rewards_normal_distribution[action]["mean"]
            std = self.rewards_normal_distribution[action]["std"]
            reward = self.generate_normal_distribution_rewards(mean=mean, std=std)
            # update estimated model
            q_action = q_values[action_index][0]
            q_values[action_index][0] = q_action + (reward - q_action) / (t + 1)
            # record results
            average_reward = self.results[algorithms]["average_rewards"][-1]
            average_reward = average_reward + (reward - average_reward) / (t + 1)
            self.results[algorithms]["average_rewards"].append(average_reward)
            regret = self.best_reword - self.rewards_normal_distribution[action]["mean"]
            self.results[algorithms]["sum_regrets"].append(self.results[algorithms]["sum_regrets"][-1] + regret)
            self.results[algorithms]["sum_rewards"].append(self.results[algorithms]["sum_rewards"][-1] + reward)
            self.results[algorithms]["actions"].append(action_index)
            optimal_action = self.results[algorithms]["optimal_action"][-1]
            if action == self.best_action:
                optimal_action = optimal_action + (1 - optimal_action) / (t + 1)
            else:
                optimal_action = optimal_action + (0 - optimal_action) / (t + 1)
            self.results[algorithms]["optimal_action"].append(optimal_action)
        pass

    def compare_results(self):
        # table of reward and regret
        # average reward
        # accumulated reward
        # accumulated regrets
        # actions
        # optimal action
        pass

    pass


class Bandit():
    def __init__(self):
        self.steps = 1000
        self.arms = 3
        self.epsilon = 0.4
        self.arms_rewords_bernoulli = [0.6, 0.4, 0.8]
        self.best_reword = np.max(self.arms_rewords_bernoulli)
        self.estimate_rewords = 0.5 * np.ones((self.arms, self.steps))
        self.positive_feedback = [1, 1, 1]
        self.negative_feedback = [1, 1, 1]
        self.regrets = [0]
        self.accumulate_rewords = [0]
        self.choices = np.zeros(self.steps)
        pass

    def rand_choice(self):
        for t in range(self.steps):
            # estimate model
            for k in range(self.arms):
                r = ((float)(self.positive_feedback[k]) / (self.positive_feedback[k] + self.negative_feedback[k]))
                self.estimate_rewords[k][t] = r

            # choose action
            best_action = np.random.choice(range(self.arms))
            self.choices[t] = best_action

            # apply action and observe
            bernoulli = stats.bernoulli(self.arms_rewords_bernoulli[best_action])
            posi = bernoulli.rvs()
            negt = 1 - posi

            # update estimate
            self.positive_feedback[best_action] += posi
            self.negative_feedback[best_action] += negt

            # regret
            regret = self.best_reword - self.arms_rewords_bernoulli[best_action]
            self.regrets.append(self.regrets[-1] + regret)

            # accumulate rewords
            self.accumulate_rewords.append(self.accumulate_rewords[-1] + posi)

            # update memory

        print("accumulate rewords of rand is: %s" % self.accumulate_rewords[-1])
        print("regrets of rand is: %.2f" % self.regrets[-1])
        # plot
        fig, ax = plt.subplots()
        for k in range(self.arms):
            ax.plot(range(self.steps), self.estimate_rewords[k],
                    label='action_%s(%s)' % (k, self.arms_rewords_bernoulli[k]))
        ax.plot(range(self.steps), -0.1 * self.choices, label='choice')
        ax.set(title="rand-choice-estimate-rewords")
        ax.legend()

        return self.regrets, self.accumulate_rewords

    def uniform_greedy(self):
        for t in range(self.steps):
            # estimate model
            for k in range(self.arms):
                r = ((float)(self.positive_feedback[k]) / (self.positive_feedback[k] + self.negative_feedback[k]))
                self.estimate_rewords[k][t] = r

            # choice action
            if t < self.epsilon * self.steps:
                best_action = np.random.choice(range(self.arms))
            else:
                best_action = np.argmax(self.estimate_rewords[..., t])
            self.choices[t] = best_action

            # apply action and observe
            bernoulli = stats.bernoulli(self.arms_rewords_bernoulli[best_action])
            posi = bernoulli.rvs()
            negt = 1 - posi

            # update estimate
            self.positive_feedback[best_action] += posi
            self.negative_feedback[best_action] += negt

            # regret
            regret = self.best_reword - self.arms_rewords_bernoulli[best_action]
            self.regrets.append(self.regrets[-1] + regret)

            # accumulate rewords
            self.accumulate_rewords.append(self.accumulate_rewords[-1] + posi)

            # update memory

        print("accumulate rewords of uniform-greedy is: %s" % self.accumulate_rewords[-1])
        print("regrets of uniform-greedy is: %.2f" % self.regrets[-1])
        # plot
        fig, ax = plt.subplots()
        for k in range(self.arms):
            ax.plot(range(self.steps), self.estimate_rewords[k],
                    label='action_%s(%s)' % (k, self.arms_rewords_bernoulli[k]))
        ax.plot(range(self.steps), -0.1 * self.choices, label='choice')
        ax.set(title="uniform-greedy-estimate-rewords")
        ax.legend()

        return self.regrets, self.accumulate_rewords

    def e_greedy(self):
        for t in range(self.steps):
            # estimate model
            for k in range(self.arms):
                r = ((float)(self.positive_feedback[k]) / (self.positive_feedback[k] + self.negative_feedback[k]))
                self.estimate_rewords[k][t] = r

            # choice action
            if np.random.rand() < self.epsilon:
                best_action = np.random.choice(range(self.arms))
            else:
                best_action = np.argmax(self.estimate_rewords[..., t])
            self.choices[t] = best_action

            # apply action and observe
            bernoulli = stats.bernoulli(self.arms_rewords_bernoulli[best_action])
            posi = bernoulli.rvs()
            negt = 1 - posi

            # update estimate
            self.positive_feedback[best_action] += posi
            self.negative_feedback[best_action] += negt

            # regret
            regret = self.best_reword - self.arms_rewords_bernoulli[best_action]
            self.regrets.append(self.regrets[-1] + regret)

            # accumulate rewords
            self.accumulate_rewords.append(self.accumulate_rewords[-1] + posi)

            # update memory

        print("accumulate rewords of e-greedy is: %s" % self.accumulate_rewords[-1])
        print("regrets of e-greedy is: %.2f" % self.regrets[-1])
        # plot
        fig, ax = plt.subplots()
        for k in range(self.arms):
            ax.plot(range(self.steps), self.estimate_rewords[k],
                    label='action_%s(%s)' % (k, self.arms_rewords_bernoulli[k]))
        ax.plot(range(self.steps), -0.1 * self.choices, label='choice')
        ax.set(title="e-greedy-estimate-rewords")
        ax.legend()

        return self.regrets, self.accumulate_rewords

    def adaptive_e_greedy(self):
        for t in range(self.steps):
            # estimate model
            for k in range(self.arms):
                r = ((float)(self.positive_feedback[k]) / (self.positive_feedback[k] + self.negative_feedback[k]))
                self.estimate_rewords[k][t] = r

            # choice action
            if np.random.rand() < self.epsilon * (1.0 - t / self.steps):
                best_action = np.random.choice(range(self.arms))
            else:
                best_action = np.argmax(self.estimate_rewords[..., t])
            self.choices[t] = best_action

            # apply action and observe
            bernoulli = stats.bernoulli(self.arms_rewords_bernoulli[best_action])
            posi = bernoulli.rvs()
            negt = 1 - posi

            # update estimate
            self.positive_feedback[best_action] += posi
            self.negative_feedback[best_action] += negt

            # regret
            regret = self.best_reword - self.arms_rewords_bernoulli[best_action]
            self.regrets.append(self.regrets[-1] + regret)

            # accumulate rewords
            self.accumulate_rewords.append(self.accumulate_rewords[-1] + posi)

            # update memory

        print("accumulate rewords of adaptive_e-greedy is: %s" % self.accumulate_rewords[-1])
        print("regrets of adaptive_e-greedy is: %.2f" % self.regrets[-1])
        # plot
        fig, ax = plt.subplots()
        for k in range(self.arms):
            ax.plot(range(self.steps), self.estimate_rewords[k],
                    label='action_%s(%s)' % (k, self.arms_rewords_bernoulli[k]))
        ax.plot(range(self.steps), -0.1 * self.choices, label='choice')
        ax.set(title="adaptive_e_greedy-estimate-rewords")
        ax.legend()

        return self.regrets, self.accumulate_rewords

    def ucb(self):
        # select all action once time
        for k in range(self.arms):
            # apply action and observe
            bernoulli = stats.bernoulli(self.arms_rewords_bernoulli[k])
            posi = bernoulli.rvs()
            negt = 1 - posi

            # update estimate
            self.positive_feedback[k] += posi
            self.negative_feedback[k] += negt
        #
        for t in range(self.steps):
            # estimate model
            for k in range(self.arms):
                k_arms = self.positive_feedback[k] + self.negative_feedback[k]
                r = ((1.0 * self.positive_feedback[k]) / k_arms)
                bound = np.sqrt((2.0 * np.log(t + 1)) / k_arms)
                ucb = r + bound
                self.estimate_rewords[k][t] = ucb
                # self.estimate_rewords[k][t] = r

            # choice action
            best_action = np.argmax(self.estimate_rewords[..., t])
            self.choices[t] = best_action

            # apply action and observe
            bernoulli = stats.bernoulli(self.arms_rewords_bernoulli[best_action])
            posi = bernoulli.rvs()
            negt = 1 - posi

            # update estimate
            self.positive_feedback[best_action] += posi
            self.negative_feedback[best_action] += negt

            # regret
            regret = self.best_reword - self.arms_rewords_bernoulli[best_action]
            self.regrets.append(self.regrets[-1] + regret)

            # accumulate rewords
            self.accumulate_rewords.append(self.accumulate_rewords[-1] + posi)

            # update memory

        print("accumulate rewords of ucb is: %s" % self.accumulate_rewords[-1])
        print("regrets of ucb is: %.2f" % self.regrets[-1])
        # plot
        fig, ax = plt.subplots()
        for k in range(self.arms):
            ax.plot(range(self.steps), self.estimate_rewords[k],
                    label='action_%s(%s)' % (k, self.arms_rewords_bernoulli[k]))
        ax.plot(range(self.steps), -0.1 * self.choices, label='choice')
        ax.set(title="ucb-estimate-rewords")
        ax.legend()

        return self.regrets, self.accumulate_rewords

    def tompson_sampling(self):
        for t in range(self.steps):
            # estimate model
            for k in range(self.arms):
                r = stats.beta(self.positive_feedback[k], self.negative_feedback[k]).rvs()
                self.estimate_rewords[k][t] = r

            # choice action
            best_action = np.argmax(self.estimate_rewords[..., t])
            self.choices[t] = best_action

            # apply action and observe
            bernoulli = stats.bernoulli(self.arms_rewords_bernoulli[best_action])
            posi = bernoulli.rvs()
            negt = 1 - posi

            # update estimate
            self.positive_feedback[best_action] += posi
            self.negative_feedback[best_action] += negt

            # regret
            regret = self.best_reword - self.arms_rewords_bernoulli[best_action]
            self.regrets.append(self.regrets[-1] + regret)

            # accumulate rewords
            self.accumulate_rewords.append(self.accumulate_rewords[-1] + posi)

            # update memory

        print("accumulate rewords of ts is: %s" % self.accumulate_rewords[-1])
        print("regrets of ts is: %.2f" % self.regrets[-1])
        # plot
        fig, ax = plt.subplots()
        for k in range(self.arms):
            ax.plot(range(self.steps), self.estimate_rewords[k],
                    label='action_%s(%s)' % (k, self.arms_rewords_bernoulli[k]))
        ax.plot(range(self.steps), -0.1 * self.choices, label='choice')
        ax.set(title="ts-estimate-rewords")
        ax.legend()

        return self.regrets, self.accumulate_rewords

    def compare(self):
        bandit = Bandit()
        regrets_rand, accumulate_rewords_rand = Bandit().rand_choice()
        regrets_uniform, accumulate_rewords_uniform = Bandit().uniform_greedy()
        regrets_e_greedy, accumulate_rewords_e_greedy = Bandit().e_greedy()
        regrets_adaptive_e_greedy, accumulate_rewords_adaptive_e_greedy = Bandit().adaptive_e_greedy()
        regrets_tompson_sampling, accumulate_rewords_tompson_sampling = Bandit().tompson_sampling()
        regrets_ucb, accumulate_rewords_ucb = Bandit().ucb()

        fig2, ax2 = plt.subplots()
        ax2.plot(range(self.steps), regrets_rand[0:-1], label='rand')
        ax2.plot(range(self.steps), regrets_uniform[0:-1], label='uniform')
        ax2.plot(range(self.steps), regrets_e_greedy[0:-1], label='e_greedy')
        ax2.plot(range(self.steps), regrets_adaptive_e_greedy[0:-1], label='adaptive_e_greedy')
        ax2.plot(range(self.steps), regrets_tompson_sampling[0:-1], label='tompson_sampling')
        ax2.plot(range(self.steps), regrets_ucb[0:-1], label='ucb')
        ax2.set(title="regret")
        ax2.legend()

        #         fig3, ax3 = plt.subplots()
        #         ax3.plot(range(self.steps), accumulate_rewords_rand[0:-1], label = 'rand')
        #         ax3.plot(range(self.steps), accumulate_rewords_uniform[0:-1], label = 'uniform')
        #         ax3.plot(range(self.steps), accumulate_rewords_e_greedy[0:-1], label = 'e_greedy')
        #         ax3.plot(range(self.steps), accumulate_rewords_adaptive_e_greedy[0:-1], label = 'adaptive_e_greedy')
        #         ax3.plot(range(self.steps), accumulate_rewords_tompson_sampling[0:-1], label = 'tompson_sampling')
        #         ax3.plot(range(self.steps), accumulate_rewords_ucb[0:-1], label = 'ucb')
        #         ax3.set(title="accumulate_rewords")
        #         ax3.legend()

        plt.show()

        pass


if __name__ == "__main__":
    print("hello world!")
    # Bandit().compare()
    np.random.seed(10)
    # N_points = 1000
    # n_bins = 20
    # x = np.random.randn(1000)
    # y = .4 * x + 5
    # fig, axs = plt.subplots(1, 1, sharey=True, tight_layout=True)
    # axs.hist(x, bins=n_bins)
    # # axs[0].hist(x, bins=n_bins)
    # # axs[1].hist(y, bins=n_bins)
    # plt.show()

    # npr = np.random.randn(2,3)
    # print(npr)
    # print(npr[..., 2])

    print(np.ones((3, 1)))