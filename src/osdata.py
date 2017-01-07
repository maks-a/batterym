#!/usr/bin/python
import re


status_file = '/sys/class/power_supply/BAT0/uevent'


def battery_capacity():
    with open(status_file, 'r') as f:
        m = re.search('POWER_SUPPLY_CAPACITY=(\d+)', f.read())
        if m:
            return int(m.group(1))


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
