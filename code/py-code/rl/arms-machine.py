#!/usr/bin/python
# coding=utf-8

__doc__ = """
5臂赌博机试验
"""

import matplotlib.pyplot as plt
import numpy as np
from scipy import stats


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

            # choice action
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
    Bandit().compare()