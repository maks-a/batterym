#!/usr/bin/python
import os  # temp
import ui
import log
import battery
import resource
from datetime import datetime, timedelta

import gi
gi.require_version('Gtk', '3.0')
gi.require_version('AppIndicator3', '0.1')

from gi.repository import Gtk as gtk
from gi.repository import GObject as gobject
from gi.repository import AppIndicator3 as appindicator


APPINDICATOR_ID = 'batteryindicator'
CATEGORY = appindicator.IndicatorCategory.SYSTEM_SERVICES
BATTERY_MONITOR_ICON = '/usr/share/icons/Humanity/devices/48/battery.svg'
CAPACITY_HISTORY_CHART = os.path.abspath('capacity_history_12h.svg')


class Indicator:

    def __init__(self):
        sec = 1000
        self.battery = battery.Battery()
        self.battery_new_info = False
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
        self.calculate_chart()
        gobject.timeout_add(1*sec, self.update_battery)
        gobject.timeout_add(1*sec, self.update_log)
        gobject.timeout_add(30*sec, self.calculate_chart)

    def battery_update_callback(self, params):
        self.battery_new_info = True

    def update_battery(self):
        self.battery.update()
        if self.battery_new_info:
            self.update_log(is_new_data=True)
            self.set_icon()
            self.set_label()
            self.calculate_chart()
        self.battery_new_info = False
        return True

    def update_log(self, is_new_data=False):
        current_time = datetime.now()
        past_time = current_time - self.log_last_update
        is_update_time = past_time >= self.log_update_period
        if is_new_data or is_update_time:
            self.log_last_update = current_time
            log.battery(self.battery.capacity(), self.battery.status())
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

    def toggle_theme(self, _):
        ui.toggle_theme()
        self.set_icon()

    def quit(self, _):
        gtk.main_quit()

    def battery_monitor(self, _):
        self.window = gtk.Window()
        self.window.set_title('Battery monitor')
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

        self.window.show_all()

    def calculate_chart(self):
        log.calculate_history_chart(CAPACITY_HISTORY_CHART)
        return True

    def run_forever(self):
        gtk.main()
