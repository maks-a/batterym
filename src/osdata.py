#!/usr/bin/python
import re


_DEBUG = True

status_file_release = '/sys/class/power_supply/BAT0/uevent'
status_file_dbg = 'data/uevent'
status_file = status_file_dbg if _DEBUG else status_file_release


def _limit(val, lo, hi):
    return max(lo, min(val, hi))


def battery_capacity():
    with open(status_file, 'r') as f:
        m = re.search('POWER_SUPPLY_CAPACITY=(\d+)', f.read())
        if m:
            return _limit(int(m.group(1)), 0, 100)


def battery_status():
    with open(status_file, 'r') as f:
        m = re.search('POWER_SUPPLY_STATUS=(\w+)', f.read())
        if m:
            return m.group(1)


def is_discharging():
    if battery_status() == 'Discharging':
        return True


def is_full():
    if battery_status() == 'Full':
        return True


def is_charging():
    if battery_status() == 'Charging':
        return True
