#!/usr/bin/python
import os
from distutils.core import setup


setup(name="biapplet",
      version="0.1.0",
      description="Battery Indicator Application for Ubuntu",
      url='',
      author='',
      author_email='',
      license='',
      packages=[''],
      data_files=[
          ('/usr/share/batterym', ['biapplet.desktop'])],
      scripts=["biapplet/biapplet.py"]
      )
