#!/usr/bin/python
import re


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
    with open(capacity_file, 'r') as f:
        m = re.search('(\d+)', f.read())
        if m:
            return _limit(int(m.group(1)), 0, 100)


def battery_status():
    with open(status_file, 'r') as f:
        m = re.search('(\w+)', f.read())
        if m:
            return m.group(1)


def is_discharging():
    return battery_status() == 'Discharging'


def is_full():
    return battery_status() == 'Full'


def is_charging():
    return battery_status() == 'Charging'
