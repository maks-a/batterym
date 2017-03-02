#!/usr/bin/python
import re
import datetime


LOG_BATTERY_FILE = 'logs/capacity'


def battery(capacity, status):
    t = datetime.datetime.now().isoformat()
    line = '{0} {1}% {2}\n'.format(t, capacity, status)
    with open(LOG_BATTERY_FILE, 'a') as f:
        f.write(line)


def parse_log_line(line, prog):
    m = prog.match(line)
    if m:
        return {
            'time': datetime.datetime(
                int(m.group('Y')), int(m.group('m')), int(m.group('d')),
                int(m.group('H')), int(m.group('M')), int(m.group('S'))),
            'capacity': float(m.group('cap')),
            'status': m.group('stat')
        }


def get_lines(fname):
    with open(fname, 'r') as f:
        lines = f.readlines()
        return lines


def parse_log_lines(lines):
    Ymd = '(?P<Y>\d+)-(?P<m>\d+)-(?P<d>\d+)'
    HMSus = '(?P<H>\d+):(?P<M>\d+):(?P<S>\d+)\.(?P<us>\d*)'
    pattern = Ymd + 'T' + HMSus + '\s+(?P<cap>\d+)%\s+(?P<stat>\w+)'
    prog = re.compile(pattern)
    return [parse_log_line(lines, prog) for lines in lines]


def get_battery():
    lines = get_lines(LOG_BATTERY_FILE)
    return filter(lambda line: line is not None, parse_log_lines(lines))
