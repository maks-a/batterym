#!/usr/bin/python


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
<polyline points="0,0 50,0 150,100 250,100 300,150" 
    fill="rgb(0,249,249)" 
    stroke-width="0" 
    stroke="rgb(0,0,0)"/>
</svg>
"""

def main():
    chart = Line()
    chart.add([100, 95, 90, 60, 20, 20])
    chart.render_to_svg('test.svg')


if __name__ == '__main__':
    main()
