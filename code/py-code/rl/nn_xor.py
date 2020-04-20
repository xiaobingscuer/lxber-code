#!/usr/bin/python
# coding=utf-8

__doc__ = """
tensorflow 搭建神经网络学习异或函数(xor)
"""

import numpy as np
import matplotlib.pyplot as plt
import math

import tensorflow as tf
from tensorflow.python.framework import ops


# create train data set
def create_datas(seed=1):
    np.random.seed(seed)
    train_num = 320
    X_train = np.random.rand(2, train_num).astype(np.float32)
    Y_train = np.round(X_train)
    # Y_train = np.sum(Y_train, axis=0) % 2
    Y_train = np.array([(Y_train[0, :] != Y_train[1, :]) * 1.0])

    print(X_train)
    print(Y_train)

    # create test data set
    X_test = np.random.rand(2, 10).astype(np.float32)
    Y_test = np.round(X_test)
    # Y_test = np.sum(Y_test, axis=0) % 2
    Y_test = np.array([(Y_test[0, :] != Y_test[1, :]) * 1.0])

    print(X_test)
    print(Y_test)

    return X_train, Y_train, X_test, Y_test


def create_placeholders(n_x, n_y):
    X = tf.placeholder(tf.float32, [n_x, None], name='X')
    Y = tf.placeholder(tf.float32, [n_y, None], name='Y')
    return X, Y


def initialize_parameters():
    tf.set_random_seed(1)
    W1 = tf.get_variable("W1", [3, 2], initializer=tf.contrib.layers.xavier_initializer(seed=1))

    b1 = tf.get_variable("b1", [3, 1], initializer=tf.zeros_initializer())

    W2 = tf.get_variable("W2", [2, 3], initializer=tf.contrib.layers.xavier_initializer(seed=1))

    b2 = tf.get_variable("b2", [2, 1], initializer=tf.zeros_initializer())

    W3 = tf.get_variable("W3", [1, 2], initializer=tf.contrib.layers.xavier_initializer(seed=1))

    b3 = tf.get_variable("b3", [1, 1], initializer=tf.zeros_initializer())

    parameters = {"W1": W1,
                  "b1": b1,
                  "W2": W2,
                  "b2": b2,
                  "W3": W3,
                  "b3": b3
                  }
    return parameters


def forward_propagation(X, parameters):
    W1 = parameters['W1']
    b1 = parameters['b1']
    W2 = parameters['W2']
    b2 = parameters['b2']
    W3 = parameters['W3']
    b3 = parameters['b3']

    Z1 = tf.add(tf.matmul(W1, X), b1)
    A1 = tf.nn.sigmoid(Z1)

    Z2 = tf.add(tf.matmul(W2, A1), b2)
    A2 = tf.nn.sigmoid(Z2)

    Z3 = tf.add(tf.matmul(W3, A2), b3)
    A3 = tf.nn.sigmoid(Z3)

    return A3


def compute_cost(Z3, Y):
    logits = tf.transpose(Z3)
    labels = tf.transpose(Y)
    cost = tf.reduce_mean(tf.nn.l2_loss(logits - labels))
    # cost = tf.reduce_mean(tf.nn.sigmoid_cross_entropy_with_logits(logits=logits, labels=labels))
    return cost


