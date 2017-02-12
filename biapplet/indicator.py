#!/usr/bin/python
import os  # temp
import ui
import log
import battery
import resource

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
        self.battery = battery.Battery()
        self.battery.register_observer(self)
        self.indicator = appindicator.Indicator.new(
            APPINDICATOR_ID, self.get_icon(), CATEGORY)
        self.indicator.set_status(appindicator.IndicatorStatus.ACTIVE)
        self.indicator.set_menu(self.build_menu())
        self.window = None

        sec = 1000
        gobject.timeout_add(0.5*sec, self.update)
        gobject.timeout_add(30*sec, self.calculate_chart)

        self.calculate_chart()

    def get_update(self, message, value):
        self.calculate_chart()

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
        self.window.vbox.pack_start(self.image, False, False, 0)

        self.window.show_all()

        self.update()

    def update(self):
        self.battery.update()
        self.set_icon()
        self.set_label()
        if self.window and self.window.props.visible:
            self.image.set_from_file(CAPACITY_HISTORY_CHART)
        return True

    def calculate_chart(self):
        log.calculate_history_chart(CAPACITY_HISTORY_CHART)
        return True

    def run_forever(self):
        gtk.main()
