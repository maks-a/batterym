#!/usr/bin/python
import re
import unittest

from batterym import fileio


_DEBUG = False

uevent_file_release = '/sys/class/power_supply/BAT0/uevent'
uevent_file_dbg = 'test/data/uevent.tmp'
uevent_file = uevent_file_dbg if _DEBUG else uevent_file_release

capacity_file_release = '/sys/class/power_supply/BAT0/capacity'
capacity_file_dbg = 'test/data/capacity.tmp'
capacity_file = capacity_file_dbg if _DEBUG else capacity_file_release

status_file_release = '/sys/class/power_supply/BAT0/status'
status_file_dbg = 'test/data/status.tmp'
status_file = status_file_dbg if _DEBUG else status_file_release


def _limit(val, lo, hi):
    return max(lo, min(val, hi))


def battery_capacity():
    m = re.search('(\d+)', fileio.read(capacity_file))
    if m:
        return _limit(int(m.group(1)), 0, 100)


def battery_status_original():
    m = re.search('(\w+)', fileio.read(status_file))
    if m:
        return m.group(1)


def battery_status():
    status = battery_status_original()
    if status == 'Charging' or status == 'Full':
        return 'Charging'
    return 'Discharging'


def is_discharging():
    return battery_status() == 'Discharging'


def is_charging():
    return battery_status() == 'Charging'


class MyTest(unittest.TestCase):

    def test_limit(self):
        self.assertEqual(_limit(5, 4, 6), 5)
        self.assertEqual(_limit(3, 4, 6), 4)
        self.assertEqual(_limit(7, 4, 6), 6)
