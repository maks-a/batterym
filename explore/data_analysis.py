#!/usr/bin/python
import pandas as pd
import numpy as np
import matplotlib
import datetime as dt

from matplotlib import pyplot as plt

# Import modules from /batterym/ folder.
import sys
sys.path.append('../batterym')
import log
import history


# Emulates the aesthetics of ggplot (a popular plotting package for R).
plt.style.use('ggplot')

logs = log.get_battery('../logs/capacity_example')
h = history.History(logs, smoothing=True)

data = pd.DataFrame(h.data())
data = data.rename(columns={'time': 'timestamp'})
data['date'] = pd.Series(data['timestamp'].dt.date)
data['time'] = pd.Series(data['timestamp'].dt.time)
data['weekday'] = pd.Series(data['timestamp'].dt.weekday)
data = data.sort_values(by='timestamp', ascending=True)

print data.head()

# Extract capacity time series.
# Parameters
X_NOW = 9
X_BEGIN = X_NOW - 5.0
X_END = X_NOW + 5.0
Y_MAX = 101
Y_MIN = 0
blue = '#2e7eb3'
light_blue = '#81b1d1'
green = '#4aa635'
light_green = '#7db471'


y1 = data['capacity'].values
y2 = data['capacity_raw'].values
f = data['status'].values
x = data['virtual_time_hour']
cap = pd.DataFrame({'capacity': y1, 'capacity_raw': y2, 'status': f}, index=x)
cap = cap[X_END:X_BEGIN]
cap_old = cap[X_END:X_NOW]
cap_new = cap[X_NOW:X_BEGIN]

charging = cap[cap['status'] == 'Charging']
discharging = cap[cap['status'] == 'Discharging']

charging_old = charging[X_END:X_NOW]
charging_new = charging[X_NOW:X_BEGIN]
discharging_old = discharging[X_END:X_NOW]
discharging_new = discharging[X_NOW:X_BEGIN]

fig, ax = plt.subplots(1, sharex=True)

cap_raw_old = cap_old['capacity_raw']
cap_raw_new = cap_new['capacity_raw']
ax.fill_between(cap_raw_old.index, 0, cap_raw_old.values, facecolor='#999999')
ax.fill_between(cap_raw_new.index, 0, cap_raw_new.values, facecolor='#cccccc')

ax.plot(cap['capacity'], color='b')

ax.plot(charging_old['capacity'], color='#00FF00',
        marker='o', linestyle='None')
ax.plot(discharging_old['capacity'], color='#0000FF',
        marker='o', linestyle='None')

ax.plot([X_NOW, X_NOW], [Y_MIN, Y_MAX], color='r')
ax.set_xlim(X_BEGIN, X_END)
ax.set_ylim(Y_MIN, Y_MAX)
ax.invert_xaxis()

# Full screen plot window.
mng = plt.get_current_fig_manager()
mng.resize(*mng.window.maxsize())

# Show plot.
plt.show()


# SOME DEBUG CODE
# plt.figure()
# data['capacity'].plot()
# plt.figure()
# data['weekday'].hist(bins=7)
# plt.figure()
# data['capacity'].hist(bins=10)
# plt.figure()
# data['time'].hist(bins=24)
