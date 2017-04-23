#!/usr/bin/python
import mathstat
import unittest

# statistic model
# - split charge/discharge
# - extract slopes by capacity bins
# - pick up slopes curve (by percentile)
# - reconstruct (dis)charging capacity timeline (start value)


def get_slopes_capacity_bins(data):
    bins = {}
    for e in data:
        key = e.get('capacity_round')
        val = e.get('slope', 0)
        if key is not None and not mathstat.is_zero(val):
            bins.setdefault(key, []).append(val)
    return bins


def get_slopes_by_percentile(bins, percentile_val):
    x = bins.keys()
    y = [mathstat.percentile(bins[i], percentile_val) for i in x]
    return dict(zip(x, y))


def reconstruct_timeline(slopes):
    capacity = slopes.keys()
    slope = slopes.values()
    n = len(slopes)
    if n < 2:
        return []
    t = [0]
    for i in xrange(1, n):
        dy = 1.0 * (capacity[i] - capacity[i-1])
        slope = slopes[capacity[i-1]]
        dx = dy / slope
        x = t[-1] + dx
        t.append(x)
    return zip(t, capacity)


class MyTest(unittest.TestCase):

    def test_get_slopes_capacity_bins(self):
        src = []
        expected = {}
        result = get_slopes_capacity_bins(src)
        self.assertEqual(result, expected)

        src = [
            {'capacity_round': 82, 'slope': 1},
            {'capacity_round': 83, 'slope': 2},
        ]
        expected = {
            82: [1],
            83: [2],
        }
        result = get_slopes_capacity_bins(src)
        self.assertEqual(result, expected)

        src = [
            {'capacity_round': 82, 'slope': 1},
            {'capacity_round': 82, 'slope': 2},
        ]
        expected = {
            82: [1, 2],
        }
        result = get_slopes_capacity_bins(src)
        self.assertEqual(result, expected)

    def test_get_slopes_by_percentile(self):
        src = {82: [1, 3, 5, 7]}
        expected = {82: 1}
        result = get_slopes_by_percentile(src, 0)
        self.assertEqual(result, expected)

        src = {82: [1, 3, 5, 7]}
        expected = {82: 3}
        result = get_slopes_by_percentile(src, 1.0/3)
        self.assertEqual(result, expected)

        src = {82: [1, 3, 5, 7]}
        expected = {82: 4}
        result = get_slopes_by_percentile(src, 0.5)
        self.assertEqual(result, expected)

        src = {82: [1, 3, 5, 7]}
        expected = {82: 5}
        result = get_slopes_by_percentile(src, 2.0/3)
        self.assertEqual(result, expected)

        src = {82: [1, 3, 5, 7]}
        expected = {82: 7}
        result = get_slopes_by_percentile(src, 1.0)
        self.assertEqual(result, expected)

    def test_reconstruct_timeline(self):
        src = {}
        expected = []
        result = reconstruct_timeline(src)
        self.assertEqual(result, expected)

        src = {82: 2}
        expected = []
        result = reconstruct_timeline(src)
        self.assertEqual(result, expected)

        src = {82: 1, 83: 1}
        expected = [
            (0, 82),
            (1, 83),
        ]
        result = reconstruct_timeline(src)
        self.assertEqual(result, expected)

        src = {82: 0.1, 83: 0.1}
        expected = [
            (0, 82),
            (10, 83),
        ]
        result = reconstruct_timeline(src)
        self.assertEqual(result, expected)
