#!/usr/bin/python
from batterym import mathstat
import unittest


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


def extrapolate(data, lo=0, hi=100):
    keys = data.keys()
    if len(keys) == 0:
        return data
    mx = max(keys)
    for k in range(mx+1, hi+1, 1):
        data[k] = data[mx]
    mn = min(keys)
    for k in range(mn-1, lo-1, -1):
        data[k] = data[mn]
    keys = data.keys()
    values = data.values()
    for i in range(1, len(keys)):
        for k in range(keys[i-1]+1, keys[i]):
            data[k] = (values[i-1] + values[i]) / 2
    return data


def reconstruct_timeline(slopes, ys):
    capacity = slopes.keys()
    slope = slopes.values()
    n = len(slopes)
    if n < 2:
        return []
    xs = [0]
    ys2 = [0]
    for i in range(1, len(ys)):
        dy = float(ys[i] - ys[i-1])
        slope = slopes.get(ys[i-1])
        if slope is None:
            continue
        dx = dy / slope
        x = xs[-1] + dx
        xs.append(x)
        if i == 1:
            ys2[0] = ys[i-1]
        ys2.append(ys[i])
    new_x, new_y = mathstat.interpolate_linear_evenly(xs, ys2, n=n)
    return zip(new_x, new_y)


class StatBateryModel:

    def __init__(self, history):
        self.history = history
        self.hdata = history.data()
        self.percentile = 0.5
        self.history_limit = 100.0

    def calculate(self, start=None):
        # split charge/discharge
        hdata = self.hdata
        hdata = filter(lambda e: e['virtual_time_hour']
                       < self.history_limit, hdata)
        charge = filter(lambda e: e['status'] == 'Charging', hdata)
        discharge = filter(lambda e: e['status'] == 'Discharging', hdata)
        # extract slopes by capacity bins
        charge_bins = get_slopes_capacity_bins(charge)
        discharge_bins = get_slopes_capacity_bins(discharge)
        # pick up slopes curve (by percentile)
        p = self.percentile
        charge_slopes = get_slopes_by_percentile(charge_bins, p)
        charge_slopes = extrapolate(charge_slopes, 0, 100)
        discharge_slopes = get_slopes_by_percentile(discharge_bins, p)
        discharge_slopes = extrapolate(discharge_slopes, 0, 100)
        # reconstruct (dis)charging capacity timeline
        ys1 = range(100, 0, -1)
        charge_timeline_total = reconstruct_timeline(charge_slopes, ys1)
        ys2 = range(0, 100)
        discharge_timeline_total = reconstruct_timeline(discharge_slopes, ys2)

        charge_timeline = discharge_timeline = []
        if start is not None:
            ys1 = range(100, start-1, -1)
            charge_timeline = reconstruct_timeline(charge_slopes, ys1)
            ys2 = range(0, start+1)
            discharge_timeline = reconstruct_timeline(discharge_slopes, ys2)
        # store data
        self.charge = charge
        self.charge_bins = charge_bins
        self.charge_slopes = charge_slopes
        self.charge_timeline = charge_timeline
        self.charge_timeline_total = charge_timeline_total
        self.discharge = discharge
        self.discharge_bins = discharge_bins
        self.discharge_slopes = discharge_slopes
        self.discharge_timeline = discharge_timeline
        self.discharge_timeline_total = discharge_timeline_total

    def plot_data(self, status):
        if status == 'Charging' and len(self.charge_timeline) > 0:
            x, y = zip(*self.charge_timeline)
            return [{'status': 'Charging', 'xs': x, 'ys': y}]
        if status == 'Discharging' and len(self.discharge_timeline) > 0:
            x, y = zip(*self.discharge_timeline)
            return [{'status': 'Discharging', 'xs': x, 'ys': y}]
        return []


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
        slopes = {}
        ys = []
        expected = []
        result = reconstruct_timeline(slopes, ys)
        self.assertEqual(result, expected)

        slopes = {82: 2}
        ys = []
        expected = []
        result = reconstruct_timeline(slopes, ys)
        self.assertEqual(result, expected)

        slopes = {82: 1, 83: 1}
        ys = [82, 83]
        expected = [
            (0, 82),
            (1, 83),
        ]
        result = reconstruct_timeline(slopes, ys)
        self.assertEqual(result, expected)

        slopes = {82: 1, 83: 1}
        ys = [83, 82]
        expected = [
            (0, 83),
            (-1, 82),
        ]
        result = reconstruct_timeline(slopes, ys)
        self.assertEqual(result, expected)

        slopes = {82: 0.1, 83: 0.1}
        ys = [82, 83]
        expected = [
            (0, 82),
            (10, 83),
        ]
        result = reconstruct_timeline(slopes, ys)
        self.assertEqual(result, expected)

        slopes = {82: 0.1, 83: 0.1}
        ys = [83, 82]
        expected = [
            (0, 83),
            (-10, 82),
        ]
        result = reconstruct_timeline(slopes, ys)
        self.assertEqual(result, expected)

        slopes = {82: -1, 83: -1}
        ys = [82, 83]
        expected = [
            (0, 82),
            (-1, 83),
        ]
        result = reconstruct_timeline(slopes, ys)
        self.assertEqual(result, expected)

        slopes = {82: -1, 83: -1}
        ys = [83, 82]
        expected = [
            (0, 83),
            (1, 82),
        ]
        result = reconstruct_timeline(slopes, ys)
        self.assertEqual(result, expected)

    def test_extrapolate(self):
        src = {}
        expected = {}
        result = extrapolate(src)
        self.assertEqual(result, expected)

        src = {5: 25}
        expected = {4: 25, 5: 25, 6: 25}
        result = extrapolate(src, 4, 6)
        self.assertEqual(result, expected)

        src = {5: 20, 7: 40}
        expected = {4: 20, 5: 20, 6: 30, 7: 40, 8: 40}
        result = extrapolate(src, 4, 8)
        self.assertEqual(result, expected)
