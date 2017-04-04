#!/usr/bin/python
import unittest

THEME_DARK = 'dark'
THEME_LIGHT = 'light'

THEME = THEME_DARK


def set_theme(theme):
    global THEME
    THEME = theme


def get_theme():
    return THEME


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
