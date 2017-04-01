#!/usr/bin/python
import os
from distutils.core import setup
from batterym.resource import RESOURCES_DIRECTORY_PATH


def find_resources(resource_dir):
    target_path = os.path.join(RESOURCES_DIRECTORY_PATH, resource_dir)
    resource_names = os.listdir(resource_dir)
    resource_list = [os.path.join(resource_dir, file_name)
                     for file_name in resource_names]
    return (target_path, resource_list)


def chmod(folder, mod):
    files = os.listdir(folder)
    for fname in files:
        if not os.path.isfile(fname) :
            continue
        os.chmod(fname, mod)


setup(name='batterym',
      version='0.1.0',
      description='Battery Monitor for Ubuntu',
      url='',
      author='',
      author_email='',
      license='',
      packages=['batterym'],
      data_files=[
          ('/usr/share/applications', ['batterym.desktop']),
          (find_resources('logs')),
          (find_resources('img'))
      ],
      scripts=['bin/batterym']
      )


chmod(os.path.join(RESOURCES_DIRECTORY_PATH, 'logs'), 0777)
chmod(os.path.join(RESOURCES_DIRECTORY_PATH, 'img'), 0777)
