#!/usr/bin/python
import re
import datetime


LOG_BATTERY_FILE = 'logs/capacity'


def battery(capacity, status):
    t = datetime.datetime.now().isoformat()
    line = '{0} {1}% {2}\n'.format(t, capacity, status)
    with open(LOG_BATTERY_FILE, 'a') as f:
        f.write(line)


def to_dt(dt_str):
    # 2017-01-09T23:02:12.315436
    dt, _, us = dt_str.partition('.')
    dt = datetime.datetime.strptime(dt, '%Y-%m-%dT%H:%M:%S')
    us = int(us.rstrip("Z"), 10)
    return dt + datetime.timedelta(microseconds=us)


def get_battery():
    lines = []
    with open(LOG_BATTERY_FILE, 'r') as f:
        lines = f.readlines()

    data = []
    for line in lines:
        m = re.search(
            '(\d+-\d+-\d+T\d+:\d+:\d+\.\d*)\s+(\d+)%\s+(\w+)', line)
        if m:
            ts = to_dt(m.group(1))
            cap = m.group(2)
            stat = m.group(3)
            data.append({
                'time': ts,
                'capacity': cap,
                'status': stat
            })

    return data
