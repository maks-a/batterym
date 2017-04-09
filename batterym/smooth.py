#!/usr/bin/python
# import numpy as np
# import matplotlib.pyplot as plt
# import scipy.ndimage
# from scipy.optimize import curve_fit
# from scipy.interpolate import interp1d
import unittest


def is_within(a, lo, hi):
    return lo <= a and a <= hi


def interpolate_linear(x, y, new_x):
    n = len(x)
    new_n = len(new_x)
    if n < 2 or new_n < 1:
        return []
    if min(new_x) < min(x):
        raise ValueError('A value in x_new is below the interpolation')
    if max(x) < max(new_x):
        raise ValueError('A value in x_new is above the interpolation')
    new_y = [None] * new_n
    j = 0
    for i in xrange(1, n):
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


def interpolate_point(segment_start, segment_end, p):
    return (1.0 - p) * segment_start + p * segment_end


def linspace(lo, hi, step):
    sz = int((hi - lo) / step)
    if sz == 0:
        return []
    return [interpolate_point(lo, hi, 1.0*i/sz) for i in xrange(0, sz+1)]


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


def subtract(a, b):
    n = len(a)
    return [a[i]-b[i] for i in xrange(0, n)]


def scale(a, k):
    return [x*k for x in a]


def evaluate_array(y1, y2, k):
    d = subtract(y1, y2)
    d = scale(d, k)
    return subtract(y1, d)


def steps_filter(x, y):
    xn = len(x)
    yn = len(y)
    if xn < 3 or yn < 3:
        return x, y
    xmin = min(x)
    xmax = max(x)

    dx = 1.0 / 60.0
    x2 = linspace(xmin, xmax, dx)

    y2 = interpolate_linear(x, y, x2)
    y3 = tangent_filter(y2, 10)
    y4 = evaluate_array(y2, y3, 0.5)

    dx = 10.0 / 60.0
    x5 = linspace(xmin, xmax, dx)
    y5 = interpolate_linear(x2, y4, x5)
    y6 = interpolate_linear(x5, y5, x)
    if yn != len(y6):
        return x, y
    return x, y6


# def running_mean(l, N):
#     sum = 0
#     result = [0 for x in l]

#     k = len(l)
#     N = min(k, N)
#     for i in xrange(0, N):
#         sum += l[i]
#         result[i] = sum / (i+1)

#     for i in range(N, k):
#         sum = sum - l[i-N] + l[i]
#         result[i] = sum / N

#     return result


# def run_test(filename):
#     x, y = np.loadtxt(filename, skiprows=0).T
#     x = list([-e for e in x])
#     y = list(y)
#     x.reverse()
#     y.reverse()
#     x5, y5 = steps_filter(x, y)
#     y6 = scipy.ndimage.gaussian_filter(y, 5)
#     y7 = running_mean(y, 5)

#     fig, ax = plt.subplots()
#     line1, = ax.plot(x, y, 'x:', color='red', label='input')
#     line2, = ax.plot(x, y6, '-+', color='green', label='gaussian_filter')
#     line3, = ax.plot(x, y7, '-+', color='pink', label='running_mean')
#     line4, = ax.plot(x5, y5, '-o', color='blue', label='custom')

#     plt.legend(handles=[line1, line2, line3, line4])
#     mng = plt.get_current_fig_manager()
#     # mng.resize(*mng.window.maxsize())
#     plt.show()


# def main():
#     folder = './test/chart/'
#     run_test(folder + 'data1.txt')
#     run_test(folder + 'data2.txt')
#     run_test(folder + 'data3.txt')
#     run_test(folder + 'data4.txt')
#     run_test(folder + 'data5.txt')
#     run_test(folder + 'data6.txt')


class MyTest(unittest.TestCase):

    def test_interpolate_linear(self):
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
        self.assertEqual(interpolate_linear(
            [2, 8, 9], [1, 7, 8], [3, 4, 5]), [2, 3, 4])

        with self.assertRaises(ValueError):
            interpolate_linear([3, 4], [6], [1])

        with self.assertRaises(ValueError):
            interpolate_linear([3, 4], [6], [7])

    def test_linspace(self):
        self.assertEqual(linspace(2, 5, 3), [2, 5])
        self.assertEqual(linspace(2, 5, 1.5), [2, 3.5, 5])
        self.assertEqual(linspace(2, 5, 1), [2, 3, 4, 5])
        self.assertEqual(linspace(2, 5, 4), [])

    def test_tangent_filter(self):
        self.assertEqual(tangent_filter([], 1), [])
        self.assertEqual(tangent_filter([5], 1), [5])
        self.assertEqual(tangent_filter([1, 3, 3], 1), [1, 3, 3])
        self.assertEqual(tangent_filter([1, 3, 3], 3), [1, 2, 3])
        self.assertEqual(tangent_filter([1, 1, 3], 3), [1, 2, 3])

    def test_subtract(self):
        self.assertEqual(subtract([], []), [])
        self.assertEqual(subtract([1], [1]), [0])
        self.assertEqual(subtract([5, 6, 7], [1, 2, 3]), [4, 4, 4])

    def test_scale(self):
        self.assertEqual(scale([], 0), [])
        self.assertEqual(scale([], 1), [])
        self.assertEqual(scale([2], 1), [2])
        self.assertEqual(scale([2], 0), [0])
        self.assertEqual(scale([1, 2, 3], 2), [2, 4, 6])

    def test_evaluate_array(self):
        self.assertEqual(evaluate_array([], [], 1), [])
        self.assertEqual(evaluate_array([5, 6, 7], [1, 2, 3], 0), [5, 6, 7])
        self.assertEqual(evaluate_array([5, 6, 7], [1, 2, 3], 0.5), [3, 4, 5])
        self.assertEqual(evaluate_array([5, 6, 7], [1, 2, 3], 1), [1, 2, 3])

    def test_steps_filter(self):
        self.assertEqual(steps_filter([], []), ([], []))
        self.assertEqual(steps_filter([1], [2]), ([1], [2]))
        self.assertEqual(steps_filter([1, 5], [2, 7]), ([1, 5], [2, 7]))
        self.assertEqual(steps_filter(
            [1, 2, 3], [1, 2, 3]), ([1, 2, 3], [1, 2, 3]))


# if __name__ == '__main__':
#     # main()
#     unittest.main()
