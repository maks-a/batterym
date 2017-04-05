#!/usr/bin/python
import os  # temp
import ui
import log
import battery
import resource
import plotter
from datetime import datetime, timedelta
import unittest

import gi
gi.require_version('Gtk', '3.0')
gi.require_version('AppIndicator3', '0.1')

from gi.repository import Gtk as gtk
from gi.repository import GObject as gobject
from gi.repository import AppIndicator3 as appindicator


APPINDICATOR_ID = 'batterym'
CATEGORY = appindicator.IndicatorCategory.SYSTEM_SERVICES
BATTERY_MONITOR_ICON = os.path.join(
    resource.RESOURCES_DIRECTORY_PATH, 'img/battery.svg')
CAPACITY_HISTORY_CHART = os.path.join(
    resource.RESOURCES_DIRECTORY_PATH, 'img/capacity_history_12h.svg')


class Indicator:

    def __init__(self):
        self.battery = battery.Battery()
        self.battery.new_params = None
        self.battery.register_callback(self.battery_update_callback)
        self.battery.update()

        self.indicator = appindicator.Indicator.new(
            APPINDICATOR_ID, self.get_icon(), CATEGORY)
        self.indicator.set_status(appindicator.IndicatorStatus.ACTIVE)
        self.indicator.set_menu(self.build_menu())
        self.window = None

        self.log_update_period = timedelta(minutes=5)
        self.log_last_update = datetime.now()
        self.update_battery()
        self.update_chart()
        sec = 1000
        gobject.timeout_add(1*sec, self.update_battery)
        gobject.timeout_add(1*sec, self.update_log)
        gobject.timeout_add(30*sec, self.update_chart)

    def battery_update_callback(self, params):
        self.battery.new_params = params

    def update_battery(self):
        self.battery.update()
        if self.battery.new_params is not None:
            self.set_icon()
            self.set_label()
            self.update_log(is_new_data=True)
            self.update_chart()
        self.battery.new_params = None
        return True

    def update_log(self, is_new_data=False):
        now = datetime.now()
        time_diff = now - self.log_last_update
        is_update_time = self.log_update_period <= time_diff
        if is_new_data or is_update_time:
            log.battery(self.battery.capacity(), self.battery.status())
            self.log_last_update = now
        return True

    def update_chart(self):
        plotter.caluclate_chart(CAPACITY_HISTORY_CHART)
        if self.window and self.window.props.visible:
            self.image.set_from_file(CAPACITY_HISTORY_CHART)
        return True

    def get_icon(self):
        return resource.icon_path(
            self.battery.capacity(), self.battery.is_charging())

    def set_icon(self):
        self.indicator.set_icon(self.get_icon())

    def set_label(self):
        text = '{0}%'.format(self.battery.capacity())
        self.indicator.set_label(text, '')

    def build_menu(self):
        menu = gtk.Menu()

        item = gtk.MenuItem('Battery monitor')
        item.connect('activate', self.battery_monitor)
        menu.append(item)

        item = gtk.MenuItem('Toggle theme')
        item.connect('activate', self.toggle_theme)
        menu.append(item)

        item = gtk.MenuItem('Quit')
        item.connect('activate', self.quit)
        menu.append(item)

        menu.show_all()
        return menu

    def battery_monitor(self, _):
        if self.window is None:
            self.window = gtk.Window()
            self.window.connect('delete-event', self.close_window)
            self.window.set_title('Battery Monitor')
            self.window.set_border_width(10)
            self.window.set_size_request(700, 500)
            self.window.set_resizable(False)
            self.window.set_position(gtk.WindowPosition.CENTER)
            self.window.set_icon_from_file(BATTERY_MONITOR_ICON)
            self.window.vbox = gtk.Box()
            self.window.vbox.set_spacing(5)
            self.window.vbox.set_orientation(gtk.Orientation.VERTICAL)
            self.window.add(self.window.vbox)
            self.image = gtk.Image()
            self.image.set_from_file(CAPACITY_HISTORY_CHART)
            self.window.vbox.pack_start(self.image, False, False, 0)
        if not self.window.props.visible:
            self.window.show_all()

    def close_window(self, arg1, arg2):
        self.window.hide()
        return True

    def toggle_theme(self, _):
        ui.toggle_theme()
        self.set_icon()

    def quit(self, _):
        gtk.main_quit()

    def run_forever(self):
        gtk.main()
