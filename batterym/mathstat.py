#!/usr/bin/python
import unittest


def is_zero(val, abs_tol=1e-3):
    return abs(val) < abs_tol


def percentile(lst, factor):
    n = len(lst)
    if n < 1:
        return 0
    lst = sorted(lst)
    k = (n-1) * factor
    m = int(k)
    if m == k:
        return lst[m]
    t = (factor - 1.0 * m / (n-1)) * (n-1)
    return (1.0-t)*lst[m] + t*lst[m+1]


def median(lst):
    return percentile(lst, 0.5)


class MyTest(unittest.TestCase):

    def test_is_zero(self):
        self.assertEqual(is_zero(1e-7, abs_tol=1e-3), True)
        self.assertEqual(is_zero(1e-3, abs_tol=1e-7), False)

    def test_percentile(self):
        self.assertAlmostEqual(percentile([], 0), 0)
        self.assertAlmostEqual(percentile([], 0.3), 0)
        self.assertAlmostEqual(percentile([], 0.5), 0)
        self.assertAlmostEqual(percentile([], 0.7), 0)
        self.assertAlmostEqual(percentile([], 1.0), 0)

        self.assertAlmostEqual(percentile([1], 0), 1)
        self.assertAlmostEqual(percentile([1], 1.0/3), 1)
        self.assertAlmostEqual(percentile([1], 1.0/2), 1)
        self.assertAlmostEqual(percentile([1], 2.0/3), 1)
        self.assertAlmostEqual(percentile([1], 1.0), 1)

        self.assertAlmostEqual(percentile([1, 1, 1], 0), 1)
        self.assertAlmostEqual(percentile([1, 1, 1], 1.0/3), 1)
        self.assertAlmostEqual(percentile([1, 1, 1], 1.0/2), 1)
        self.assertAlmostEqual(percentile([1, 1, 1], 2.0/3), 1)
        self.assertAlmostEqual(percentile([1, 1, 1], 1.0), 1)

        self.assertAlmostEqual(percentile([1, 3], 0), 1)
        self.assertAlmostEqual(percentile([1, 3], 1.0/3), 1+2.0/3)
        self.assertAlmostEqual(percentile([1, 3], 1.0/2), 2)
        self.assertAlmostEqual(percentile([1, 3], 2.0/3), 1+2.0*2/3)
        self.assertAlmostEqual(percentile([1, 3], 1.0), 3)

        self.assertAlmostEqual(percentile([1, 2, 3, 4, 5, 6, 7], 0), 1)
        self.assertAlmostEqual(percentile([1, 2, 3, 4, 5, 6, 7], 1.0/3), 3)
        self.assertAlmostEqual(percentile([1, 2, 3, 4, 5, 6, 7], 1.0/2), 4)
        self.assertAlmostEqual(percentile([1, 2, 3, 4, 5, 6, 7], 2.0/3), 5)
        self.assertAlmostEqual(percentile([1, 2, 3, 4, 5, 6, 7], 1.0), 7)

        self.assertAlmostEqual(percentile([1, 3, 5, 7], 0), 1)
        self.assertAlmostEqual(percentile([1, 3, 5, 7], 1.0/3), 3)
        self.assertAlmostEqual(percentile([1, 3, 5, 7], 1.0/2), 4)
        self.assertAlmostEqual(percentile([1, 3, 5, 7], 2.0/3), 5)
        self.assertAlmostEqual(percentile([1, 3, 5, 7], 1.0), 7)

    def test_median(self):
        self.assertAlmostEqual(median([]), 0)
        self.assertAlmostEqual(median([1]), 1)
        self.assertAlmostEqual(median([1, 3]), 2)
        self.assertAlmostEqual(median([1, 3, 4]), 3)

