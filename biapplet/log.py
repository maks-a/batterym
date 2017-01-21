#!/usr/bin/python
import re
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
        cap = m.group(2)
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
    return [[e['time'], e['capacity']] for e in src]


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
    src = sorted(src)
    n = len(src)
    for i in xrange(0, n):
        y = src[i][1]
        t2 = src[i][0]
        if i == 0:
            res.append([t2, y])
            continue
        t1 = src[i-1][0]
        dt = t2 - t1
        if dt >= threshold:
            dt = 1e-3
        res.append([t1+dt, y])
    return res


class LinearInterpolation:

    def __init__(self, data):
        self.data = sorted(data)
        self.min = self.data[0][0]
        self.max = self.data[-1][0]

    def resample(samples_number):
        pass


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
            [-5, 1],
            [-4.999, 2]
        ]
        self.assertEqual(cut_pauses(src, 5), exp)


if __name__ == '__main__':
    unittest.main()
