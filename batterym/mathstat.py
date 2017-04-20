#!/usr/bin/python
import unittest


def is_zero(val, abs_tol=1e-3):
    return abs(val) < abs_tol


def percentile(lst, factor):
    n = len(lst)
    if n < 1:
        return 0
    lst = sorted(lst)
    m = int(n*factor)
    if n % 2 == 1:
        return lst[m]
    return (lst[m-1] + lst[m])/2


def median(lst):
    return percentile(lst, 0.5)


class MyTest(unittest.TestCase):

    def test_median(self):
        self.assertEqual(median([]), 0)
        self.assertEqual(median([1]), 1)
        self.assertEqual(median([1, 3]), 2)
        self.assertEqual(median([1, 3, 4]), 3)

    def test_is_zero(self):
        self.assertEqual(is_zero(1e-7, abs_tol=1e-3), True)
        self.assertEqual(is_zero(1e-3, abs_tol=1e-7), False)