def model(X_train, Y_train, X_test, Y_test, learning_rate=0.001, num_epochs=3000, minibatch_size=16, print_cost=True):
    ops.reset_default_graph()

    tf.set_random_seed(1)
    seed = 3
    (n_x, m) = X_train.shape
    n_y = Y_train.shape[0]

    print(n_x, m, n_y)

    costs = []

    X, Y = create_placeholders(n_x, n_y)

    parameters = initialize_parameters()

    Z3 = forward_propagation(X, parameters)

    cost = compute_cost(Z3, Y)

    optimizer = tf.train.AdamOptimizer(learning_rate=learning_rate).minimize(cost)

    init = tf.global_variables_initializer()

    with tf.Session() as sess:
        sess.run(init)
        epoch_cost = 0.
        for epoch in range(num_epochs):
            # epoch_cost = 0.
            num_minibatches = int(m / minibatch_size)
            seed = seed + 1
            minibatches = random_mini_batches(X_train, Y_train, minibatch_size, seed)
            for minibatch in minibatches:
                (minibatch_X, minibatch_Y) = minibatch
                _, minibatch_cost = sess.run([optimizer, cost], feed_dict={X: minibatch_X, Y: minibatch_Y})
                epoch_cost += minibatch_cost / num_minibatches

            # _, minibatch_cost = sess.run([optimizer, cost], feed_dict={X: X_train, Y: Y_train})
            # epoch_cost = minibatch_cost

            if print_cost == True and epoch % 100 == 0:
                print("Cost after epoch %i: %f" % (epoch, epoch_cost))
            if print_cost == True and epoch % 5 == 0:
                costs.append(epoch_cost)

        plt.plot(np.squeeze(costs))
        plt.ylabel('cost')
        plt.xlabel('iterations (per tens)')
        plt.title("Learning rate =" + str(learning_rate))
        plt.show()

        parameters = sess.run(parameters)

        print ("Parameters have been trained!")

        # Calculate the correct predictions
        # correct_prediction = tf.equal(tf.argmax(Z3), tf.argmax(Y))
        correct_prediction = tf.equal(Z3 > 0.5, Y > 0.5)
        # Calculate accuracy on the test set
        accuracy = tf.reduce_mean(tf.cast(correct_prediction, "float"))
        print("Train Accuracy:", accuracy.eval({X: X_train, Y: Y_train}))
        print("Test Accuracy:", accuracy.eval({X: X_test, Y: Y_test}))
        return parameters


def random_mini_batches(X, Y, mini_batch_size=64, seed=0):
    """
    Creates a list of random minibatches from (X, Y)

    Arguments:
    X -- input data, of shape (input size, number of examples)
    Y -- true "label" vector (containing 0 if cat, 1 if non-cat), of shape (1, number of examples)
    mini_batch_size - size of the mini-batches, integer
    seed -- this is only for the purpose of grading, so that you're "random minibatches are the same as ours.

    Returns:
    mini_batches -- list of synchronous (mini_batch_X, mini_batch_Y)
    """

    m = X.shape[1]  # number of training examples
    mini_batches = []
    np.random.seed(seed)

    # Step 1: Shuffle (X, Y)
    permutation = list(np.random.permutation(m))
    shuffled_X = X[:, permutation]
    shuffled_Y = Y[:, permutation].reshape((Y.shape[0], m))

    # Step 2: Partition (shuffled_X, shuffled_Y). Minus the end case.
    num_complete_minibatches = int(math.floor(m / mini_batch_size))  # number of mini batches of size mini_batch_size in your partitionning
    for k in range(0, num_complete_minibatches):
        mini_batch_X = shuffled_X[:, k * mini_batch_size: k * mini_batch_size + mini_batch_size]
        mini_batch_Y = shuffled_Y[:, k * mini_batch_size: k * mini_batch_size + mini_batch_size]
        mini_batch = (mini_batch_X, mini_batch_Y)
        mini_batches.append(mini_batch)

    # Handling the end case (last mini-batch < mini_batch_size)
    if m % mini_batch_size != 0:
        mini_batch_X = shuffled_X[:, num_complete_minibatches * mini_batch_size: m]
        mini_batch_Y = shuffled_Y[:, num_complete_minibatches * mini_batch_size: m]
        mini_batch = (mini_batch_X, mini_batch_Y)
        mini_batches.append(mini_batch)

    return mini_batches


def prdeict(X, parameters):
    with tf.Session() as sess:
        z3 = sess.run(forward_propagation(X, parameters))
        return z3
        # return (z3 > 0.5) * 1.


X_train, Y_train, X_test, Y_test = create_datas(seed=1)
parameters = model(X_train, Y_train, X_test, Y_test)

X = [[0.3, 0.1, 0.6],
   [0.2, 0.8, 0.7]]
print(X)
print(prdeict(X, parameters))
