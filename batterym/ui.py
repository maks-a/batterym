#!/usr/bin/python
from batterym import config
import unittest


THEME_DARK = 'dark'
THEME_LIGHT = 'light'


def set_theme(theme):
    config.set_entry('theme', theme)


def get_theme():
    return config.get_entry('theme', default_value=THEME_DARK)


def reset_theme():
    set_theme(THEME_DARK)


def toggle_theme():
    if get_theme() == THEME_DARK:
        set_theme(THEME_LIGHT)
    elif get_theme() == THEME_LIGHT:
        set_theme(THEME_DARK)


class MyTest(unittest.TestCase):

    def setUp(self):
        self.theme = get_theme()

    def tearDown(self):
        set_theme(self.theme)

    def test_set_and_get_theme(self):
        set_theme(THEME_LIGHT)
        self.assertEqual(get_theme(), THEME_LIGHT)

        set_theme(THEME_DARK)
        self.assertEqual(get_theme(), THEME_DARK)

    def test_reset_theme(self):
        set_theme(THEME_LIGHT)
        reset_theme()
        self.assertEqual(get_theme(), THEME_DARK)

    def test_toggle_theme(self):
        set_theme(THEME_DARK)
        toggle_theme()
        self.assertEqual(get_theme(), THEME_LIGHT)

        set_theme(THEME_LIGHT)
        toggle_theme()
        self.assertEqual(get_theme(), THEME_DARK)
