#!/usr/bin/python
import numpy as np
import matplotlib.pyplot as plt
import scipy.ndimage
from scipy.optimize import curve_fit
from scipy.interpolate import interp1d
import unittest


# def find_duplicate_idxs1(a):
#     result = []
#     n = len(a)
#     i = -1
#     while i < n:
#         i += 1
#         for j in xrange(i+1, n):
#             if a[i] == a[j]:
#                 continue
#             if j-i > 1:
#                 for k in xrange(i+1, j):
#                     result.append(k)
#             i = j-1
#             break
#     return result


# def find_duplicate_idxs(arr):
#     idxs = []
#     n = len(arr)
#     i = -1
#     while i < n:
#         i += 1
#         for j in xrange(i+1, n):
#             if arr[i] == arr[j] and j+1 < n:
#                 idxs.append(j)
#                 continue
#             i = j-1
#             break
#     return idxs


# def steps_filter2(x, y):
#     idxs = find_duplicate_idxs(y)
#     for i in idxs:
#         x[i] = y[i] = None
#     new_x = [j for j in x if j is not None]
#     new_y = [j for j in y if j is not None]
#     return new_x, new_y


def steps_filter(x, y):
    return x, y


def run_test(filename):
    x, y = np.loadtxt(filename, skiprows=0).T
    x = [-e for e in x]
    fig, ax = plt.subplots()

    ax.plot(x, y, '+:', color='#aaaaaa')

    x2, y2 = steps_filter(x, y)
    ax.plot(x2, y2, '-o', color='red')

    # modes = ['reflect', 'constant', 'nearest', 'mirror', 'wrap']
    # ax.plot(x, scipy.ndimage.gaussian_filter(y, 5, mode=modes[2]), color='red')

    plt.show()


def main():
    folder = './test/chart/'
    # run_test(folder + 'data1.txt')
    # run_test(folder + 'data2.txt')
    # run_test(folder + 'data3.txt')
    # run_test(folder + 'data4.txt')
    run_test(folder + 'data5.txt')


class MyTest(unittest.TestCase):

    def test1(self):
        self.assertEqual(find_duplicate_idxs([]), [])
        pass


if __name__ == '__main__':
    main()
    #unittest.main()
