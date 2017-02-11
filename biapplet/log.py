#!/usr/bin/python
from __future__ import division
import re
import copy
import datetime
import unittest


LOG_BATTERY_FILE = 'logs/capacity'


def battery(capacity, status):
    t = datetime.datetime.now().isoformat()
    line = '{0} {1}% {2}\n'.format(t, capacity, status)
    with open(LOG_BATTERY_FILE, 'a') as f:
        f.write(line)


def to_datetime(dt_iso):
    # 2017-01-09T23:02:12.315436
    dt, _, us = dt_iso.partition('.')
    dt = datetime.datetime.strptime(dt, '%Y-%m-%dT%H:%M:%S')
    us = int(us.rstrip("Z"), 10)
    return dt + datetime.timedelta(microseconds=us)


def parse_log_line(line):
    m = re.search(
        '(\d+-\d+-\d+T\d+:\d+:\d+\.\d*)\s+(\d+)%\s+(\w+)', line)
    if m:
        ts = to_datetime(m.group(1))
        cap = float(m.group(2))
        stat = m.group(3)
        return {
            'time': ts,
            'capacity': cap,
            'status': stat
        }


def get_battery():
    lines = []
    with open(LOG_BATTERY_FILE, 'r') as f:
        lines = f.readlines()

    return [parse_log_line(x) for x in lines]


def get_time_capacity(src):
    return [[e['time'], int(e['capacity'])] for e in src]


def convert_to_relative_time(src):
    if len(src) <= 0:
        return []
    src = sorted(src)
    t0 = src[-1][0]
    return [
        [-(t0 - e[0]).total_seconds(), e[1]] for e in src
    ]


def cut_pauses(src, threshold):
    res = []
    src = sorted(src, reverse=True)
    n = len(src)
    for i in xrange(0, n):
        y = src[i][1]
        t2 = src[i][0]
        if i == 0:
            res.append([t2, y])
            continue
        t1 = src[i-1][0]
        dt = t1 - t2
        if dt >= threshold:
            dt = 1e-3
        x = res[-1][0]
        res.append([x-dt, y])
    res = sorted(res)
    return res


class LinearInterpolation:

    def __init__(self, data):
        self.data = sorted(data)

    def resample(self, samples_number):
        n = len(self.data)
        if n <= 0 or n == samples_number:
            return self.data
        if samples_number == 0:
            return []
        if samples_number == 1:
            return [self.resample(3)[1]]
        x0 = self.data[0][0]
        xn = self.data[-1][0]
        st = (xn - x0) / (samples_number - 1)
        res = []
        for i in xrange(1, n):
            x1 = self.data[i-1][0]
            x2 = self.data[i][0]
            y1 = self.data[i-1][1]
            y2 = self.data[i][1]
            for j in xrange(0, samples_number):
                x = x0 + j * st
                if x1 <= x and x <= x2:
                    y = y1 + (y2 - y1) * (x - x1) / (x2 - x1)
                    res.append([x, y])
        return res


def calculate_virtual_time(samples, threshold_sec):
    prev = None
    virtual_time = 0
    for curr in samples:
        if prev is not None:
            t1 = prev['relative_time_sec']
            t2 = curr['relative_time_sec']
            delta = t2 - t1
            is_overtime = delta >= threshold_sec
            is_status_changed = curr['status'] != prev['status']

            if not is_overtime and not is_status_changed:
                virtual_time += delta

        curr['virtual_time_sec'] = virtual_time
        prev = copy.deepcopy(curr)

    return samples


def separate_by_status(samples):
    result = []
    chunk = []
    prev = None
    for curr in samples:
        if prev is not None:
            if curr['status'] != prev['status']:
                result.append(chunk)
                chunk = []

        chunk.append(curr)
        prev = curr

    result.append(chunk)
    return result


def calculate_life(src):
    time_limit = 5.0 / 60.0
    a = filter(lambda d: d['virtual_time_hour'] < time_limit, src)
    a = sorted(a, key=lambda e: e['virtual_time_hour'])
    if len(a) <= 0:
        return

    curr_status = a[0]['status']
    b = []
    for e in a:
        if e['status'] != curr_status:
            break
        b.append(e)
    a = b

    if len(a) <= 0:
        return
    dy = a[-1]['capacity'] - a[0]['capacity']
    dx = a[-1]['virtual_time_hour'] - a[0]['virtual_time_hour']
    k = dy/dx
    life = 100.0/k
    return life


