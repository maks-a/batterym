#!/usr/bin/python

THEME_DARK = 'dark'
THEME_LIGHT = 'light'

THEME = THEME_DARK


def toggle_theme():
    global THEME
    if THEME == THEME_DARK:
        THEME = THEME_LIGHT
    elif THEME == THEME_LIGHT:
        THEME = THEME_DARK


def get_theme():
    return THEME
