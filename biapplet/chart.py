#!/usr/bin/python
from __future__ import division


def color_to_rgb(color):
    table = {
        'white': (255, 255, 255),
        'black': (0, 0, 0)
    }
    return 'rgb{0}'.format(table[color])


def line_to_points(y):
    n = len(y)
    points = []
    for x in range(0, n):
        points.append([x, y[x]])
    return points


def is_closed(points):
    return points[0] == points[-1]


def close_polyline_by_x(points):
    if is_closed(points):
        return points
    x = points[-1][0]
    points.append([x, 0])
    points.append([0, 0])
    points.append(points[0])
    return points


def mirror_polyline_vertically(points):
    y_mx = max([p[1] for p in points])
    return [[p[0], y_mx - p[1]] for p in points]


def scale_polyline(polyline, f):
    return [[f[0]*p[0], f[1]*p[1]] for p in polyline]


def flat_coordinates(points):
    return [coord for p in points for coord in p]


class Line():

    def add(self, data):
        self.line = data

    def line_to_points(self):
        points = line_to_points(self.line)
        polyline = close_polyline_by_x(points)
        polyline = mirror_polyline_vertically(polyline)
        polyline = scale_polyline(polyline, [40, 1])
        coords = flat_coordinates(polyline)
        return coords

    def render_polyline(self):
        svg = '<polyline'
        points = ', '.join(map(str, self.line_to_points()))
        svg += ' points="{0}"'.format(points)
        svg += ' fill="{0}"'.format(color_to_rgb('white'))
        svg += ' stroke-width="{0}"'.format(0)
        svg += ' stroke="{0}"'.format(color_to_rgb('white'))
        svg += ' />'
        return svg

    def render(self):
        svg = []
        svg.append('<svg>')
        svg.append(self.render_polyline())
        svg.append('</svg>')
        return svg

    def render_to_svg(self, filepath):
        with open(filepath, 'w') as f:
            f.writelines(self.render())


"""
<svg>
<polyline
    points="0,0 50,0 150,100 250,100 300,150" 
    fill="rgb(0,249,249)" 
    stroke-width="0" 
    stroke="rgb(0,0,0)"
/>
</svg>
"""


def round_points(points):
    return [[int(p[0]), int(p[1])] for p in points]


def scale_points(points, k):
    return [[k[0]*p[0], k[1]*p[1]] for p in points]


def shift_points(points, offset):
    return [[p[0]+offset[0], p[1]+offset[1]] for p in points]


def get_square():
    return [[0, 0], [1, 0], [1, 1], [0, 1], [0, 0]]


def get_rectangular(w, h):
    return scale_points(get_square(), [w, h])


def get_color(text):
    t = {
        'white': '#fff',
        'black': '#000',
        'red': '#f00',
        'green': '#0f0',
        'blue': '#00f'
    }
    return t.get(text, text)


def tostr(point):
    return '({0}, {1})'.format(point[0], point[1])


class BoundingBox:

    def __init__(self):
        self.left_bottom = None
        self.right_top = None

    def __init__(self, point):
        self.left_bottom = point[:]
        self.right_top = point[:]

    def include(self, point):
        if self.left_bottom is None or self.right_top is None:
            self.left_bottom = point[:]
            self.right_top = point[:]
            return

        self.left_bottom[0] = min(self.left_bottom[0], point[0])
        self.left_bottom[1] = min(self.left_bottom[1], point[1])
        self.right_top[0] = max(self.right_top[0], point[0])
        self.right_top[1] = max(self.right_top[1], point[1])

    def width(self):
        return self.right_top[0] - self.left_bottom[0]

    def height(self):
        return self.right_top[1] - self.left_bottom[1]


