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


def is_ascending_order(arr):
    for i in range(1, len(arr)):
        if arr[i-1] > arr[i]:
            return False
    return True


def is_descending_order(arr):
    for i in range(1, len(arr)):
        if arr[i-1] < arr[i]:
            return False
    return True


def interpolate_linear(x, y, new_x):
    n = len(x)
    new_n = len(new_x)
    if n < 2 or new_n < 1:
        return []
    if min(new_x) < min(x):
        raise ValueError('A value in x_new is below the interpolation')
    if max(x) < max(new_x):
        raise ValueError('A value in x_new is above the interpolation')
    is_ascending = is_ascending_order(x)
    if not is_ascending and not is_descending_order(x):
        raise ValueError('Input x-array must be ascending or desceding')
    if not is_ascending:
        x = list(reversed(x))
        y = list(reversed(y))
    new_y = [None] * new_n
    j = 0
    for i in range(1, n):
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


def interpolate_linear_evenly(x, y, n=None, dx=None):
    nx = len(x)
    ny = len(y)
    if nx != ny:
        raise ValueError('Arguments x, y must have same size')
    if nx < 2:
        return x, y
    if n is None and dx is None:
        raise ValueError('Bad arguments: n, dx')
    if n is not None and n < 2:
        raise ValueError('Bad argument: n must be more than 1')
    lo, hi = x[0], x[-1]
    if dx is not None and (hi-lo) < 0:
        dx *= -1
    if n is not None and dx is None:
        dx = float(hi - lo) / (n - 1)
    if abs(hi-lo) < abs(dx):
        dx = hi - lo
    new_x = linspace(lo, hi, dx)
    new_y = interpolate_linear(x, y, new_x)
    if len(new_x) != len(new_y):
        raise ValueError('ouch!')
    return new_x, new_y


def interpolate_point(segment_start, segment_end, p):
    return (1.0 - p) * segment_start + p * segment_end


def linspace(lo, hi, step):
    sz = int((hi - lo) / step)
    if sz == 0:
        return []
    return [interpolate_point(lo, hi, 1.0*i/sz) for i in range(0, sz+1)]


def round_pattern(val, pattern):
    tol = 1
    for key in sorted(pattern.keys(), reverse=True):
        if key <= val:
            tol = pattern[key]
            break
    result = val - val % tol
    return result


