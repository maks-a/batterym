#!/usr/bin/python
from datetime import datetime as dt


LOG_BATTERY_FILE = 'logs/capacity'


def battery(capacity, status):
    t = dt.now().isoformat()
    line = '{0} {1}% {2}\n'.format(t, capacity, status)
    with open(LOG_BATTERY_FILE, 'a') as f:
        f.write(line)
