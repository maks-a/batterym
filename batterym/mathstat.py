#!/usr/bin/python
import unittest


def is_zero(val, abs_tol=1e-3):
    return abs(val) < abs_tol


def is_within(a, lo, hi):
    return lo <= a and a <= hi


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

