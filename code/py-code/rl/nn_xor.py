#!/usr/bin/python
# coding=utf-8

__doc__ = """
tensorflow 搭建神经网络学习异或函数(xor)
"""

import numpy as np
import matplotlib.pyplot as plt
import math
import json

import tensorflow as tf
from tensorflow.python.framework import ops

# plt.ion()


# create train data set
def create_datas(seed=1, train_num=120, test_num=30):
    np.random.seed(seed)
    X_train = np.random.rand(2, train_num).astype(np.float32)
    Y_train = np.round(X_train)
    Y_train = np.array([(Y_train[0, :] != Y_train[1, :]) * 1.0])

    print("X_train.shape", X_train.shape)
    print("Y_train.shape", Y_train.shape)

    plot_data_set(X_train, Y_train, 'train datas')

    # create test data set
    np.random.seed(seed*1024)
    X_test = np.random.rand(2, test_num).astype(np.float32)
    Y_test = np.round(X_test)
    Y_test = np.array([(Y_test[0, :] != Y_test[1, :]) * 1.0])

    print("X_test.shape", X_test.shape)
    print("Y_test.shape", Y_test.shape)

    plot_data_set(X_test, Y_test, 'test datas')

    return X_train, Y_train, X_test, Y_test

def plot_data_set(X, Y, title):
    X_t = X.transpose()
    is_x0 = (Y[0] == 0.)
    is_x1 = (Y[0] == 1.)
    X_0, X_1 = X_t[is_x0], X_t[is_x1]

    fig, axs = plt.subplots(1, 1)
    axs.plot([0., 1.], [0.5, 0.5], color='black')
    axs.plot([.5, .5], [0., 1.], color='black')
    axs.scatter(X_0[:, 0], X_0[:, 1], label='0', alpha=0.6, color='b')
    axs.scatter(X_1[:, 0], X_1[:, 1], label='1', alpha=0.6, color='r')
    axs.set(title=title)
    axs.legend()
    # plt.show()
    pass

def create_placeholders(n_x, n_y):
    X = tf.placeholder(tf.float32, [n_x, None], name='X')
    Y = tf.placeholder(tf.float32, [n_y, None], name='Y')
    return X, Y


def initialize_parameters():
    tf.set_random_seed(1)
    W1 = tf.get_variable("W1", [2, 2], initializer=tf.contrib.layers.xavier_initializer(seed=1))
    b1 = tf.get_variable("b1", [2, 1], initializer=tf.zeros_initializer())

    W2 = tf.get_variable("W2", [3, 2], initializer=tf.contrib.layers.xavier_initializer(seed=1))
    b2 = tf.get_variable("b2", [3, 1], initializer=tf.zeros_initializer())

    W3 = tf.get_variable("W3", [1, 3], initializer=tf.contrib.layers.xavier_initializer(seed=1))
    b3 = tf.get_variable("b3", [1, 1], initializer=tf.zeros_initializer())

    parameters = {"W1": W1,
                  "b1": b1,
                  "W2": W2,
                  "b2": b2,
                  "W3": W3,
                  "b3": b3
                  }
    return parameters


def add_layer(layer_name, inputs, node_size, in_size, activation_func=None, parameters={}):
    with tf.name_scope(layer_name):
        # Weights = tf.get_variable(layer_name+"_W", [node_size, in_size], initializer=tf.contrib.layers.xavier_initializer(seed=1))
        # biases = tf.get_variable(layer_name+"_b", [node_size, 1], initializer=tf.zeros_initializer())
        with tf.name_scope("Weights"):
            Weights = tf.Variable(tf.random_normal([node_size, in_size], seed=1))

        with tf.name_scope("biases"):
            biases = tf.Variable(tf.zeros([node_size, 1]))

        with tf.name_scope("outputs"):
            Z = tf.add(tf.matmul(Weights, inputs), biases)
            if activation_func is None:
                outputs = Z
            else:
                outputs = activation_func(Z)

        parameters.update({layer_name + "_W": Weights})
        parameters.update({layer_name + "_b": biases})

        tf.summary.histogram(layer_name+"/Weights", Weights)
        tf.summary.histogram(layer_name+"/biases", biases)
        tf.summary.histogram(layer_name+"/outputs", outputs)
        return outputs


def forward_propagation_layers(inputs, input_size, node_sizes, activation_funcs, parameters, layer_count=0):
    if len(node_sizes) == 0:
        return inputs
    outputs = add_layer("layer%s"%layer_count, inputs, node_sizes[0], input_size, activation_funcs[0], parameters)
    return forward_propagation_layers(outputs, node_sizes[0], node_sizes[1:], activation_funcs[1:], parameters, layer_count+1)


def predict_a_layer(layer_name, inputs, weights, biases, activation_func=None):
    with tf.name_scope(layer_name):
        with tf.name_scope("predict"):
            Z = tf.add(tf.matmul(weights, inputs), biases)
            if activation_func is None:
                outputs = Z
            else:
                outputs = activation_func(Z)
            return outputs


