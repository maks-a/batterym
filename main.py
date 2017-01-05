#!/usr/bin/python
# This code is an example for a tutorial on Ubuntu Unity/Gnome AppIndicators:
# http://candidtim.github.io/appindicator/2014/09/13/ubuntu-appindicator-step-by-step.html
# icons from https://materialdesignicons.com/

import os
import signal

from gi.repository import Gtk as gtk
from gi.repository import AppIndicator3 as appindicator
from gi.repository import Notify as notify


APPINDICATOR_ID = 'myappindicator'


def main():
  indicator = appindicator.Indicator.new(
    APPINDICATOR_ID, os.path.abspath('ic_battery_charging_white_48dp.png'),
    appindicator.IndicatorCategory.SYSTEM_SERVICES)
  indicator.set_status(appindicator.IndicatorStatus.ACTIVE)
  indicator.set_menu(build_menu())
  notify.init(APPINDICATOR_ID)
  gtk.main()


def build_menu():
  menu = gtk.Menu()
  item_quit = gtk.MenuItem('Quit')
  item_quit.connect('activate', quit)
  menu.append(item_quit)
  menu.show_all()
  return menu


def quit(_):
  notify.uninit()
  gtk.main_quit()


if __name__ == "__main__":
  signal.signal(signal.SIGINT, signal.SIG_DFL)
  main()
