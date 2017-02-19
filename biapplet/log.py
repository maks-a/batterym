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
        return {
            'time': to_datetime(m.group(1)),
            'capacity': float(m.group(2)),
            'status': m.group(3)
        }


def get_battery():
    lines = []
    with open(LOG_BATTERY_FILE, 'r') as f:
        lines = f.readlines()

    return [parse_log_line(x) for x in lines]


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
        curr['virtual_time_min'] = virtual_time/60
        curr['virtual_time_hour'] = virtual_time/(60*60)
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


def median(lst):
    n = len(lst)
    if n < 1:
        return
    lst = sorted(lst)
    m = int(n/2)
    if n % 2 == 1:
        return lst[m]
    return (lst[m-1] + lst[m])/2


def calculate_slope(src):
    time_limit = 10.0 / 60.0
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

    ks = []
    n = len(a)
    for i in xrange(1, n):
        dy = a[i]['capacity'] - a[0]['capacity']
        dx = a[i]['virtual_time_hour'] - a[0]['virtual_time_hour']
        if dx < 1e-9:
            continue
        k = dy/dx
        ks.append(k)
    k = median(ks)
    return k


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

    xoffset = 0
    slope = calculate_slope(res)
    xl = yl = []
    eps = 1e-9
    if slope is not None and (slope < -eps or eps < slope):
        # y = kx + b, b=0
        # x = y/k - b/k
        # k = 100/life
        b = 0
        life = 100.0/abs(slope)
        k = slope
        y = res[0]['capacity']
        x = y/k - b/k
        x = abs(x)
        if slope > 0:
            yl = [0, y]
            xl = [0, x]
        else:
            dy = 100.0-y
            x = -dy/slope
            xl = [0, x]
            yl = [100, y]

        xoffset = x

        # life_time = datetime.timedelta(seconds=life*60*60)
        # remaining_life_time = datetime.timedelta(seconds=xoffset*60*60)
        # print life_time, remaining_life_time

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

    blue = '#2e7eb3'
    green = '#4aa635'
    prediction_color = None
    for ch in res:
        is_charging = ch[0]['status'] == 'Charging'
        color = green if is_charging else blue
        if prediction_color is None:
            prediction_color = color

        xs = [x['virtual_time_hour']+xoffset for x in ch]
        ys = [int(x['capacity']) for x in ch]

        plot.add(xs=xs, ys=ys, stroke=color, fill=color)

    plot.add(xs=xl, ys=yl,
             stroke=prediction_color, stroke_dash=True)
    plot.render_to_svg(image_path)


def main():
    calculate_history_chart('capacity_history_12h.svg')


class LogProcessingTest(unittest.TestCase):

    def test_to_datetime(self):
        self.assertEqual(
            to_datetime('2017-01-09T23:02:12.315436'),
            datetime.datetime(2017, 1, 9, 23, 2, 12, 315436))


if __name__ == '__main__':
    main()
    # unittest.main()
