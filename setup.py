#!/usr/bin/python
import os
from distutils.core import setup

import batterym.fileio as fileio
import batterym.paths as paths
import batterym.config as config


def find_resources(folder):
    target_folder = os.path.join(paths.RESOURCES_DIR, folder)
    fnames = os.listdir(folder)
    resources = [os.path.join(folder, x) for x in fnames]
    return (target_folder, resources)


version = config.get_entry('version', 'config/config_default.json')
print('batterym v{0}'.format(version))
print('installation path:', paths.RESOURCES_DIR)

setup(name='batterym',
      version=version,
      description='Battery Monitor for Ubuntu',
      url='https://github.com/maks-a/batterym',
      author='https://github.com/maks-a',
      license='Apache License 2.0',
      packages=['batterym'],
      data_files=[
          (paths.SHARE_APP_DIR, ['batterym.desktop']),
          (paths.RESOURCES_DIR, []),
          (find_resources('config')),
          (paths.LOGS_DIR, []),
          (find_resources('img')),
      ],
      scripts=['bin/batterym']
      )

fileio.create_missing_dirs(paths.LOGS_DIR)
fileio.append('', paths.LOG_BATTERY_FILE)
fileio.append('', paths.LOG_BATTERY_ALL_FILE)

print('batterym is successfully installed.')
