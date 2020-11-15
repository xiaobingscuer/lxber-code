#!/usr/bin/python
# coding=utf-8

"""
解不等式约束方程
"""

import copy
import math


def calc_fangcha(r=[]):
    mean = (sum(r)/len(r))
    ssum = 0
    for ri in r:
        ssum += (ri - mean) ** 2
    ssum /= len(r)
    return math.sqrt(ssum)


def calc_sum(r=[], c=[]):
    pass


def split(p=1):
    pass


class Solve:
    best_ret = []
    best_rc_sum = -1
    best_ret_var = 10000000
    best_ret_r_sum = -1

    rc = {}
    p = 0.1
    rmax = .6
    rmax_range = int(1/p) * 1
    rmax_hat = rmax_range * rmax

    c = [0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1]

    def get_best_ret_real(self):
        ret_real = []
        for ri in self.best_ret:
            ret_real.append(ri/self.rmax_range)
        return ret_real


def calc_main(c=[], rc_sum=0, depth=0, ret=[]):
    if depth >= len(c):
        if rc_sum >= Solve.best_rc_sum:
            if sum(ret) >= Solve.best_ret_r_sum:
                # if calc_fangcha(ret) <= Solve.best_ret_var:
                Solve.best_rc_sum = rc_sum
                Solve.best_ret = copy.copy(ret)

                Solve.best_ret_var = calc_fangcha(ret)
                Solve.best_ret_r_sum = sum(ret)
        return
    for ri in range(0, int(Solve.rmax_range) + 1):
        rc_sum_hat = rc_sum
        if len(ret) - 1 < depth:
            ret.append(ri)
        else:
            ret[depth] = ri
        # print(ri)
        rc_key = '{}-{}'.format(depth, ri)
        # print(rc_key)
        if rc_key in Solve.rc:
            rci = Solve.rc[rc_key]
        else:
            ci = c[depth]
            rci = ri * ci
            Solve.rc[rc_key] = rci

        if rc_sum_hat + rci > Solve.rmax_hat:
            break
        else:
            # rc_sum_hat += rci
            calc_main(c, rc_sum_hat + rci, depth+1, ret)

    print('bset ret is {}, best ret sum is {}'.format(Solve.best_ret, Solve.best_rc_sum))
    pass


if __name__ == '__main__':
    calc_main(Solve.c)

    print('bset ret is {}, best ret sum is {}'.format(Solve.get_best_ret_real(Solve), Solve.best_rc_sum/Solve.rmax_range))
    print(Solve.rc)
    pass


