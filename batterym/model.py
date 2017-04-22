#!/usr/bin/python
import mathstat

# statistic model
# - split charge/discharge
# - extract slopes by capacity bins
# - pick up slopes curve (by percentile)
# - reconstruct (dis)charging capacity timeline (start value)


def get_slopes_capacity_bins(data):
    bins = {}
    for e in data:
        key = e.get('capacity_round')
        val = e.get('slope', 0)
        if key is not None and not mathstat.is_zero(val):
            bins.setdefault(key, []).append(v)
    return bins


def get_slopes_by_percentile(bins, percentile_val):
    x = bins.keys()
    y = [mathstat.percentile(bins[i], percentile_val) for i in x]
    return dict(zip(x, y))


def reconstruct_timeline(slopes):
    y2 = range(10, 101, 1)
    #y2 = range(100, 10, -1)
    x2 = [0]
    for i in xrange(1, len(y2)):
        dy = y2[i] - y2[i-1]
        sl = new_slopes[y2[i-1]]
        dx = dy / sl
        x = x2[i-1] + dx
        x2.append(x)
