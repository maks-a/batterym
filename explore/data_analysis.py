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


# Emulates the aesthetics of ggplot (a popular plotting package for R).
plt.style.use('ggplot')

logs = log.get_battery('../logs/capacity_example')
data = pd.DataFrame(logs)
data = data.rename(columns={'time': 'timestamp'})
data['date'] = pd.Series(data['timestamp'].dt.date)
data['time'] = pd.Series(data['timestamp'].dt.time)
data['weekday'] = pd.Series(data['timestamp'].dt.weekday)

# Add relative time.
most_recent_datetime = data['timestamp'].iloc[-1]
print 'Most recent time: ', most_recent_datetime
data['relative_time'] = pd.Series(most_recent_datetime - data['timestamp'])

print data.head()


# plt.figure()
# data['capacity'].plot()

# plt.figure()
# data['weekday'].hist(bins=7)

# plt.figure()
# data['capacity'].hist(bins=10)

# plt.figure()
# data['time'].hist(bins=24)

# plt.show()
