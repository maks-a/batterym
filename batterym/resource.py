#!/usr/bin/python
import os
import unittest

from batterym import ui
from batterym.paths import IMAGE_FOLDER_PATTERN


def image_path(name, theme):
    folder = IMAGE_FOLDER_PATTERN.format(theme)
    return os.path.abspath(os.path.join(folder, name))


def icon_filename(capacity, is_charging):
    filename = 'battery-'
    if capacity >= 90:
        filename += '100'
    elif capacity >= 70:
        filename += '080'
    elif capacity >= 50:
        filename += '060'
    elif capacity >= 30:
        filename += '040'
    elif capacity >= 10:
        filename += '020'
    else:
        filename += '000'
    if is_charging:
        filename += '-charging'
    filename += '.svg'
    return filename


def icon_path(capacity, is_charging):
    return image_path(icon_filename(capacity, is_charging), ui.get_theme())


class MyTest(unittest.TestCase):

    def test_image_path(self):
        self.assertEqual(image_path('a.png', 'dark'),
                         '/usr/share/icons/ubuntu-mono-dark/status/22/a.png')
        self.assertEqual(image_path('a.png', 'light'),
                         '/usr/share/icons/ubuntu-mono-light/status/22/a.png')

    def test_icon_filename(self):
        self.assertEqual(icon_filename(100, False), 'battery-100.svg')
        self.assertEqual(icon_filename(90, False), 'battery-100.svg')
        self.assertEqual(icon_filename(80, False), 'battery-080.svg')
        self.assertEqual(icon_filename(70, False), 'battery-080.svg')
        self.assertEqual(icon_filename(60, False), 'battery-060.svg')
        self.assertEqual(icon_filename(50, False), 'battery-060.svg')
        self.assertEqual(icon_filename(40, False), 'battery-040.svg')
        self.assertEqual(icon_filename(30, False), 'battery-040.svg')
        self.assertEqual(icon_filename(20, False), 'battery-020.svg')
        self.assertEqual(icon_filename(10, False), 'battery-020.svg')
        self.assertEqual(icon_filename(0, False), 'battery-000.svg')

        self.assertEqual(icon_filename(100, True), 'battery-100-charging.svg')
        self.assertEqual(icon_filename(90, True), 'battery-100-charging.svg')
        self.assertEqual(icon_filename(80, True), 'battery-080-charging.svg')
        self.assertEqual(icon_filename(70, True), 'battery-080-charging.svg')
        self.assertEqual(icon_filename(60, True), 'battery-060-charging.svg')
        self.assertEqual(icon_filename(50, True), 'battery-060-charging.svg')
        self.assertEqual(icon_filename(40, True), 'battery-040-charging.svg')
        self.assertEqual(icon_filename(30, True), 'battery-040-charging.svg')
        self.assertEqual(icon_filename(20, True), 'battery-020-charging.svg')
        self.assertEqual(icon_filename(10, True), 'battery-020-charging.svg')
        self.assertEqual(icon_filename(0, True), 'battery-000-charging.svg')

    def test_icon_path(self):
        ui.reset_theme()
        self.assertEqual(icon_path(
            100, True),
            '/usr/share/icons/ubuntu-mono-dark/status/22/battery-100-charging.svg')

        ui.toggle_theme()
        self.assertEqual(icon_path(
            100, True),
            '/usr/share/icons/ubuntu-mono-light/status/22/battery-100-charging.svg')
