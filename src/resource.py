#!/usr/bin/python
import os


IMAGE_FOLDER_PATTERN = '/usr/share/icons/ubuntu-mono-{0}/status/22'


def image_path(name, theme):
    folder = IMAGE_FOLDER_PATTERN.format(theme)
    return os.path.abspath(os.path.join(folder, name))


def icon_filename(capacity, is_charging):
    filename = 'battery-'
    if capacity >= 100:
        filename += '100'
    elif capacity >= 80:
        filename += '080'
    elif capacity >= 60:
        filename += '060'
    elif capacity >= 40:
        filename += '040'
    elif capacity >= 20:
        filename += '020'
    else:
        filename += '000'
    if is_charging:
        filename += '-charging'
    filename += '.svg'
    return filename


def icon_path(capacity, is_charging, theme):
    return image_path(icon_filename(capacity, is_charging), theme)
