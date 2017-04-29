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

# logs = log.get_battery('../logs/capacity_example')
# h = history.History(logs, smoothing=True)
# hdata = h.data()

# data = pd.DataFrame(hdata)
# data = data.rename(columns={'time': 'timestamp'})
# data = data.sort_values(by='timestamp', ascending=True)

# # Extract charging sessions
# data = data[data['status'] == 'Charging']

# # Group by sequence_id
# # and leave the longest sessions 
# grouped = data.groupby('sequence_id')['capacity_raw'].size()
# grouped = grouped.sort_values(inplace=False, ascending=False)
# grouped = grouped[:3]
# data = data[data.sequence_id.isin(grouped.index)]

#print data

x = np.linspace(0, 10, 500)
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
