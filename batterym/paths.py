#!/usr/bin/python
import os


RESOURCES_DIRECTORY_PATH = '/usr/share/batterym'
IMAGE_FOLDER_PATTERN = '/usr/share/icons/ubuntu-mono-{0}/status/22'


CONFIG_FILE = os.path.join(RESOURCES_DIRECTORY_PATH, 'config/config.json')
LOG_BATTERY_FILE = os.path.join(RESOURCES_DIRECTORY_PATH, 'logs/capacity')

BATTERY_MONITOR_ICON = os.path.join(
    RESOURCES_DIRECTORY_PATH, 'img/battery.svg')
CAPACITY_HISTORY_CHART = os.path.join(
    RESOURCES_DIRECTORY_PATH, 'img/capacity_history_12h.svg')
