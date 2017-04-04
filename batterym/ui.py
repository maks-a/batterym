#!/usr/bin/python
import unittest

THEME_DARK = 'dark'
THEME_LIGHT = 'light'

THEME = THEME_DARK


def reset_theme():
    global THEME
    THEME = THEME_DARK


def toggle_theme():
    global THEME
    if THEME == THEME_DARK:
        THEME = THEME_LIGHT
    elif THEME == THEME_LIGHT:
        THEME = THEME_DARK


def get_theme():
    return THEME


class MyTest(unittest.TestCase):

    def test_reset_theme(self):
        reset_theme()
        self.assertEqual(get_theme(), THEME_DARK)

        toggle_theme()
        reset_theme()
        self.assertEqual(get_theme(), THEME_DARK)

    def test_toggle_theme(self):
        reset_theme()

        toggle_theme()
        self.assertEqual(get_theme(), THEME_LIGHT)

        toggle_theme()
        self.assertEqual(get_theme(), THEME_DARK)
