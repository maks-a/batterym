#!/usr/bin/python
import numpy as np
import matplotlib.pyplot as plt
# import scipy.ndimage
# from scipy.optimize import curve_fit
# from scipy.interpolate import interp1d
import unittest


# def duplicate_idxs(x, y):
#     idxs = []
#     n = len(y)
#     i = -1
#     while i < n:
#         i += 1
#         for j in xrange(i+1, n):
#             if y[i] != y[j]:
#                 i = j-1
#                 break
#             if (j-i) > 1:
#                 idxs.append(j-1)
#                 continue
#     return idxs


# def dilute(x, y):
#     idxs = []
#     n = len(x)
#     for i in xrange(n):
#         if i == 0 or i+1 == n or i % 2 != 0:
#             continue
#         idxs.append(i)
#     return idxs


# def steep(x, y, dx):
#     idxs = []
#     n = len(x)
#     skip = False
#     for i in xrange(2, n-1):
#         j = i-1
#         if skip:
#             skip = False
#             continue
#         if abs(x[j] - x[i]) <= dx:
#             k = j if x[j] < x[i] else i
#             idxs.append(i)
#             skip = True
#     return idxs


# def eliminate(x, y, index_extractor):
#     idxs = index_extractor(x, y)
#     for i in idxs:
#         x[i] = None
#         y[i] = None
#     new_x = [j for j in x if j is not None]
#     new_y = [j for j in y if j is not None]
#     return new_x, new_y


# def steps_filter1(x, y):
#     x, y = eliminate(x, y, duplicate_idxs)
#     # dx = 10.0 / 60.0
#     # x, y = eliminate(x, y, lambda x, y: steep(x, y, dx))
#     # x, y = eliminate(x, y, dilute)
#     return x, y


def running_mean(l, N):
    sum = 0
    result = [0 for x in l]

    k = len(l)
    N = min(k, N)
    for i in xrange(0, N):
        sum += l[i]
        result[i] = sum / (i+1)

    for i in range(N, k):
        sum = sum - l[i-N] + l[i]
        result[i] = sum / N

    return result


def is_within(a, lo, hi):
    return lo <= a and a <= hi


def interpolate_linear(x, y, new_x):
    n = len(x)
    if n < 2:
        return []
    new_n = len(new_x)
    new_y = [None] * new_n
    j = 0
    for i in xrange(1, n):
        while j < new_n and new_x[j] < x[i-1]:
            j += 1
        if j >= new_n:
            break
        dx = x[i] - x[i-1]
        dy = y[i] - y[i-1]
        if dx == 0:
            w = 0
        else:
            w = 1.0 * dy / dx
        while j < new_n and is_within(new_x[j], x[i-1], x[i]):
            dxx = new_x[j] - x[i-1]
            dyy = w * dxx
            new_y[j] = y[i-1] + dyy
            j += 1
    return new_y


def linspace(lo, hi, step):
    sz = int((hi - lo) / step)
    step = 1.0 * (hi-lo) / sz
    return [lo+i*step for i in xrange(0, sz+1)]


def tangent_filter(a, w):
    n = len(a)
    k = int((w-1) / 2)
    result = [0 for x in a]
    for i in xrange(0, n):
        l = max(0, i-k)
        r = min(n-1, i+k)
        d = min(i-l, r-i)
        result[i] = float(a[i-d] + a[i+d]) / 2.0
    return result


def sub(a, b):
    n = len(a)
    return [a[i]-b[i] for i in xrange(0, n)]


def scale(a, k):
    return [x*k for x in a]


def normalize(a):
    mx = max(a)
    mn = min(a)
    d = mx-mn
    return [(2.0*(x-mn)-d)/d for x in a]


def scale_dif(y1, y2, k):
    d = sub(y1, y2)
    d = scale(d, k)
    return sub(y1, d)


def steps_filter(x, y):
    xmin = min(x)
    xmax = max(x)

    dx = 1.0 / 60.0
    x2 = linspace(xmin, xmax, dx)

    y2 = interpolate_linear(x, y, x2)
    y3 = tangent_filter(y2, 10)
    y4 = scale_dif(y2, y3, 0.5)

    dx = 5.0 / 60.0
    x5 = linspace(xmin, xmax, dx)
    y5 = interpolate_linear(x2, y4, x5)
    return x5, y5


