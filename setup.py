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
          ('/usr/share/batterym', ['batterym.desktop'])],
      scripts=["bin/batterym"]
      )
