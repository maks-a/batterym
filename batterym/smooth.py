#!/usr/bin/python
import numpy as np
import matplotlib.pyplot as plt
# import scipy.ndimage
# from scipy.optimize import curve_fit
# from scipy.interpolate import interp1d
import unittest


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


def scale_dif(y1, y2, k):
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
    y4 = scale_dif(y2, y3, 0.5)

    dx = 5.0 / 60.0
    x5 = linspace(xmin, xmax, dx)
    y5 = interpolate_linear(x2, y4, x5)
    y6 = interpolate_linear(x5, y5, x)
    if yn != len(y6):
        return x, y
    return x, y6


########################################################################
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

    def test_linspace(self):
        self.assertEqual(linspace(2, 5, 3), [2, 5])
        self.assertEqual(linspace(2, 5, 1.5), [2, 3.5, 5])
        self.assertEqual(linspace(2, 5, 1), [2, 3, 4, 5])
        self.assertEqual(linspace(2, 5, 4), [])


if __name__ == '__main__':
    # main()
    unittest.main()
