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
import paths
import model
import smooth
import history
import mathstat


def get_data():
    logs = log.get_battery(paths.LOG_BATTERY_ALL_FILE)
    # logs = log.get_battery('../logs/capacity_example')
    h = history.History(logs, smoothing=True)
    hdata = h.data()

    data = pd.DataFrame(hdata)
    data['timestamp'] = data['time']
    data = data.sort_values(by='timestamp', ascending=True)

    # Extract charging sessions
    # data = data[data['status'] == 'Discharging']

    # Group by sequence_id
    # grouped = data.groupby('sequence_id')['capacity_raw'].max()
    # grouped = grouped[grouped.values >= 100]
    # data = data[data.sequence_id.isin(grouped.index)]

    # CAP_LOW = 70
    # grouped = data.groupby('sequence_id')['capacity_raw'].min()
    # grouped = grouped[grouped.values <= CAP_LOW]
    # data = data[data.sequence_id.isin(grouped.index)]
    # data = data[data['capacity_raw'] >= CAP_LOW]

    # grouped = data.groupby('sequence_id')['capacity_raw'].count()
    # grouped = grouped.sort_values(inplace=False, ascending=False)
    # grouped = grouped[:30]
    # data = data[data.sequence_id.isin(grouped.index)]

    return data.T.to_dict().values()


def sessions_len_statistic(data):
    h = history.History(data, smoothing=True)
    vt_min = 0.0
    vt_max = 1000.0
    hdata = h.data()
    hdata = filter(
        lambda e: mathstat.is_within(e['virtual_time_hour'], vt_min, vt_max),
        hdata)
    #d = calculate(hdata)

    plt.style.use('ggplot')
    fig, ax = plt.subplots(2, 2)

    # Capacity timeline chart.
    x = y = []
    line1 = ax[0][0].plot(x, y, color='r', marker='x')
    ax[0][0].set_ylim(0, 105)
    ax[0][0].invert_xaxis()
    ax[0][0].set_title('timeline')
    ax[0][0].set_xlabel('past virtual time, hour')
    ax[0][0].set_ylabel('capacity, %')

    # Session times histogram.
    y = []
    ax[1][0].hist(y, bins=50, normed=1, color='r')

    # Legend.
    fig.tight_layout()
    # Full screen plot window.
    mng = plt.get_current_fig_manager()
    mng.resize(*mng.window.maxsize())
    # Show plot.
    plt.show()


def main():
    data = get_data()
    sessions_len_statistic(data)


if __name__ == '__main__':
    main()
