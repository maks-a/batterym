#!/usr/bin/python
import os
from distutils.core import setup


setup(name="batterym",
      version="0.1.0",
      description="Battery Monitor for Ubuntu",
      url='',
      author='',
      author_email='',
      license='',
      packages=['batterym'],
      data_files=[
          ('/usr/share/batterym', ['batterym.desktop']),
          ('/var/lib/batterym/logs', ['logs/capacity'])
          ],
      scripts=["bin/batterym"]
      )

os.chmod('/var/lib/batterym/logs/capacity', 0777)
