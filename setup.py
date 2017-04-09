#!/usr/bin/python
import os
from distutils.core import setup
from batterym.misc import create_missing_dirs
from batterym.paths import RESOURCES_DIRECTORY_PATH


def find_resources(resource_dir):
    target_path = os.path.join(RESOURCES_DIRECTORY_PATH, resource_dir)
    resource_names = os.listdir(resource_dir)
    resource_list = [os.path.join(resource_dir, file_name)
                     for file_name in resource_names]
    return (target_path, resource_list)


def chmod(folder, mod):
    files = os.listdir(folder)
    for fname in files:
        fname = os.path.join(folder, fname)
        if not os.path.isfile(fname) :
            continue
        os.chmod(fname, mod)
        print 'changing mode of {0} to {1}'.format(fname, mod)


setup(name='batterym',
      version='0.1.0',
      description='Battery Monitor for Ubuntu',
      url='https://github.com/maks-a/batterym',
      author='https://github.com/maks-a',
      license='Apache License 2.0',
      packages=['batterym'],
      data_files=[
          ('/usr/share/applications', ['batterym.desktop']),
          (find_resources('config')),
          (os.path.join(RESOURCES_DIRECTORY_PATH, 'logs'), []),
          (find_resources('img')),
      ],
      scripts=['bin/batterym']
      )

create_missing_dirs(os.path.join(RESOURCES_DIRECTORY_PATH, 'logs'))

capacity_log = os.path.join(RESOURCES_DIRECTORY_PATH, 'logs/capacity')
if not os.path.isfile(capacity_log):
    with open(capacity_log, 'w') as f:
        f.write('')

chmod(os.path.join(RESOURCES_DIRECTORY_PATH, 'config'), 0777)
chmod(os.path.join(RESOURCES_DIRECTORY_PATH, 'logs'), 0777)
chmod(os.path.join(RESOURCES_DIRECTORY_PATH, 'img'), 0777)
