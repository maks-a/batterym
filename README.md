Battery Monitor
-------------

Battery Monitor is an application for Ubuntu laptops that tracks battery capacity history and provides time-to-end prediction. It has a simple user interface that gives just enough information to answer the following questions:

- what is current capacity?
- what is predicted time to full charge/discharge (time-to-end)?
- what is recent capacity history?
- what is predicted capacity trend?


## Screenshots

### Example 1

![Battery Monitor](img/batterym_1.png)

How to read this information:

- 13% current capacity
- predicted remaining 53 minutes till full discharge
- it took ~9.5 hours to fully discharge from 100%
- predicted discharging trend is linear

### Example 2

![Battery Monitor](img/batterym_2.png)

How to read this information:

- 4% current capacity
- predicted 2 hours 35 minutes till full charge
- predicted charging trend is exponential

### Example 3

![Battery Monitor](img/batterym_3.png)

How to read this information:

- 100% current capacity
- it took ~2.5 hours to fully charge (almost as predicted!!!)

## Quick Links

- [TODO](todo.md)
- [Release Notes](release-notes.md)

## Dependencies

### Usage

- Python 2.7
- `sudo apt-get install --reinstall python-gi`

### Build tools

- `sudo pip install coverage`

## Installation

Non-root, non-sudo user installation is supported. Application will be installed in `/home/{$USER}/.local/batterym/` folder. After installation the file `install_log.txt` should appear in the source folder.

- run `./install.sh`
- save `install_log.txt` for the later uninstallation
- add `batterym` to `Startup Applications`

## Uninstallation

Make sure you have `install_log.txt` next to `uninstall.sh`.

- run `./uninstall.sh`

## Licensing

Apache License, Version 2.0. See LICENSE for the full license text.

## Links

- http://candidtim.github.io/appindicator/2014/09/13/ubuntu-appindicator-step-by-step.html
- http://askubuntu.com/questions/751608/how-can-i-write-a-dynamically-updated-panel-app-indicator
- http://askubuntu.com/questions/750815/fuzzy-clock-for-ubuntu/752675#752675
- http://askubuntu.com/questions/150970/how-can-i-change-the-application-indicator-label-after-delay
- http://stackoverflow.com/questions/11132929/showing-a-gtk-calendar-in-a-menu
