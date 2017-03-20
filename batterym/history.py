#!/usr/bin/python
import log
#import unittest


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


# def running_mean(l, N):
#     sum = 0
#     result = [0 for x in l]

#     k = len(l)
#     N = min(k, N)
#     for i in xrange(0, N):
#         sum += l[i]
#         result[i] = sum / (i+1)

#     for i in range(N, k):
#         sum = sum - l[i-N] + l[i]
#         result[i] = sum / N

#     return result


# def my_filter(a, w):
#     n = len(a)
#     k = int((w-1) / 2)
#     result = [0 for x in a]
#     for i in xrange(0, n):
#         l = max(0, i-k)
#         r = min(n-1, i+k)
#         d = min(i-l, r-i)
#         result[i] = float(a[i-d] + a[i+d]) / 2.0

#     return result


# def my_filter2(a):
#     result = a[:]
#     n = len(result)
#     i = -1
#     while i < n:
#         i += 1
#         for j in xrange(i+1, n):
#             if a[i] == a[j]:
#                 continue
#             if j-i > 1:
#                 for k in xrange(i, j):
#                     t = (k-i) / (1.0*(j-i))
#                     result[k] = (1-t)*a[i] + t*a[j]
#                 result[j-1] = a[j]
#             i = j-1
#             break
#     return result


# def find_duplicate_idxs(a):
#     result = []
#     n = len(a)
#     i = -1
#     while i < n:
#         i += 1
#         for j in xrange(i+1, n):
#             if a[i] == a[j]:
#                 continue
#             if j-i > 1:
#                 for k in xrange(i+1, j):
#                     result.append(k)
#             i = j-1
#             break
#     return result


def smooth_virtual_time(samples):
    return samples
#     chunks = separate_by_sequence_id(samples)
#     k = len(chunks)
#     for j in xrange(0, k):
#         chunk = chunks[j]
#         ys = [x['capacity'] for x in chunk]
#         idxs = find_duplicate_idxs(ys)
#         # ys.reverse()
#         # ys = my_filter2(ys)
#         #ys = my_filter2(ys)
#         # ys.reverse()
#         #ys = my_filter(ys, 9)
#         # ys = my_filter(ys, 9)
#         #ys = running_mean(ys, 3)
#         new_chunk = []
#         n = len(chunk)
#         for i in xrange(0, n):
#             if i not in idxs:
#                 new_chunk.append(chunk[i])
#         chunks[j] = new_chunk

#         # chunk = chunks[j]
#         # ys = [x['capacity'] for x in chunk]
#         # ys = my_filter(ys, 5)
#         # n = len(ys)
#         # for i in xrange(0, n):
#         #     e = chunk[i]
#         #     e['capacity_raw'] = e['capacity']
#         #     e['capacity'] = ys[i]
#         # chunks[j] = chunk

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

    def __init__(self, log_data=[], threshold_sec=15*60, smoothing=False):
        data = add_relative_time(log_data)
        data = sorted(data, key=lambda e: e['relative_time_sec'])
        data = add_virtual_time(data, threshold_sec)
        if smoothing:
            data = smooth_virtual_time(data)
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


def main():
    image_path = 'capacity_history_12h.svg'

    history1 = History(log.get_battery())
    history1.set_plot_data_xlimit(hours=12.0)
    history1.calculate_plot_data()
    plot_data1 = {
        'history charging': history1.plot_data(['Charging', 'Full']),
        'history discharging': history1.plot_data(['Discharging']),
    }

    history2 = History(log.get_battery(), smoothing=True)
    history2.set_plot_data_xlimit(hours=12.0)
    history2.calculate_plot_data()
    plot_data2 = {
        'history charging': history2.plot_data(['Charging', 'Full']),
        'history discharging': history2.plot_data(['Discharging']),
    }

    white = '#fff'
    red = '#f00'
    blue = '#2e7eb3'
    light_blue = '#8cc'
    green = '#4aa635'
    light_green = '#8c8'
    ylabels = ['0 %', '25 %', '50 %', '75%', '100 %']
    xlabels = [0, 2, 4, 6, 8, 10, '12 hours']

    from chart import Chart
    plot = Chart(xlabels=xlabels, ylabels=ylabels,
                 inverseX=True, padding_top=30, height=450)
    plot.set_minimal_canvas([0, 0], [12, 100])

    for p in plot_data1['history charging']:
        plot.add(xs=p['xs'], ys=p['ys'], stroke=light_green, fill=light_green,
                 drop=white)

    for p in plot_data1['history discharging']:
        plot.add(xs=p['xs'], ys=p['ys'], stroke=light_blue, fill=light_blue,
                 drop=white)

    for p in plot_data2['history charging']:
        plot.add(xs=p['xs'], ys=p['ys'], stroke=red)

    for p in plot_data2['history discharging']:
        plot.add(xs=p['xs'], ys=p['ys'], stroke=red)

    plot.render_to_svg(image_path)


# class TestStringMethods(unittest.TestCase):

#     def test_my_filter2(self):
#         self.assertEqual(my_filter2([]), [])
#         self.assertEqual(my_filter2([1]), [1])
#         self.assertEqual(my_filter2([1, 2]), [1, 2])
#         self.assertEqual(my_filter2([1, 2, 3]), [1, 2, 3])
#         self.assertEqual(my_filter2([1, 1, 3]), [1, 2, 3])
#         self.assertEqual(my_filter2([1, 1, 3, 3]), [1, 2, 3, 3])
#         self.assertEqual(my_filter2([1, 1, 3, 3, 5]), [1, 2, 3, 4, 5])
#         self.assertEqual(my_filter2([1, 1, 2, 2, 3]), [1, 1.5, 2, 2.5, 3])


if __name__ == '__main__':
    #main()
    #unittest.main()
    pass
