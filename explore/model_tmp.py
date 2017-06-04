#!/usr/bin/python
import unittest

"""
TODO:
- battery life comparison for different models (linear, statistical, etc.)
- generic battery model API


- estimate current charge/discharge time-to-end
    - overwrite & extend slopes
    - in=[history, charge/discharge], out=time

- predict future charge/discharge time-to-end curve
    - tangental
    - statistical (slopes)

"""

class BatteryModel:

    def __init__(self, history):
        pass

    def calculate(self):
        pass

    def get_life_timeline(self, time_range):
        pass


class MyTest(unittest.TestCase):

    def test_tmp(self):
        pass
