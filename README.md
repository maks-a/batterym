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
[sudo] password for m: 
running install
running build
running build_py
running build_scripts
running install_lib
warning: install_lib: 'build/lib.linux-x86_64-2.7' does not exist -- no Python modules to install

running install_scripts
copying build/scripts-2.7/biapplet.py -> /usr/local/bin
changing mode of /usr/local/bin/biapplet.py to 775
running install_data
creating /usr/share/batterym
copying biapplet.desktop -> /usr/share/batterym
running install_egg_info
Writing /usr/local/lib/python2.7/dist-packages/biapplet-0.1.0.egg-info
```
