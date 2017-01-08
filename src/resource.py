#!/usr/bin/python
import os


IMAGE_FOLDER = 'res/'


def image_path(name, theme):
    return os.path.abspath(os.path.join(IMAGE_FOLDER, theme, name))


def icon_file_charging(capacity):
    filename = 'battery-charging-'
    if capacity >= 100:
        filename += '100'
    elif capacity >= 90:
        filename += '90'
    elif capacity >= 80:
        filename += '80'
    elif capacity >= 60:
        filename += '60'
    elif capacity >= 40:
        filename += '40'
    else:
        filename += '20'
    filename += '.png'
    return filename


def icon_file_no_charging(capacity):
    filename = 'battery-'
    if capacity >= 100:
        filename += '100'
    elif capacity >= 90:
        filename += '90'
    elif capacity >= 80:
        filename += '80'
    elif capacity >= 70:
        filename += '70'
    elif capacity >= 60:
        filename += '60'
    elif capacity >= 50:
        filename += '50'
    elif capacity >= 40:
        filename += '40'
    elif capacity >= 30:
        filename += '30'
    elif capacity >= 20:
        filename += '20'
    elif capacity >= 10:
        filename += '10'
    else:
        filename += '0'
    filename += '.png'
    return filename


def icon_filename(capacity, is_charging):
    if is_charging:
        return icon_file_charging(capacity)
    return icon_file_no_charging(capacity)


def icon_path(capacity, is_charging, theme):
    return image_path(icon_filename(capacity, is_charging), theme)
