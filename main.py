#!/usr/bin/python
# This code is an example for a tutorial on Ubuntu Unity/Gnome AppIndicators:
# http://candidtim.github.io/appindicator/2014/09/13/ubuntu-appindicator-step-by-step.html
# icons from https://materialdesignicons.com/

import os
import signal

from gi.repository import Gtk as gtk
from gi.repository import AppIndicator3 as appindicator
from gi.repository import Notify as notify


APPINDICATOR_ID = 'batteryindicator'
indicator = None
icon = None
category = appindicator.IndicatorCategory.SYSTEM_SERVICES


def set_icon(new_icon):
    global icon
    icon = new_icon
    indicator.set_icon(icon)


def register_indicator(app_id, icon, ctgry):
    return appindicator.Indicator.new(app_id, icon, ctgry)


def setup_indicator(icon):
    global indicator
    indicator = register_indicator(APPINDICATOR_ID, icon, category)
    indicator.set_status(appindicator.IndicatorStatus.ACTIVE)
    indicator.set_menu(build_menu())
    indicator.set_label('84%', '')
    set_icon(icon)
    notify.init(APPINDICATOR_ID)


def build_menu():
    menu = gtk.Menu()
    item_quit = gtk.MenuItem('Quit')
    item_quit.connect('activate', quit)
    menu.append(item_quit)
    menu.show_all()
    return menu


def quit(source):
    notify.uninit()
    gtk.main_quit()


def run_forever():
    gtk.main()


def run():
    signal.signal(signal.SIGINT, signal.SIG_DFL)
    setup_indicator(
        os.path.abspath('ic_battery_charging_white_48dp.png'))
    run_forever()


if __name__ == "__main__":
    run()
