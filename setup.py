#!/usr/bin/python
import os
from distutils.core import setup
from batterym.config import get_entry
from batterym.misc import append_to_file
from batterym.misc import create_missing_dirs

from batterym.paths import SHARE_APP_DIR
from batterym.paths import RESOURCES_DIR
from batterym.paths import CONFIG_DIR
from batterym.paths import LOGS_DIR
from batterym.paths import IMAGE_DIR
from batterym.paths import LOG_BATTERY_FILE
from batterym.paths import LOG_BATTERY_ALL_FILE


def find_resources(resource_dir):
    target_path = os.path.join(RESOURCES_DIR, resource_dir)
    resource_names = os.listdir(resource_dir)
    resource_list = [os.path.join(resource_dir, file_name)
                     for file_name in resource_names]
    return (target_path, resource_list)


version = get_entry('version', 'config/config.json')
print 'batterym v{0}'.format(version)
print 'installation path:', RESOURCES_DIR

setup(name='batterym',
      version=version,
      description='Battery Monitor for Ubuntu',
      url='https://github.com/maks-a/batterym',
      author='https://github.com/maks-a',
      license='Apache License 2.0',
      packages=['batterym'],
      data_files=[
          (SHARE_APP_DIR, ['batterym.desktop']),
          (find_resources('config')),
          (LOGS_DIR, []),
          (find_resources('img')),
      ],
      scripts=['bin/batterym']
      )

create_missing_dirs(LOGS_DIR)
append_to_file('', LOG_BATTERY_FILE)
append_to_file('', LOG_BATTERY_ALL_FILE)