def run_test2(filename):
    x, y = np.loadtxt(filename, skiprows=0).T

    x = list([-e for e in x])
    y = list(y)
    x.reverse()
    y.reverse()

    xmin = min(x)
    xmax = max(x)
    dx = 1.0 / 60.0
    samps = int((xmax - xmin) / dx)
    #x2 = np.linspace(xmin, xmax, samps)
    #f = interp1d(x, y, kind='linear')
    #y2 = f(x2)
    x2 = linspace(xmin, xmax, samps)
    y2 = interpolate_linear(x, y, x2)
    #y2 = running_mean(y2, 3)

    y3 = tangent_filter(y2, 10)
    y4 = scale_dif(y2, y3, 0.5)

    dx = 5.0 / 60.0
    samps = int((xmax - xmin) / dx)
    x5 = linspace(xmin, xmax, samps)
    y5 = interpolate_linear(x2, y4, x5)

    fig, ax = plt.subplots()

    ax.plot(x, y, 'x:', color='red')

    # x2, y2 = steps_filter(x, y)
    # ax.plot(x2, y2, '-x', color='green')

    # ax.plot(x2, y3, '-x', color='grey')
    #ax.plot(x2, y4, '-+', color='grey')
    ax.plot(x5, y5, '-o', color='blue')

    # modes = ['reflect', 'constant', 'nearest', 'mirror', 'wrap']
    # ax.plot(x, scipy.ndimage.gaussian_filter(y, 5, mode=modes[2]), color='red')

    mng = plt.get_current_fig_manager()
    mng.resize(*mng.window.maxsize())
    plt.show()


def run_test(filename):
    x, y = np.loadtxt(filename, skiprows=0).T
    x = list([-e for e in x])
    y = list(y)
    x.reverse()
    y.reverse()
    x5, y5 = steps_filter(x, y)

    fig, ax = plt.subplots()
    ax.plot(x, y, 'x:', color='red')
    ax.plot(x5, y5, '-o', color='blue')
    mng = plt.get_current_fig_manager()
    mng.resize(*mng.window.maxsize())
    plt.show()


def main():
    folder = './test/chart/'
    run_test(folder + 'data1.txt')
    run_test(folder + 'data2.txt')
    run_test(folder + 'data3.txt')
    run_test(folder + 'data4.txt')
    run_test(folder + 'data5.txt')


class MyTest(unittest.TestCase):

    # def test_duplicate_idxs(self):
    #     self.assertEqual(duplicate_idxs(None, []), [])
    #     self.assertEqual(duplicate_idxs(None, [1]), [])
    #     self.assertEqual(duplicate_idxs(None, [1, 1]), [])
    #     self.assertEqual(duplicate_idxs(None, [1, 1, 1]), [1])
    #     self.assertEqual(duplicate_idxs(None, [1, 1, 1, 2]), [1])
    #     self.assertEqual(duplicate_idxs(None, [1, 1, 1, 2, 2]), [1])
    #     self.assertEqual(duplicate_idxs(None, [1, 1, 1, 2, 2, 2]), [1, 4])

    def test_interpolate(self):
        self.assertEqual(interpolate_linear([2, 4], [2, 5], []), [])
        self.assertEqual(interpolate_linear([2, 4], [2, 5], [3]), [3.5])
        self.assertEqual(interpolate_linear(
            [2, 4], [2, 5], [2, 3, 4]), [2, 3.5, 5])
        self.assertEqual(interpolate_linear([2, 2], [5, 5], []), [])
        self.assertEqual(interpolate_linear([2, 2], [5, 5], [2]), [5])
        self.assertEqual(interpolate_linear([2, 2], [2, 5], [2]), [2])
        self.assertEqual(interpolate_linear([1], [2], []), [])
        self.assertEqual(interpolate_linear([1], [2], [3]), [])
        self.assertEqual(interpolate_linear([1], [2], [3, 4]), [])
        self.assertEqual(interpolate_linear([-10, -8], [10, 20], [-9]), [15])


if __name__ == '__main__':
    main()
    unittest.main()
