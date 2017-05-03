#!/usr/bin/python
import pandas as pd
import numpy as np
import matplotlib
import datetime as dt

from matplotlib import pyplot as plt

# Import modules from /batterym/ folder.
import os
import sys
sys.path.append(os.path.abspath('../batterym'))
import log
import model
import smooth
import history


def battery_life_statistic():
    plt.style.use('ggplot')
    fig, ax = plt.subplots()

    # Full screen plot window.
    mng = plt.get_current_fig_manager()
    mng.resize(*mng.window.maxsize())
    # Show plot.
    plt.show()
    # break

def main():
    battery_life_statistic()

if __name__ == '__main__':
    main()