class MyTest(unittest.TestCase):

    def test_round_pattern(self):
        pattern = {100: 5}
        self.assertEqual(round_pattern(-10, pattern), -10)
        self.assertEqual(round_pattern(0, pattern), 0)
        self.assertEqual(round_pattern(15, pattern), 15)
        self.assertEqual(round_pattern(100, pattern), 100)
        self.assertEqual(round_pattern(101, pattern), 100)
        self.assertEqual(round_pattern(102, pattern), 100)
        self.assertEqual(round_pattern(103, pattern), 100)
        self.assertEqual(round_pattern(104, pattern), 100)
        self.assertEqual(round_pattern(105, pattern), 105)
        self.assertEqual(round_pattern(106, pattern), 105)

        pattern = {100: 5, 0: 2}
        self.assertEqual(round_pattern(15, pattern), 14)
        self.assertEqual(round_pattern(100, pattern), 100)
        self.assertEqual(round_pattern(101, pattern), 100)
        self.assertEqual(round_pattern(102, pattern), 100)
        self.assertEqual(round_pattern(103, pattern), 100)
        self.assertEqual(round_pattern(104, pattern), 100)
        self.assertEqual(round_pattern(105, pattern), 105)
        self.assertEqual(round_pattern(106, pattern), 105)

        pattern = {0: 4, 100: 5}
        self.assertEqual(round_pattern(15, pattern), 12)
        self.assertEqual(round_pattern(100, pattern), 100)
        self.assertEqual(round_pattern(101, pattern), 100)
        self.assertEqual(round_pattern(102, pattern), 100)
        self.assertEqual(round_pattern(103, pattern), 100)
        self.assertEqual(round_pattern(104, pattern), 100)
        self.assertEqual(round_pattern(105, pattern), 105)
        self.assertEqual(round_pattern(106, pattern), 105)

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

    def test_linspace(self):
        self.assertEqual(linspace(2, 5, 3), [2, 5])
        self.assertEqual(linspace(2, 5, 1.5), [2, 3.5, 5])
        self.assertEqual(linspace(2, 5, 1), [2, 3, 4, 5])
        self.assertEqual(linspace(2, 5, 4), [])

        self.assertEqual(linspace(5, 2, -3), [5, 2])
        self.assertEqual(linspace(5, 2, -1.5), [5, 3.5, 2])
        self.assertEqual(linspace(5, 2, -1), [5, 4.000000000000001, 3, 2])
        self.assertEqual(linspace(5, 2, -4), [])

        self.assertEqual(linspace(4, 2, -2), [4, 2])

    def test_is_ascending_order(self):
        self.assertAlmostEqual(is_ascending_order([]), True)
        self.assertAlmostEqual(is_ascending_order([1]), True)
        self.assertAlmostEqual(is_ascending_order([1, 1]), True)
        self.assertAlmostEqual(is_ascending_order([1, 2]), True)
        self.assertAlmostEqual(is_ascending_order([3, 2]), False)

    def test_is_descending_order(self):
        self.assertAlmostEqual(is_descending_order([]), True)
        self.assertAlmostEqual(is_descending_order([1]), True)
        self.assertAlmostEqual(is_descending_order([1, 1]), True)
        self.assertAlmostEqual(is_descending_order([2, 1]), True)
        self.assertAlmostEqual(is_descending_order([2, 3]), False)

    def test_interpolate_linear(self):
        with self.assertRaises(ValueError):
            interpolate_linear([3, 4], [6], [1])

        with self.assertRaises(ValueError):
            interpolate_linear([3, 4], [6], [7])

        with self.assertRaises(ValueError):
            interpolate_linear([3, 5, 4], [1, 2, 3], [4])

        self.assertEqual(interpolate_linear([4, 2], [2, 5], []), [])
        self.assertEqual(interpolate_linear([4, 2], [2, 5], [3]), [3.5])
        self.assertEqual(interpolate_linear([4, 2], [5, 2], [4, 2]), [5, 2])
        self.assertEqual(interpolate_linear(
            [4, 2], [2, 5], [2, 3, 4]), [5, 3.5, 2])
        self.assertEqual(interpolate_linear(
            [-8, -10], [10, 20], [-9]), [15])
        self.assertEqual(interpolate_linear(
            [2, 4, 6], [3, 6, 9], [3, 4, 5]), [4.5, 6, 7.5])
        self.assertEqual(interpolate_linear(
            [6, 4, 2], [3, 6, 9], [3, 4, 5]), [7.5, 6, 4.5])

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

    def test_interpolate_linear_evenly(self):
        with self.assertRaises(ValueError):
            interpolate_linear_evenly([1, 2], [1, 2, 3], n=2)

        with self.assertRaises(ValueError):
            interpolate_linear_evenly([1, 2], [1, 2])

        with self.assertRaises(ValueError):
            interpolate_linear_evenly([1, 2], [1, 2], n=1)

        x, y = [1], [1]

        result = interpolate_linear_evenly(x, y, n=2)
        expected = [1], [1]
        self.assertEqual(result, expected)

        x, y = [2, 4], [2, 5]

        result = interpolate_linear_evenly(x, y, n=2)
        expected = [2, 4], [2, 5]
        self.assertEqual(result, expected)

        result = interpolate_linear_evenly(x, y, n=3)
        expected = [2, 3, 4], [2, 3.5, 5]
        self.assertEqual(result, expected)

        result = interpolate_linear_evenly(x, y, dx=30)
        expected = [2, 4], [2, 5]
        self.assertEqual(result, expected)

        result = interpolate_linear_evenly(x, y, dx=2)
        expected = [2, 4], [2, 5]
        self.assertEqual(result, expected)

        result = interpolate_linear_evenly(x, y, dx=1)
        expected = [2, 3, 4], [2, 3.5, 5]
        self.assertEqual(result, expected)

        x, y = [2, 4], [5, 2]

        result = interpolate_linear_evenly(x, y, n=2)
        expected = [2, 4], [5, 2]
        self.assertEqual(result, expected)

        result = interpolate_linear_evenly(x, y, n=3)
        expected = [2, 3, 4], [5, 3.5, 2]
        self.assertEqual(result, expected)

        result = interpolate_linear_evenly(x, y, dx=30)
        expected = [2, 4], [5, 2]
        self.assertEqual(result, expected)

        result = interpolate_linear_evenly(x, y, dx=2)
        expected = [2, 4], [5, 2]
        self.assertEqual(result, expected)

        result = interpolate_linear_evenly(x, y, dx=1)
        expected = [2, 3, 4], [5, 3.5, 2]
        self.assertEqual(result, expected)

        x, y = [4, 2], [5, 2]

        result = interpolate_linear_evenly(x, y, n=2)
        expected = [4, 2], [5, 2]
        self.assertEqual(result, expected)

        result = interpolate_linear_evenly(x, y, n=3)
        expected = [4, 3, 2], [5, 3.5, 2]
        self.assertEqual(result, expected)

        result = interpolate_linear_evenly(x, y, dx=30)
        expected = [4, 2], [5, 2]
        self.assertEqual(result, expected)

        result = interpolate_linear_evenly(x, y, dx=2)
        expected = [4, 2], [5, 2]
        self.assertEqual(result, expected)

        result = interpolate_linear_evenly(x, y, dx=1)
        expected = [4, 3, 2], [5, 3.5, 2]
        self.assertEqual(result, expected)
