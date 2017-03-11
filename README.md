# Battery Monitor

## Requirements

`sudo apt-get install --reinstall python-gi`

## Links

- http://candidtim.github.io/appindicator/2014/09/13/ubuntu-appindicator-step-by-step.html
- https://materialdesignicons.com/
- /sys/class/power_supply/BAT0/uevent
- http://askubuntu.com/questions/751608/how-can-i-write-a-dynamically-updated-panel-app-indicator
- http://askubuntu.com/questions/750815/fuzzy-clock-for-ubuntu/752675#752675
- http://askubuntu.com/questions/150970/how-can-i-change-the-application-indicator-label-after-delay
- http://stackoverflow.com/questions/11132929/showing-a-gtk-calendar-in-a-menu

```bash
sudo python setup.py install
running install
running build
running build_py
creating build/lib.linux-x86_64-2.7
creating build/lib.linux-x86_64-2.7/biapplet
copying biapplet/__init__.py -> build/lib.linux-x86_64-2.7/biapplet
copying biapplet/observable.py -> build/lib.linux-x86_64-2.7/biapplet
copying biapplet/chart.py -> build/lib.linux-x86_64-2.7/biapplet
copying biapplet/indicator.py -> build/lib.linux-x86_64-2.7/biapplet
copying biapplet/plotter.py -> build/lib.linux-x86_64-2.7/biapplet
copying biapplet/resource.py -> build/lib.linux-x86_64-2.7/biapplet
copying biapplet/battery.py -> build/lib.linux-x86_64-2.7/biapplet
copying biapplet/osdata.py -> build/lib.linux-x86_64-2.7/biapplet
copying biapplet/future.py -> build/lib.linux-x86_64-2.7/biapplet
copying biapplet/ui.py -> build/lib.linux-x86_64-2.7/biapplet
copying biapplet/history.py -> build/lib.linux-x86_64-2.7/biapplet
copying biapplet/biapplet.py -> build/lib.linux-x86_64-2.7/biapplet
copying biapplet/log.py -> build/lib.linux-x86_64-2.7/biapplet
running build_scripts
running install_lib
creating /usr/local/lib/python2.7/dist-packages/biapplet
copying build/lib.linux-x86_64-2.7/biapplet/__init__.py -> /usr/local/lib/python2.7/dist-packages/biapplet
copying build/lib.linux-x86_64-2.7/biapplet/observable.py -> /usr/local/lib/python2.7/dist-packages/biapplet
copying build/lib.linux-x86_64-2.7/biapplet/chart.py -> /usr/local/lib/python2.7/dist-packages/biapplet
copying build/lib.linux-x86_64-2.7/biapplet/indicator.py -> /usr/local/lib/python2.7/dist-packages/biapplet
copying build/lib.linux-x86_64-2.7/biapplet/plotter.py -> /usr/local/lib/python2.7/dist-packages/biapplet
copying build/lib.linux-x86_64-2.7/biapplet/resource.py -> /usr/local/lib/python2.7/dist-packages/biapplet
copying build/lib.linux-x86_64-2.7/biapplet/battery.py -> /usr/local/lib/python2.7/dist-packages/biapplet
copying build/lib.linux-x86_64-2.7/biapplet/osdata.py -> /usr/local/lib/python2.7/dist-packages/biapplet
copying build/lib.linux-x86_64-2.7/biapplet/future.py -> /usr/local/lib/python2.7/dist-packages/biapplet
copying build/lib.linux-x86_64-2.7/biapplet/ui.py -> /usr/local/lib/python2.7/dist-packages/biapplet
copying build/lib.linux-x86_64-2.7/biapplet/history.py -> /usr/local/lib/python2.7/dist-packages/biapplet
copying build/lib.linux-x86_64-2.7/biapplet/biapplet.py -> /usr/local/lib/python2.7/dist-packages/biapplet
copying build/lib.linux-x86_64-2.7/biapplet/log.py -> /usr/local/lib/python2.7/dist-packages/biapplet
byte-compiling /usr/local/lib/python2.7/dist-packages/biapplet/__init__.py to __init__.pyc
byte-compiling /usr/local/lib/python2.7/dist-packages/biapplet/observable.py to observable.pyc
byte-compiling /usr/local/lib/python2.7/dist-packages/biapplet/chart.py to chart.pyc
byte-compiling /usr/local/lib/python2.7/dist-packages/biapplet/indicator.py to indicator.pyc
byte-compiling /usr/local/lib/python2.7/dist-packages/biapplet/plotter.py to plotter.pyc
byte-compiling /usr/local/lib/python2.7/dist-packages/biapplet/resource.py to resource.pyc
byte-compiling /usr/local/lib/python2.7/dist-packages/biapplet/battery.py to battery.pyc
byte-compiling /usr/local/lib/python2.7/dist-packages/biapplet/osdata.py to osdata.pyc
byte-compiling /usr/local/lib/python2.7/dist-packages/biapplet/future.py to future.pyc
byte-compiling /usr/local/lib/python2.7/dist-packages/biapplet/ui.py to ui.pyc
byte-compiling /usr/local/lib/python2.7/dist-packages/biapplet/history.py to history.pyc
byte-compiling /usr/local/lib/python2.7/dist-packages/biapplet/biapplet.py to biapplet.pyc
byte-compiling /usr/local/lib/python2.7/dist-packages/biapplet/log.py to log.pyc
running install_scripts
changing mode of /usr/local/bin/biapplet to 755
changing mode of /usr/local/bin/biapplet.py to 775
running install_data
running install_egg_info
Removing /usr/local/lib/python2.7/dist-packages/biapplet-0.1.0.egg-info
Writing /usr/local/lib/python2.7/dist-packages/biapplet-0.1.0.egg-info
```
