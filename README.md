# Battery Monitor

Battery Monitor is an application for Ubuntu laptops that provides timeline power usage and prediction graph.

![Battery Monitor]
(img/battery_monitor.png)

## Dependencies

- Python 2.7
- `sudo apt-get install --reinstall python-gi`

## Installation

- `sudo ./install.sh`
- add `batterym` to `Startup Applications`

## Links

- http://candidtim.github.io/appindicator/2014/09/13/ubuntu-appindicator-step-by-step.html
- http://askubuntu.com/questions/751608/how-can-i-write-a-dynamically-updated-panel-app-indicator
- http://askubuntu.com/questions/750815/fuzzy-clock-for-ubuntu/752675#752675
- http://askubuntu.com/questions/150970/how-can-i-change-the-application-indicator-label-after-delay
- http://stackoverflow.com/questions/11132929/showing-a-gtk-calendar-in-a-menu

## TODO

- [ ] Preserve history after reinstall
- [ ] Add config
- [ ] Remember theme selection after restart