def calculate_history_chart(image_path):
    a = get_battery()

    # find max time
    t0 = max([e['time'] for e in a])

    # add relative time
    for e in a:
        t = float((t0 - e['time']).total_seconds())
        e['relative_time_sec'] = t

    # sort by relative_time
    a = sorted(a, key=lambda e: e['relative_time_sec'])

    # cut pauses
    threshold_sec = 15 * 60
    res = calculate_virtual_time(a, threshold_sec)

    # add virtual time
    for e in res:
        t = e['virtual_time_sec']
        e['virtual_time_min'] = t/(60)
        e['virtual_time_hour'] = t/(60*60)

    # y = kx + b, b=0
    # x = y/k - b/k
    # k = 100/life
    b = 0
    life = calculate_life(res)
    k = 100/life
    y = float(res[0]['capacity'])
    x = y/k - b/k
    xl = [0, x]
    yl = [0, y]
    xoffset = x

    res = filter(lambda d: d['virtual_time_hour'] < (12.0-xoffset), res)
    res = separate_by_status(res)

    # plot chunks
    import chart

    ylabels = ['0 %', '25 %', '50 %', '75%', '100 %']
    xlabels = [0, 2, 4, 6, 8, 10, '12 hours']
    plot = chart.Chart(inverseX=True,
                       xlabels=xlabels, ylabels=ylabels,
                       padding_top=30,
                       height=450)
    plot.set_minimal_canvas([0, 0], [12, 100])

    for ch in res:
        is_charging = ch[0]['status'] == 'Charging'
        color = '#4aa635' if is_charging else '#2e7eb3'

        xs = [x['virtual_time_hour']+xoffset for x in ch]
        ys = [int(x['capacity']) for x in ch]

        plot.add(xs=xs, ys=ys, stroke=color, fill=color)


    plot.add(xs=xl, ys=yl, stroke='#2e7eb3', stroke_dash=True)
    plot.render_to_svg(image_path)


def main():
    calculate_history_chart('test.svg')


class LogProcessingTest(unittest.TestCase):

    def test_to_datetime(self):
        self.assertEqual(
            to_datetime('2017-01-09T23:02:12.315436'),
            datetime.datetime(2017, 1, 9, 23, 2, 12, 315436))

    def test_get_time_capacity(self):
        src = []
        exp = []
        self.assertEqual(get_time_capacity(src), exp)

        src = [
            {'time': 1, 'capacity': 2},
            {'time': 3, 'capacity': 4},
            {'time': 5, 'capacity': 6}
        ]
        exp = [
            [1, 2],
            [3, 4],
            [5, 6]
        ]
        self.assertEqual(get_time_capacity(src), exp)

    def test_convert_to_relative_time(self):
        src = []
        exp = []
        self.assertEqual(convert_to_relative_time(src), exp)

        src = [
            [datetime.datetime(2000, 1, 1, 10, 0, 0), 1],
            [datetime.datetime(2000, 1, 1, 10, 0, 5), 2]
        ]
        exp = [
            [-5, 1],
            [0, 2]
        ]
        self.assertEqual(convert_to_relative_time(src), exp)

    def test_cut_pauses(self):
        src = []
        exp = []
        self.assertEqual(cut_pauses(src, 1), exp)

        src = [
            [-5, 1],
            [0, 2]
        ]
        exp = [
            [-5, 1],
            [0, 2]
        ]
        self.assertEqual(cut_pauses(src, 5.1), exp)

        src = [
            [-5, 1],
            [0, 2]
        ]
        exp = [
            [-0.001, 1],
            [0, 2]
        ]
        self.assertEqual(cut_pauses(src, 5), exp)

        src = [
            [-11, 1],
            [-10, 2],
            [-5, 3],
            [0, 4]
        ]
        exp = [
            [-1.002, 1],
            [-0.002, 2],
            [-0.001, 3],
            [0, 4]
        ]
        self.assertEqual(cut_pauses(src, 5), exp)

    def test_LinearInterpolation(self):
        src = []
        exp = []
        res = LinearInterpolation(src).resample(10)
        self.assertEqual(res, exp)

        src = [
            [0, 20],
            [10, 30]
        ]
        exp = []
        res = LinearInterpolation(src).resample(0)
        self.assertEqual(res, exp)

        src = [
            [0, 20],
            [10, 30]
        ]
        exp = [
            [5, 25]
        ]
        res = LinearInterpolation(src).resample(1)
        self.assertEqual(res, exp)

        src = [
            [0, 20],
            [10, 30]
        ]
        exp = [
            [0, 20],
            [10, 30]
        ]
        res = LinearInterpolation(src).resample(2)
        self.assertEqual(res, exp)

        src = [
            [0, 20],
            [10, 30]
        ]
        exp = [
            [0, 20],
            [5, 25],
            [10, 30]
        ]
        res = LinearInterpolation(src).resample(3)
        self.assertEqual(res, exp)

        src = [
            [0, 20],
            [10, 30]
        ]
        exp = [
            [0, 20],
            [2, 22],
            [4, 24],
            [6, 26],
            [8, 28],
            [10, 30]
        ]
        res = LinearInterpolation(src).resample(6)
        self.assertEqual(res, exp)

        src = [
            [-10, 20],
            [0, 30]
        ]
        exp = [
            [-5, 25]
        ]
        res = LinearInterpolation(src).resample(1)
        self.assertEqual(res, exp)

        src = [
            [-10, 20],
            [0, 30]
        ]
        exp = [
            [-10, 20],
            [0, 30]
        ]
        res = LinearInterpolation(src).resample(2)
        self.assertEqual(res, exp)

        src = [
            [-10, 20],
            [0, 30]
        ]
        exp = [
            [-10, 20],
            [-5, 25],
            [0, 30]
        ]
        res = LinearInterpolation(src).resample(3)
        self.assertEqual(res, exp)

        src = [
            [-10, 20],
            [0, 30]
        ]
        exp = [
            [-10, 20],
            [-8, 22],
            [-6, 24],
            [-4, 26],
            [-2, 28],
            [0, 30]
        ]
        res = LinearInterpolation(src).resample(6)
        self.assertEqual(res, exp)


if __name__ == '__main__':
    main()
    #unittest.main()
