#!/usr/bin/python
import pandas as pd
import numpy as np
import matplotlib
import datetime as dt

from matplotlib import pyplot as plt

# Import modules from /batterym/ folder.
import os
import sys
sys.path.append(os.path.abspath('../batterym'))
import log
import history
import mathstat


# Emulates the aesthetics of ggplot (a popular plotting package for R).
plt.style.use('ggplot')

logs = log.get_battery('../logs/capacity_example')
h = history.History(logs, smoothing=True)
hdata = h.data()

data = pd.DataFrame(hdata)
data = data.rename(columns={'time': 'timestamp'})
data = data.sort_values(by='timestamp', ascending=True)

print data.head()

# Extract capacity time series.
# Parameters
X_NOW = 9
X_BEGIN = X_NOW - 5
X_END = X_NOW + 25.0
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

cap_raw_old = cap_old['capacity_raw']
cap_raw_new = cap_new['capacity_raw']

fig, ax = plt.subplots(1)

# ax[0].fill_between(cap_raw_old.index, 0,
#                    cap_raw_old.values, facecolor='#999999')
# ax[0].fill_between(cap_raw_new.index, 0,
#                    cap_raw_new.values, facecolor='#cccccc')
# ax[0].plot(cap['capacity'], color='b')
# ax[0].plot(charging_old['capacity'], color='#00FF00',
#            marker='o', linestyle='None')
# ax[0].plot(discharging_old['capacity'], color='#0000FF',
#            marker='o', linestyle='None')
# ax[0].plot([X_NOW, X_NOW], [Y_MIN, Y_MAX], color='r')
# ax[0].set_xlim(X_BEGIN, X_END)
# ax[0].set_ylim(Y_MIN, Y_MAX)
# ax[0].invert_xaxis()

# ax[1].hist(cap['capacity'], bins=10)

status = 'Charging'

charging_hdata = filter(lambda e: e['status']==status, hdata)
charging_bins = history.get_capacity_round_bins(charging_hdata)
x1 = charging_bins.keys()
y1 = [mathstat.percentile(charging_bins[x], 0.5) for x in x1]
new_slopes = {}
for i in xrange(0, len(x1)):
    new_slopes[x1[i]] = y1[i]

y2 = range(10, 101, 1)
#y2 = range(100, 10, -1)
x2 = [0]
for i in xrange(1, len(y2)):
    dy = y2[i] - y2[i-1]
    sl = new_slopes[y2[i-1]]
    dx = dy / sl
    x = x2[i-1] + dx
    x2.append(x)

# d = data[data['status'] == status]
# d = d[d['slope'] != 0]
# x = d['capacity_round']
# y = d['slope']
# ax.scatter(x, y)
# ax.plot(pd.Series(y1, index=x1), color='#FF0000', marker='o')
# ax.set_xlim(0, 101)

ax.plot(pd.Series(y2, index=x2), color='#FF0000', marker='+')
ax.set_ylim(0, 101)
ax.invert_xaxis()


# Full screen plot window.
mng = plt.get_current_fig_manager()
mng.resize(*mng.window.maxsize())

# Show plot.
plt.show()
