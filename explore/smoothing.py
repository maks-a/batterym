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
import smooth
import history


plt.style.use('ggplot')

logs = log.get_battery('../logs/capacity_example')
h = history.History(logs, smoothing=True)
hdata = h.data()

data = pd.DataFrame(hdata)
data = data.rename(columns={'time': 'timestamp'})
data = data.sort_values(by='timestamp', ascending=True)

# Extract charging sessions
data = data[data['status'] == 'Charging']

# Group by sequence_id
grouped = data.groupby('sequence_id')['capacity_raw'].max()
grouped = grouped[grouped.values >= 100]
data = data[data.sequence_id.isin(grouped.index)]

CAP_LOW = 80
grouped = data.groupby('sequence_id')['capacity_raw'].min()
grouped = grouped[grouped.values <= CAP_LOW]
data = data[data.sequence_id.isin(grouped.index)]
data = data[data['capacity_raw'] >= CAP_LOW]

grouped = data.groupby('sequence_id')['capacity_raw'].count()
grouped = grouped.sort_values(inplace=False, ascending=False)
grouped = grouped[:1]
data = data[data.sequence_id.isin(grouped.index)]


fig, ax = plt.subplots()

grouped = data.groupby('sequence_id')
for name, group in grouped:
    pivot_time = group['timestamp'].min()
    delta = group['timestamp'] - pivot_time
    seconds = abs(delta).dt.seconds
    hours = seconds / (60 * 60)
    group['delta_time'] = hours
    group = group.sort_values(by='delta_time', ascending=True)

    ax.plot(group['delta_time'], group['capacity_raw'], color='r', marker='x')

    x = list(group['delta_time'])
    y = list(group['capacity_raw'])

    n = min(len(x), len(y))
    for i in xrange(15, min(n-2, 30)):
        x2, y2 = smooth.steps_filter(x[:i], y[:i])
        ax.plot(x2, y2, color='b', marker='o')

    x2, y2 = smooth.steps_filter(x, y)
    ax.plot(x2, y2, color='b', marker='o')

#ax.set_ylim(0, 101)
ax.set_xlim(0, 1.8)
ax.set_ylim(CAP_LOW, 101)
# Full screen plot window.
mng = plt.get_current_fig_manager()
mng.resize(*mng.window.maxsize())
# Show plot.
plt.show()
# break


def draw_round():
    x = np.linspace(0, 10, 200)
    y = 10 * np.sin(x)
    y2 = np.round(y)

    fig, ax = plt.subplots()

    ax.set_ylim(-11, 11)
    ax.plot(x, y, color='b', marker='+')
    ax.plot(x, y2, color='r', marker='o')

    # Full screen plot window.
    mng = plt.get_current_fig_manager()
    mng.resize(*mng.window.maxsize())

    # Show plot.
    plt.show()


# draw_round()
