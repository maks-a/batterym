#!/usr/bin/python
import signal
from indicator import Indicator
import unittest


def run():
    signal.signal(signal.SIGINT, signal.SIG_DFL)
    Indicator().run_forever()


if __name__ == "__main__":
    run()
