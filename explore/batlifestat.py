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
import model
import smooth
import history


def get_data():
    # logs = log.get_battery()
    logs = log.get_battery('../logs/capacity_example')
    h = history.History(logs, smoothing=True)
    hdata = h.data()

    data = pd.DataFrame(hdata)
    data['timestamp'] = data['time']
    data = data.sort_values(by='timestamp', ascending=True)

    # Extract charging sessions
    data = data[data['status'] == 'Discharging']

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


def calculate(hdata):
    percentile = 0.5
    history_limit = 1000.0

    # split charge/discharge
    hdata = filter(lambda e: e['virtual_time_hour'] < history_limit, hdata)
    charge = filter(lambda e: e['status'] == 'Charging', hdata)
    discharge = filter(lambda e: e['status'] == 'Discharging', hdata)
    # extract slopes by capacity bins
    charge_bins = model.get_slopes_capacity_bins(charge)
    discharge_bins = model.get_slopes_capacity_bins(discharge)
    # pick up slopes curve (by percentile)
    p = percentile
    charge_slopes = model.get_slopes_by_percentile(charge_bins, p)
    charge_slopes = model.extrapolate(charge_slopes, 0, 100)
    discharge_slopes = model.get_slopes_by_percentile(discharge_bins, p)
    discharge_slopes = model.extrapolate(discharge_slopes, 0, 100)
    # reconstruct (dis)charging capacity timeline
    ys1 = range(100, 0, -1)
    charge_timeline_total = model.reconstruct_timeline(charge_slopes, ys1)
    ys2 = range(0, 100)
    discharge_timeline_total = model.reconstruct_timeline(discharge_slopes, ys2)


def battery_life_statistic(data):
    h = history.History(data, smoothing=True)
    calculate(h.data())

    plt.style.use('ggplot')
    fig, ax = plt.subplots(3)

    # Capacity timeline chart.
    x = [0, 0.3, 0.6, 1]
    y = [65, 60, 50, 20]
    ax[0].plot(x, y, color='r', marker='o', label='timeline')
    ax[0].set_ylim(0, 101)

    # Slope bins, original and extended.
    x = [50, 60, 40, 30, 70, 80]
    y = [10, 20, 10, 10, 20, 20]
    ax[1].scatter(x, y, color='r', label='extended')
    x = [50, 60]
    y = [10, 20]
    ax[1].scatter(x, y, color='b', label='original')

    # Reconstructed timeline, original and extended
    x = [0, 0.3, 0.6, 1]
    y = [65, 60, 50, 20]
    ax[2].plot(x, y, color='r', marker='x', label='extended')
    x = [0.3, 0.6]
    y = [60, 50]
    ax[2].plot(x, y, color='b', marker='o', label='original')
    ax[2].set_ylim(0, 101)

    # Full screen plot window.
    mng = plt.get_current_fig_manager()
    mng.resize(*mng.window.maxsize())
    # Show plot.
    plt.show()
    # break


def main():
    data = get_data()
    battery_life_statistic(data)

if __name__ == '__main__':
    main()
