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
    fig, ax = plt.subplots(3)

    # Capacity timeline chart.
    x = [0, 0.3, 0.6, 1]
    y = [65, 60, 50, 20]
    ax[0].plot(x, y, color='r', marker='o', label='timeline')
    ax[0].set_ylim(0, 101)

    # Slope bins, original and extended.
    x = [50, 60, 40, 30, 70, 80]
    y = [10, 20, 10, 10, 20, 20]
    ax[1].scatter(x, y, color='r', label='extended')
    x = [50, 60]
    y = [10, 20]
    ax[1].scatter(x, y, color='b', label='original')

    # Reconstructed timeline, original and extended
    x = [0, 0.3, 0.6, 1]
    y = [65, 60, 50, 20]
    ax[2].plot(x, y, color='r', marker='x', label='extended')
    x = [0.3, 0.6]
    y = [60, 50]
    ax[2].plot(x, y, color='b', marker='o', label='original')
    ax[2].set_ylim(0, 101)

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
