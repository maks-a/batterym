# Battery Monitor

## Requirements

- `sudo apt-get install --reinstall python-gi`
- `sudo python setup.py install`

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
creating build
creating build/lib.linux-x86_64-2.7
creating build/lib.linux-x86_64-2.7/batterym
copying batterym/__init__.py -> build/lib.linux-x86_64-2.7/batterym
copying batterym/main.py -> build/lib.linux-x86_64-2.7/batterym
copying batterym/observable.py -> build/lib.linux-x86_64-2.7/batterym
copying batterym/chart.py -> build/lib.linux-x86_64-2.7/batterym
copying batterym/indicator.py -> build/lib.linux-x86_64-2.7/batterym
copying batterym/plotter.py -> build/lib.linux-x86_64-2.7/batterym
copying batterym/resource.py -> build/lib.linux-x86_64-2.7/batterym
copying batterym/battery.py -> build/lib.linux-x86_64-2.7/batterym
copying batterym/osdata.py -> build/lib.linux-x86_64-2.7/batterym
copying batterym/future.py -> build/lib.linux-x86_64-2.7/batterym
copying batterym/ui.py -> build/lib.linux-x86_64-2.7/batterym
copying batterym/history.py -> build/lib.linux-x86_64-2.7/batterym
copying batterym/log.py -> build/lib.linux-x86_64-2.7/batterym
running build_scripts
creating build/scripts-2.7
copying and adjusting bin/batterym -> build/scripts-2.7
changing mode of build/scripts-2.7/batterym from 644 to 755
running install_lib
creating /usr/local/lib/python2.7/dist-packages/batterym
copying build/lib.linux-x86_64-2.7/batterym/__init__.py -> /usr/local/lib/python2.7/dist-packages/batterym
copying build/lib.linux-x86_64-2.7/batterym/main.py -> /usr/local/lib/python2.7/dist-packages/batterym
copying build/lib.linux-x86_64-2.7/batterym/observable.py -> /usr/local/lib/python2.7/dist-packages/batterym
copying build/lib.linux-x86_64-2.7/batterym/chart.py -> /usr/local/lib/python2.7/dist-packages/batterym
copying build/lib.linux-x86_64-2.7/batterym/indicator.py -> /usr/local/lib/python2.7/dist-packages/batterym
copying build/lib.linux-x86_64-2.7/batterym/plotter.py -> /usr/local/lib/python2.7/dist-packages/batterym
copying build/lib.linux-x86_64-2.7/batterym/resource.py -> /usr/local/lib/python2.7/dist-packages/batterym
copying build/lib.linux-x86_64-2.7/batterym/battery.py -> /usr/local/lib/python2.7/dist-packages/batterym
copying build/lib.linux-x86_64-2.7/batterym/osdata.py -> /usr/local/lib/python2.7/dist-packages/batterym
copying build/lib.linux-x86_64-2.7/batterym/future.py -> /usr/local/lib/python2.7/dist-packages/batterym
copying build/lib.linux-x86_64-2.7/batterym/ui.py -> /usr/local/lib/python2.7/dist-packages/batterym
copying build/lib.linux-x86_64-2.7/batterym/history.py -> /usr/local/lib/python2.7/dist-packages/batterym
copying build/lib.linux-x86_64-2.7/batterym/log.py -> /usr/local/lib/python2.7/dist-packages/batterym
byte-compiling /usr/local/lib/python2.7/dist-packages/batterym/__init__.py to __init__.pyc
byte-compiling /usr/local/lib/python2.7/dist-packages/batterym/main.py to main.pyc
byte-compiling /usr/local/lib/python2.7/dist-packages/batterym/observable.py to observable.pyc
byte-compiling /usr/local/lib/python2.7/dist-packages/batterym/chart.py to chart.pyc
byte-compiling /usr/local/lib/python2.7/dist-packages/batterym/indicator.py to indicator.pyc
byte-compiling /usr/local/lib/python2.7/dist-packages/batterym/plotter.py to plotter.pyc
byte-compiling /usr/local/lib/python2.7/dist-packages/batterym/resource.py to resource.pyc
byte-compiling /usr/local/lib/python2.7/dist-packages/batterym/battery.py to battery.pyc
byte-compiling /usr/local/lib/python2.7/dist-packages/batterym/osdata.py to osdata.pyc
byte-compiling /usr/local/lib/python2.7/dist-packages/batterym/future.py to future.pyc
byte-compiling /usr/local/lib/python2.7/dist-packages/batterym/ui.py to ui.pyc
byte-compiling /usr/local/lib/python2.7/dist-packages/batterym/history.py to history.pyc
byte-compiling /usr/local/lib/python2.7/dist-packages/batterym/log.py to log.pyc
running install_scripts
copying build/scripts-2.7/batterym -> /usr/local/bin
changing mode of /usr/local/bin/batterym to 755
running install_data
copying batterym.desktop -> /usr/share/batterym
running install_egg_info
Writing /usr/local/lib/python2.7/dist-packages/batterym-0.1.0.egg-info
```
