#!/usr/bin/python
import log
# import scipy.ndimage
# import scipy.signal
# import numpy as np


def add_relative_time(data):
    t0 = max([e.get('time') for e in data])
    for e in data:
        e['relative_time_sec'] = float((t0 - e['time']).total_seconds())
    return data


def add_virtual_time(samples, threshold_sec):
    virtual_time = 0
    n = len(samples)
    sequence_id = 0
    for i in xrange(0, n):
        curr = samples[i]
        if i > 0:
            prev = samples[i - 1]
            t1 = prev['relative_time_sec']
            t2 = curr['relative_time_sec']
            delta = t2 - t1
            is_overtime = delta >= threshold_sec
            is_status_changed = curr['status'] != prev['status']
            if not is_overtime and not is_status_changed:
                virtual_time += delta
            else:
                sequence_id += 1
        curr['virtual_time_hour'] = virtual_time/(60*60)
        curr['sequence_id'] = sequence_id
    return samples


# def smooth_virtual_time(samples):
#     chunks = separate_by_sequence_id(samples)
#     k = 5
#     modes = ['reflect', 'constant', 'nearest', 'mirror', 'wrap']
#     for chunk in chunks:
#         ys = [x['capacity'] for x in chunk]
#         #xs = [x['virtual_time_hour'] for x in chunk]
#         ys2 = scipy.ndimage.gaussian_filter(ys, k)
#         #ys2 = scipy.signal.savgol_filter(ys, k, 2)
#         n = len(ys2)
#         if n < 2*k:
#             continue
#         for i in xrange(0, n):
#             e = chunk[i]
#             e['capacity_raw'] = e['capacity']
#             e['capacity'] = ys2[i]
#     return [item for sublist in chunks for item in sublist]


def separate_by_sequence_id(samples):
    result = []
    chunk = []
    prev = None
    for curr in samples:
        if prev is not None:
            if curr['sequence_id'] != prev['sequence_id']:
                result.append(chunk)
                chunk = []
        chunk.append(curr)
        prev = curr
    result.append(chunk)
    return result


def extract_plot_data(batch):
    status = None if len(batch) == 0 else batch[0].get('status')
    xs = filter(
        lambda x: x is not None, [e.get('virtual_time_hour') for e in batch])
    ys = filter(
        lambda x: x is not None, [e.get('capacity') for e in batch])
    return {
        'status': status,
        'xs': xs,
        'ys': ys
    }


class History:

    def __init__(self, log_data=[], threshold_sec=15*60):
        data = add_relative_time(log_data)
        data = sorted(data, key=lambda e: e['relative_time_sec'])
        data = add_virtual_time(data, threshold_sec)
        #data = smooth_virtual_time(data)
        self._data = data
        self._plot_data = []
        self._plot_xoffset = 0
        self._plot_xlimit = 12.0

    def data(self):
        return self._data

    def set_plot_data_xoffset(self, xoffset):
        self._plot_xoffset = xoffset

    def set_plot_data_xlimit(self, hours):
        self._plot_xlimit = hours

    def get_recent_history(self, limit):
        data = filter(lambda d: d['virtual_time_hour'] < limit, self._data)
        return data

    def calculate_plot_data(self):
        limit = self._plot_xlimit - self._plot_xoffset
        data = self.get_recent_history(limit)
        # shift
        for e in data:
            e['virtual_time_hour'] += self._plot_xoffset
        data = separate_by_sequence_id(data)
        # exptract plot data
        self._plot_data = [extract_plot_data(batch) for batch in data]

    def plot_data(self, status):
        return [x for x in self._plot_data if x.get('status') in status]