class Chart:

    def __init__(self, width=650, height=75,
                 padding_top=10, padding_bottom=20,
                 padding_left=20, padding_right=40,
                 inverseX=False):
        self.width = width
        self.height = height
        self.padding_top = padding_top
        self.padding_bottom = padding_bottom
        self.padding_left = padding_left
        self.padding_right = padding_right
        self.inverseX = inverseX
        self.traces = []
        self.canvas = BoundingBox([0, 0])

        self.add_frame()  # TODO: remove
        self.add_background()
        self.add_axes()

    def add_frame(self):
        points = get_rectangular(self.width, self.height)
        data = {}
        data['points'] = points
        data['atr'] = {}
        data['atr']['fill'] = 'none'
        data['atr']['stroke-width'] = 1
        data['atr']['stroke'] = '#f00'
        self.traces.append(data)

    def add_background(self):
        w = self.width - self.padding_left - self.padding_right
        h = self.height - self.padding_top - self.padding_bottom
        points = get_rectangular(w, h)
        padding = [self.padding_left, self.padding_bottom]
        points = shift_points(points, padding)
        data = {}
        data['points'] = points
        data['atr'] = {}
        data['atr']['fill'] = get_color('white')
        self.traces.append(data)

    def add_axes(self):
        d = 5
        w = self.width - self.padding_left - self.padding_right
        h = self.height - self.padding_top - self.padding_bottom
        padding = [self.padding_left, self.padding_bottom]

        data = {}
        data['atr'] = {}
        data['atr']['fill'] = 'none'
        data['atr']['stroke-width'] = 0.5
        data['atr']['stroke'] = '#777'

        points = [[0, h], [w+d, h]]
        points = shift_points(points, padding)
        data['points'] = points
        self.traces.append(data)

        data = dict(data)
        points = [[0, 0], [w+d, 0]]
        points = shift_points(points, padding)
        data['points'] = points
        self.traces.append(data)

        data = dict(data)
        points = [[0, -d], [0, h]]
        points = shift_points(points, padding)
        data['points'] = points
        self.traces.append(data)

        data = dict(data)
        points = [[w, -d], [w, h]]
        points = shift_points(points, padding)
        data['points'] = points
        self.traces.append(data)

    def add(self, ys, xs=None, stroke_width=1, stroke='black'):
        ny = len(ys)
        if xs is None:
            xs = range(0, ny)
        n = min(len(xs), ny)
        xs = xs[:n]
        ys = ys[:n]

        points = []
        for i in xrange(0, n):
            point = [xs[i], ys[i]]
            points.append(point)
            self.canvas.include(point)

        data = {}
        data['canvas'] = points
        data['atr'] = {}
        data['atr']['fill'] = 'none'
        data['atr']['stroke-width'] = stroke_width
        data['atr']['stroke'] = get_color(stroke)
        self.traces.append(data)

    def canvas_to_points(self, canvas):
        w = self.width - self.padding_left - self.padding_right
        h = self.height - self.padding_top - self.padding_bottom
        xk = w / self.canvas.width()
        yk = h / self.canvas.height()

        if self.inverseX:
            canvas = shift_points(canvas, [-self.canvas.width(), 0])
            canvas = scale_points(canvas, [-1, 1])
        points = scale_points(canvas, [xk, yk])
        points = round_points(points)
        padding = [self.padding_left, self.padding_bottom]
        points = shift_points(points, padding)
        return points

    def render_points(self, points):
        points = shift_points(points, [0, -self.height])
        points = scale_points(points, [1, -1])

        coords = ['{0},{1}'.format(p[0], p[1]) for p in points]

        pts = ' '.join(coords)
        return '\tpoints="{0}"'.format(pts)

    def render_trace(self, trace):
        res = []
        res.append('<polyline')

        canvas = trace.get('canvas')
        if canvas:
            trace['points'] = self.canvas_to_points(canvas)

        points = trace.get('points')
        if points:
            res.append(self.render_points(points))

        atr = trace.get('atr')
        if atr:
            for a in atr:
                res.append('\t{0}=\"{1}\"'.format(a, atr[a]))

        res.append('/>')
        return res

    def render(self):
        svg = []
        svg.append('<svg>')
        for t in self.traces:
            svg.extend(self.render_trace(t))
        svg.append('</svg>')
        return svg

    def render_to_svg(self, filepath):
        with open(filepath, 'w') as f:
            lines = self.render()
            for line in lines:
                f.write(line + '\n')


def main():
    chart = Line()
    chart.add([100, 20, 30])
    chart.render_to_svg('test1.svg')

    chart = Chart(inverseX=True)
    ys = [100, 20, 30]
    import random
    ys = [random.randrange(0, 100) for i in xrange(200)]
    chart.add(ys)
    chart.render_to_svg('test.svg')


if __name__ == '__main__':
    main()
