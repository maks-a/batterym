#!/usr/bin/python
# This code is an example for a tutorial on Ubuntu Unity/Gnome AppIndicators:
# http://candidtim.github.io/appindicator/2014/09/13/ubuntu-appindicator-step-by-step.html
# icons from https://materialdesignicons.com/
# /sys/class/power_supply/BAT0/uevent

import os
import time
import signal
import threading
import src.ui as ui
import src.resource as resource
import src.osdata as osdata
from datetime import datetime
from datetime import timedelta

from gi.repository import Gtk as gtk
from gi.repository import AppIndicator3 as appindicator


APPINDICATOR_ID = 'batteryindicator'
indicator = None
category = appindicator.IndicatorCategory.SYSTEM_SERVICES

battery_capacity = None
is_charging = None
icon = None



def get_icon(capacity, is_charging):
    if capacity is None or is_charging is None:
        return
    return resource.icon_path(capacity, is_charging, ui.THEME)


def probing():
    global battery_capacity
    global is_charging
    global icon
    battery_capacity = osdata.battery_capacity()
    is_charging = osdata.is_charging()
    icon = get_icon(battery_capacity, is_charging)


def run_monitoring(stop_event):
    step = timedelta(seconds=1)
    t1 = datetime.now() - step
    while not stop_event.is_set():
        t2 = datetime.now()
        if (t2 - t1) > step:
            t1 = t2
            probing()
            set_icon()
            set_label()
        time.sleep(0.1)


def run_background_monitoring():
    global th_background
    global th_background_stop
    th_background_stop = threading.Event()
    th_background = threading.Thread(
        target=run_monitoring, args=[th_background_stop])
    th_background.start()


def set_icon():
    if icon is None:
        return
    indicator.set_icon(icon)


def set_label():
    if battery_capacity is None:
        return
    indicator.set_label('{0}%'.format(battery_capacity), '')


def setup_indicator():
    global indicator
    probing()
    indicator = appindicator.Indicator.new(
        APPINDICATOR_ID, icon, category)
    indicator.set_status(appindicator.IndicatorStatus.ACTIVE)
    indicator.set_menu(build_menu())
    set_icon()
    set_label()


def build_menu():
    menu = gtk.Menu()
    item_quit = gtk.MenuItem('Toggle theme')
    item_quit.connect('activate', toggle_theme)
    menu.append(item_quit)
    item_quit = gtk.MenuItem('Quit')
    item_quit.connect('activate', quit)
    menu.append(item_quit)
    menu.show_all()
    return menu


def toggle_theme(source):
    ui.toggle_theme()
    set_icon()


def quit(source):
    if th_background_stop:
        th_background_stop.set()
    gtk.main_quit()


def run_forever():
    gtk.main()


def run():
    signal.signal(signal.SIGINT, signal.SIG_DFL)
    setup_indicator()
    run_background_monitoring()
    run_forever()


if __name__ == "__main__":
    run()
