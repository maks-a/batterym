#!/usr/bin/python
import os
import re
import misc
import datetime
import resource
import unittest


LOG_BATTERY_FILE = os.path.join(
    resource.RESOURCES_DIRECTORY_PATH, 'logs/capacity')


def battery(capacity, status):
    t = datetime.datetime.now().isoformat()
    line = '{0} {1}% {2}\n'.format(t, capacity, status)
    misc.append_to_file(line, LOG_BATTERY_FILE)


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


def parse_log_lines(lines):
    Ymd = '(?P<Y>\d+)-(?P<m>\d+)-(?P<d>\d+)'
    HMSus = '(?P<H>\d+):(?P<M>\d+):(?P<S>\d+)\.(?P<us>\d*)'
    pattern = Ymd + 'T' + HMSus + '\s+(?P<cap>\d+)%\s+(?P<stat>\w+)'
    prog = re.compile(pattern)
    return [parse_log_line(lines, prog) for lines in lines]


def get_battery():
    lines = misc.read_lines_from_file(LOG_BATTERY_FILE)
    return filter(lambda line: line is not None, parse_log_lines(lines))


class MyTest(unittest.TestCase):

    def test_parse_log_line(self):
        self.assertEqual(parse_log_lines(
            ['2017-01-09T22:59:17.275801 100% Full']),
            [{
                'time': datetime.datetime(2017, 1, 9, 22, 59, 17),
                'capacity': 100,
                'status': 'Full',
            }]
        )
        self.assertEqual(parse_log_lines(
            ['2017-01-09T22:59:17.275801 95% Discharging']),
            [{
                'time': datetime.datetime(2017, 1, 9, 22, 59, 17),
                'capacity': 95,
                'status': 'Discharging',
            }]
        )
        self.assertEqual(parse_log_lines(
            ['2017-01-09T22:59:17.275801 46% Charging']),
            [{
                'time': datetime.datetime(2017, 1, 9, 22, 59, 17),
                'capacity': 46,
                'status': 'Charging',
            }]
        )
        self.assertEqual(parse_log_lines(
            ['2017-01-09T22:59:17.275801 97% Unknown']),
            [{
                'time': datetime.datetime(2017, 1, 9, 22, 59, 17),
                'capacity': 97,
                'status': 'Unknown',
            }]
        )
