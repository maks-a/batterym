#!/usr/bin/python
from os.path import join
from site import getuserbase


INSTALL_DIR = getuserbase()
SHARE_APP_DIR = join(INSTALL_DIR, 'share/applications')
RESOURCES_DIR = join(INSTALL_DIR, 'batterym')

CONFIG_DIR = join(RESOURCES_DIR, 'config')
LOGS_DIR = join(RESOURCES_DIR, 'logs')
IMAGE_DIR = join(RESOURCES_DIR, 'img')


CONFIG_DEFAULT_FILE = join(CONFIG_DIR, 'config_default.json')
CONFIG_USER_FILE = join(CONFIG_DIR, 'config_user.json')
LOG_BATTERY_FILE = join(LOGS_DIR, 'capacity')
LOG_BATTERY_ALL_FILE = join(LOGS_DIR, 'capacity_all')
BATTERY_MONITOR_ICON = join(IMAGE_DIR, 'battery.svg')
CAPACITY_HISTORY_CHART = join(IMAGE_DIR, 'capacity_history_12h.svg')


# External resources
IMAGE_FOLDER_PATTERN = '/usr/share/icons/ubuntu-mono-{0}/status/22'
