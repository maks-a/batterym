#!/usr/bin/python
import numpy as np
import matplotlib.pyplot as plt
import scipy.ndimage
from scipy.optimize import curve_fit
from scipy.interpolate import interp1d
import unittest


def duplicate_idxs(x, y):
    idxs = []
    n = len(y)
    i = -1
    while i < n:
        i += 1
        for j in xrange(i+1, n):
            if y[i] != y[j]:
                i = j-1
                break
            if (j-i) > 1:
                idxs.append(j-1)
                continue
    return idxs


def dilute(x, y):
    idxs = []
    n = len(x)
    for i in xrange(n):
        if i == 0 or i+1 == n or i%2!=0:
            continue
        idxs.append(i)
    return idxs


def steep(x, y, dx):
    idxs = []
    n = len(x)
    skip = False
    for i in xrange(2, n-1):
        j = i-1
        if skip:
            skip = False
            continue
        if abs(x[j] - x[i]) <= dx:
            k = j if x[j] < x[i] else i
            idxs.append(i)
            skip = True
    return idxs


def eliminate(x, y, index_extractor):
    idxs = index_extractor(x, y)
    for i in idxs:
        x[i] = None
        y[i] = None
    new_x = [j for j in x if j is not None]
    new_y = [j for j in y if j is not None]
    return new_x, new_y


def steps_filter(x, y):
    x, y = eliminate(x, y, duplicate_idxs)
    # dx = 10.0 / 60.0
    # x, y = eliminate(x, y, lambda x, y: steep(x, y, dx))
    # x, y = eliminate(x, y, dilute)
    return x, y


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


def run_test(filename):
    x, y = np.loadtxt(filename, skiprows=0).T

    x = list([-e for e in x])
    y = list(y)
    x.reverse()
    y.reverse()
    f = interp1d(x, y, kind='linear')

    dx = 1.0 / 60.0
    xmin = min(x)
    xmax = max(x)
    samps = int((xmax - xmin) / dx)
    x2 = np.linspace(xmin, xmax, samps)
    y2 = f(x2)
    y2 = running_mean(y2, 15)

    fig, ax = plt.subplots()

    ax.plot(x, y, 'x:', color='red')

    # x2, y2 = steps_filter(x, y)
    ax.plot(x2, y2, '-o', color='blue')

    # modes = ['reflect', 'constant', 'nearest', 'mirror', 'wrap']
    # ax.plot(x, scipy.ndimage.gaussian_filter(y, 5, mode=modes[2]), color='red')

    plt.show()


def main():
    folder = './test/chart/'
    run_test(folder + 'data1.txt')
    run_test(folder + 'data2.txt')
    run_test(folder + 'data3.txt')
    run_test(folder + 'data4.txt')
    run_test(folder + 'data5.txt')


class MyTest(unittest.TestCase):

    def test1(self):
        self.assertEqual(duplicate_idxs(None, []), [])
        self.assertEqual(duplicate_idxs(None, [1]), [])
        self.assertEqual(duplicate_idxs(None, [1, 1]), [])
        self.assertEqual(duplicate_idxs(None, [1, 1, 1]), [1])
        self.assertEqual(duplicate_idxs(None, [1, 1, 1, 2]), [1])
        self.assertEqual(duplicate_idxs(None, [1, 1, 1, 2, 2]), [1])
        self.assertEqual(duplicate_idxs(None, [1, 1, 1, 2, 2, 2]), [1, 4])


if __name__ == '__main__':
    main()
    #unittest.main()
