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


def get_capacity_slopes(data, default_slopes=None):
    d = {}
    if default_slopes is not None:
        x, y = default_slopes
        d = dict(zip(x, y))
    for e in data:
        key = e.get('capacity_round')
        val = e.get('slope', 0)
        if key is not None and not mathstat.is_zero(val):
            d[key] = val
    x = d.keys()
    y = d.values()
    return x, y


def extrapolate(data):
    x, y = data
    res = model.extrapolate(dict(zip(x, y)))
    if len(res) > 0:
        x = res.keys()
        y = res.values()
        return x, y
    return [], []


def reconstruct_timeline(slopes, ys):
    x, y = slopes
    d = dict(zip(x, y))
    res = model.reconstruct_timeline(d, ys)
    x2 = y2 = []
    if 0 < len(res):
        x2, y2 = zip(*res)
    return x2, y2


def get_battery_life(data, ys):
    data = sorted(data, key=lambda e: e['timestamp'])
    slopes = None
    i = -1
    for e in data:
        i += 1
        slopes = get_capacity_slopes([e], slopes)
        extended = extrapolate(slopes)
        reconstructed = reconstruct_timeline(extended, ys)
        t = None
        xs = reconstructed[0]
        if 2 < len(xs):
            x_min = min(reconstructed[0])
            x_max = max(reconstructed[0])
            dx = x_max - x_min
            if 0 < dx:
                t = dx
        e['battery_life_hour'] = t
    return data


def calculate(hdata):
    percentile = 0.5
    history_limit = 1000.0

    # split charge/discharge
    hdata = filter(lambda e: e['virtual_time_hour'] < history_limit, hdata)
    charge = filter(lambda e: e['status'] == 'Charging', hdata)
    discharge = filter(lambda e: e['status'] == 'Discharging', hdata)
    # extract capacity slopes
    charge_cap_slopes = get_capacity_slopes(charge)
    discharge_cap_slopes = get_capacity_slopes(discharge)

    charge_cap_slopes_ext = extrapolate(charge_cap_slopes)
    discharge_cap_slopes_ext = extrapolate(discharge_cap_slopes)

    ys1 = range(100, 0, -1)
    charge_reconstructed_ext = reconstruct_timeline(
        charge_cap_slopes_ext, ys1)
    ys = charge_cap_slopes[0]
    if 0 < len(ys):
        y_min = min(ys)
        y_max = max(ys)
        x, y = charge_reconstructed_ext
        c = zip(x, y)
        c = filter(lambda e: is_within(e[1], y_min, y_max), c)
        charge_reconstructed = zip(*c)

    ys2 = range(0, 100, 1)
    discharge_reconstructed_ext = reconstruct_timeline(
        discharge_cap_slopes_ext, ys2)
    ys = discharge_cap_slopes[0]
    if 0 < len(ys):
        y_min = min(discharge_cap_slopes[0])
        y_max = max(discharge_cap_slopes[0])
        x, y = discharge_reconstructed_ext
        c = zip(x, y)
        c = filter(lambda e: is_within(e[1], y_min, y_max), c)
        discharge_reconstructed = zip(*c)

    charge = get_battery_life(charge, ys1)
    discharge = get_battery_life(discharge, ys2)

    return {
        # 'charge': charge,
        # 'charge_cap_slopes': charge_cap_slopes,
        # 'charge_cap_slopes_ext': charge_cap_slopes_ext,
        # 'charge_reconstructed': charge_reconstructed,
        # 'charge_reconstructed_ext': charge_reconstructed_ext,

        'discharge': discharge,
        'discharge_cap_slopes': discharge_cap_slopes,
        'discharge_cap_slopes_ext': discharge_cap_slopes_ext,
        'discharge_reconstructed': discharge_reconstructed,
        'discharge_reconstructed_ext': discharge_reconstructed_ext,
    }


def is_within(val, lo, hi):
    return lo <= val and val <= hi


def battery_life_statistic(data):
    h = history.History(data, smoothing=True)
    vt_min = 0.0
    vt_max = 1000.0
    hdata = h.data()
    hdata = filter(
        lambda e: is_within(e['virtual_time_hour'], vt_min, vt_max),
        hdata)
    d = calculate(hdata)

    plt.style.use('ggplot')
    fig, ax = plt.subplots(3, 2)

    # Capacity timeline chart.
    df = pd.DataFrame(d['discharge'])
    x = df['virtual_time_hour'].values
    y = df['capacity'].values
    line1 = ax[0][0].plot(x, y, color='r', marker='x')
    ax[0][0].set_ylim(0, 105)
    ax[0][0].invert_xaxis()
    ax[0][0].set_title('timeline')
    ax[0][0].set_xlabel('past virtual time, hour')
    ax[0][0].set_ylabel('capacity, %')

    # Slope vs capacity, original and extended.
    x, y = d['discharge_cap_slopes_ext']
    line2 = ax[0][1].plot(x, y, color='r', marker='x', label='extended')
    x, y = d['discharge_cap_slopes']
    line3 = ax[0][1].plot(x, y, color='b', marker='o', label='original')
    ax[0][1].set_title('slope vs capacity')
    ax[0][1].set_xlabel('capacity, %')
    ax[0][1].set_ylabel('slope')

    # Reconstructed timeline, original and extended.
    x, y = d['discharge_reconstructed_ext']
    ax[1][1].plot(x, y, color='r', marker='x', label='extended')
    x, y = d['discharge_reconstructed']
    ax[1][1].plot(x, y, color='b', marker='o', label='original')
    ax[1][1].set_ylim(0, 101)
    ax[1][1].set_title('reconstructed timeline')
    ax[1][1].set_xlabel('time, hour')
    ax[1][1].set_ylabel('capacity, %')
    ax[1][1].invert_xaxis()

    # Battery life timeline.
    x = df['virtual_time_hour'].values
    y = df['battery_life_hour'].values
    ax[1][0].plot(x, y, color='r', marker='+')
    ax[1][0].set_title('battery life timeline')
    ax[1][0].set_xlabel('reversed virtual time, hour')
    ax[1][0].set_ylabel('capacity, %')
    ax[1][0].invert_xaxis()

    # Battery life timeline histogram.
    y = df['battery_life_hour'].values
    y = [e for e in y if 0 < e]
    # y2 = sorted(y)
    # n = len(y2)
    # k = int(0.1 * n)
    # y2 = y2[k:-k]
    ax[2][0].hist(y, bins=50, normed=1, color='r')
    #ax[2][0].hist(y2, bins=50, normed=1, color='b')
    ax[2][0].set_title('battery life timeline')
    ax[2][0].set_xlabel('reversed virtual time, hour')
    ax[2][0].set_ylabel('capacity, %')

    # Legend.
    fig.tight_layout()
    # Full screen plot window.
    mng = plt.get_current_fig_manager()
    mng.resize(*mng.window.maxsize())
    # Show plot.
    plt.show()


def main():
    data = get_data()
    battery_life_statistic(data)

if __name__ == '__main__':
    main()
