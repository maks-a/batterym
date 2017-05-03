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
import mathstat


def get_data():
    # logs = log.get_battery()
    logs = log.get_battery('../logs/capacity_example')
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
    return zip(*res)


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
    y_min = min(charge_cap_slopes[0])
    y_max = max(charge_cap_slopes[0])
    x, y = charge_reconstructed_ext
    c = zip(x, y)
    c = filter(lambda e: is_within(e[1], y_min, y_max), c)
    charge_reconstructed = zip(*c)

    ys2 = range(0, 100, 1)
    discharge_reconstructed_ext = reconstruct_timeline(
        discharge_cap_slopes_ext, ys2)
    y_min = min(discharge_cap_slopes[0])
    y_max = max(discharge_cap_slopes[0])
    x, y = discharge_reconstructed_ext
    c = zip(x, y)
    c = filter(lambda e: is_within(e[1], y_min, y_max), c)
    discharge_reconstructed = zip(*c)

    # # extract slopes by capacity bins
    # charge_bins = model.get_slopes_capacity_bins(charge)
    # discharge_bins = model.get_slopes_capacity_bins(discharge)
    # # pick up slopes curve (by percentile)
    # p = percentile
    # charge_slopes = model.get_slopes_by_percentile(charge_bins, p)
    # charge_slopes = model.extrapolate(charge_slopes, 0, 100)
    # discharge_slopes = model.get_slopes_by_percentile(discharge_bins, p)
    # discharge_slopes = model.extrapolate(discharge_slopes, 0, 100)
    # # reconstruct (dis)charging capacity timeline
    # ys1 = range(100, 0, -1)
    # charge_timeline_total = model.reconstruct_timeline(charge_slopes, ys1)
    # ys2 = range(0, 100)
    # discharge_timeline_total = model.reconstruct_timeline(
    #     discharge_slopes, ys2)
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
    fig, ax = plt.subplots(4)

    # Capacity timeline chart.
    df = pd.DataFrame(d['discharge'])
    x = df['virtual_time_hour'].values
    y = df['capacity'].values
    line1 = ax[0].plot(x, y, color='r', marker='o')
    ax[0].set_ylim(0, 105)
    ax[0].invert_xaxis()
    ax[0].set_title('timeline')
    ax[0].set_xlabel('past virtual time, hour')
    ax[0].set_ylabel('capacity, %')

    # Slope vs capacity, original and extended.
    x, y = d['discharge_cap_slopes_ext']
    line2 = ax[1].plot(x, y, color='r', marker='x', label='extended')
    x, y = d['discharge_cap_slopes']
    line3 = ax[1].plot(x, y, color='b', marker='o', label='original')
    ax[1].set_title('slope vs capacity')
    ax[1].set_xlabel('capacity, %')
    ax[1].set_ylabel('slope')

    # Reconstructed timeline, original and extended.
    x, y = d['discharge_reconstructed_ext']
    ax[2].plot(x, y, color='r', marker='x', label='extended')
    x, y = d['discharge_reconstructed']
    ax[2].plot(x, y, color='b', marker='o', label='original')
    ax[2].set_ylim(0, 101)
    ax[2].set_title('reconstructed timeline')
    ax[2].set_xlabel('time, hour')
    ax[2].set_ylabel('capacity, %')
    ax[2].invert_xaxis()

    # Battery life timeline.
    x, y = [], []
    ax[3].plot(x, y, color='r', marker='x')
    ax[3].set_title('battery life timeline')
    ax[3].set_xlabel('reversed virtual time, hour')
    ax[3].set_ylabel('capacity, %')

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