def predict_layers(inputs, parameters, params_activation_func, layer_count=0):
    layers = len(params_activation_func)
    if layers == layer_count:
        return inputs
    layer_name = "layer%s"%layer_count
    weights = parameters[layer_name + "_W"]
    biases = parameters[layer_name + "_b"]
    actfunc = params_activation_func[layer_count]
    outputs = predict_a_layer(layer_name, inputs, weights, biases, actfunc)
    return predict_layers(outputs, parameters, params_activation_func, layer_count+1)


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

    tf.summary.histogram("W1", W1)
    tf.summary.histogram("W2", W2)
    tf.summary.histogram("W3", W3)

    tf.summary.histogram("b1", b1)
    tf.summary.histogram("b2", b2)
    tf.summary.histogram("b3", b3)

    tf.summary.histogram("A1", A1)
    tf.summary.histogram("A2", A2)
    tf.summary.histogram("A3", A3)

    return A3


def compute_cost(Y_hat, Y):
    Y_hat = tf.transpose(Y_hat)
    Y = tf.transpose(Y)
    cost = tf.reduce_mean(tf.reduce_sum(tf.square(Y_hat - Y)))
    tf.summary.scalar("loss", cost)
    return cost


def model(X_train, Y_train, X_test, Y_test, learning_rate=0.001, num_epochs=5000, minibatch_size=20, print_cost=True):
    # ops.reset_default_graph()

    tf.set_random_seed(1)
    seed = 3
    (n_x, m) = X_train.shape
    n_y = Y_train.shape[0]

    print(n_x, m, n_y)

    costs = []
    with tf.name_scope('inputs'):
        X, Y = create_placeholders(n_x, n_y)

    with tf.name_scope('parameters'):
        # parameters = initialize_parameters()
        parameters = {}
        nodes = [4, 2, 1]
        params_activation_func = [tf.nn.sigmoid] * len(nodes)

    with tf.name_scope('forward_propagation'):
        # Y_hat = forward_propagation(X, parameters)
        Y_hat = forward_propagation_layers(X, n_x, nodes, params_activation_func, parameters, 0)

    with tf.name_scope('loss'):
        cost = compute_cost(Y_hat, Y)

    with tf.name_scope('train'):
        optimizer = tf.train.AdamOptimizer(learning_rate=learning_rate).minimize(cost)

    merged = tf.summary.merge_all()

    init = tf.global_variables_initializer()

    with tf.Session() as sess:
        writer = tf.summary.FileWriter("D:\\lxb\\imgs\\RL_img\\nn_xor\\logs", sess.graph)

        sess.run(init)
        # epoch_cost = 0.
        for epoch in range(num_epochs):
            epoch_cost = 0.
            num_minibatches = int(m / minibatch_size)
            seed = seed + 1
            minibatches = random_mini_batches(X_train, Y_train, minibatch_size, seed)
            for minibatch in minibatches:
                (minibatch_X, minibatch_Y) = minibatch
                _, minibatch_cost = sess.run([optimizer, cost], feed_dict={X: minibatch_X, Y: minibatch_Y})
                epoch_cost += minibatch_cost / num_minibatches

            if print_cost == True and epoch % 100 == 0:
                print("Cost after epoch %i: %f" % (epoch, epoch_cost))
            if print_cost == True and epoch % 5 == 0:
                costs.append(epoch_cost)
                result = sess.run(merged, feed_dict={X: minibatch_X, Y: minibatch_Y})
                writer.add_summary(result, epoch)

        figs, axss = plt.subplots(1, 1)
        plt.plot(np.squeeze(costs))
        plt.ylabel('cost')
        plt.xlabel('iterations (per tens)')
        plt.title("Learning rate =" + str(learning_rate))
        # plt.show()

        # parameters = sess.run(parameters)

        print("Parameters have been trained!")

        # Calculate the correct predictions
        correct_prediction = tf.equal(Y_hat > 0.5, Y > 0.5)
        # Calculate accuracy on the test set
        accuracy = tf.reduce_mean(tf.cast(correct_prediction, "float"))
        print("Train Accuracy:", accuracy.eval({X: X_train, Y: Y_train}))
        print("Test Accuracy:", accuracy.eval({X: X_test, Y: Y_test}))
        return parameters, params_activation_func


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
        Y_hat = sess.run(forward_propagation(X, parameters))
        return Y_hat
        # return (Y_hat > 0.5) * 1.


def predict_nn(inputs, parameters, params_activation_func):
    with tf.Session() as sess:
        with tf.name_scope('predict_layers'):
            Y_hat = sess.run(predict_layers(inputs, parameters, params_activation_func))
            return Y_hat
        # return (Y_hat > 0.5) * 1.

# 启动
X_train, Y_train, X_test, Y_test = create_datas(seed=1, train_num=20, test_num=10)
# parameters = model(X_train, Y_train, X_test, Y_test)
parameters, params_activation_func = model(X_train, Y_train, X_test, Y_test)

# 将网络参数保存到文件
with open('nn_parameters.txt', 'wb+') as fs:
    pass

# 可视化在测试集上的表现
Y_test_hat = predict_nn(X_test, parameters, params_activation_func)
Y_test_hat = (np.array(Y_test_hat) > 0.5) * 1
plot_data_set(X_test, Y_test_hat, 'predict test datas')

# 预测未在训练集合测试集上的数据
X = [[0.3, 0.1, 0.6, 0.4999999999999999],
     [0.2, 0.8, 0.7, 0.5000000000000001]]
print(X)
# print(prdeict(X, parameters))
print((predict_nn(X, parameters, params_activation_func) > 0.5) * 1)

#
plt.show()
