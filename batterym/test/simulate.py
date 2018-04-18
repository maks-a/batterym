#!/usr/bin/python
import time
import random

status_file_dbg = 'data/uevent.tmp'
capacity_file = 'data/capacity.tmp'
status_file = 'data/status.tmp'

capacity = 0
is_charging = True
status = 'Charging'

pattern = """POWER_SUPPLY_NAME = BAT0
POWER_SUPPLY_STATUS = {status}
POWER_SUPPLY_PRESENT = 1
POWER_SUPPLY_TECHNOLOGY = Li-poly
POWER_SUPPLY_CYCLE_COUNT = 0
POWER_SUPPLY_VOLTAGE_MIN_DESIGN = 7500000
POWER_SUPPLY_VOLTAGE_NOW = 8112000
POWER_SUPPLY_CURRENT_NOW = 2394000
POWER_SUPPLY_CHARGE_FULL_DESIGN = 6480000
POWER_SUPPLY_CHARGE_FULL = 6151000
POWER_SUPPLY_CHARGE_NOW = 5945000
POWER_SUPPLY_CAPACITY = {capacity}
POWER_SUPPLY_CAPACITY_LEVEL = Normal
POWER_SUPPLY_MODEL_NAME = DELL 0DRRP55
POWER_SUPPLY_MANUFACTURER = Sanyo
POWER_SUPPLY_SERIAL_NUMBER = 1358
"""


def update_capacity():
    global capacity
    global is_charging
    global status

    if capacity <= 0:
        is_charging = True
    if capacity >= 105:
        is_charging = False

    direction = 1 if is_charging else -1
    step = random.randrange(-2, 6, 1)
    capacity += step * direction
    status = 'Charging' if is_charging else 'Discharging'
    if capacity >= 95:
        status = 'Full'


def fill_pattern():
    return pattern.format(status=status, capacity=capacity)


def main():
    while True:
        update_capacity()
        print('capacity: {0}, {1}'.format(capacity, status))
        with open(status_file_dbg, 'w') as f:
            f.write(fill_pattern())

        with open(capacity_file, 'w') as f:
            f.write(str(capacity))

        with open(status_file, 'w') as f:
            f.write(status)

        time.sleep(0.5)

if __name__ == '__main__':
    main()
