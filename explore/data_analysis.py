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


logs = log.get_battery('../logs/capacity_example')
data = pd.DataFrame(logs)
data = data.rename(columns={'time': 'timestamp'})
data['date'] = pd.Series(data['timestamp'].dt.date)
data['time'] = pd.Series(data['timestamp'].dt.time)


print data.head()
