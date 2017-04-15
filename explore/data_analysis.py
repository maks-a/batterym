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
X_BEGIN = 0
X_END = 21

y1 = data['capacity'].values
y2 = data['capacity_raw'].values
x = data['virtual_time_hour']
cap = pd.DataFrame({'capacity': y1, 'capacity_raw': y2}, index=x)
cap = cap[X_END:X_BEGIN]

fig, ax = plt.subplots(1, sharex=True)
ax.plot(cap['capacity_raw'], color='r', marker='x')
ax.plot(cap['capacity'], color='b', marker='+')
ax.set_xlim(X_BEGIN, X_END)
ax.set_ylim(0, 105)
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
