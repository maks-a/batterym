#!/usr/bin/python
import os
import ui
import unittest


IMAGE_FOLDER_PATTERN = '/usr/share/icons/ubuntu-mono-{0}/status/22'

RESOURCES_DIRECTORY_PATH = '/usr/share/batterym'


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
    return image_path(icon_filename(capacity, is_charging), ui.THEME)
