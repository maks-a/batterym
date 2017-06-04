#!/usr/bin/python


def round_prediction(minutes):
    minutes = int(minutes)
    if minutes <= 60:
        tol = 1
    elif minutes <= 180:
        tol = 5
    elif minutes <= 270:
        tol = 10
    else:
        tol = 15
    minutes -= minutes % tol
    return int(minutes)


def to_hhmm(minutes):
    h = minutes / 60
    m = minutes % 60
    if h == 0:
        return '{0}m'.format(m)
    if m == 0:
        return '{0}h'.format(h)
    return '{0}h{1}m'.format(h, m)


def main():
    for m in xrange(1, 600, 1):
        r = round_prediction(m)
        err = 100*abs(m-r)/m
        m = to_hhmm(m)
        r = to_hhmm(r)
        # print '{0} rounded to {1} with error {2}%'.format(m, r, err)
        print err

if __name__ == '__main__':
    main()
