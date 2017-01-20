#!/usr/bin/python
import ui
import log
import osdata
import resource

from gi.repository import Gtk as gtk
from gi.repository import GObject as gobject
from gi.repository import AppIndicator3 as appindicator


APPINDICATOR_ID = 'batteryindicator'
CATEGORY = appindicator.IndicatorCategory.SYSTEM_SERVICES


class Battery:

    def __init__(self):
        self._status = None
        self._capacity = None
        self.update()

    def status(self):
        return self._status

    def capacity(self):
        return self._capacity

    def is_charging(self):
        return self.status() == 'Charging'

    def update(self):
        status = osdata.battery_status()
        capacity = osdata.battery_capacity()
        is_new = (self._status != status
                  or self._capacity != capacity)
        self._status = status
        self._capacity = capacity

        if is_new:
            self.log()

    def log(self):
        log.battery(self.capacity(), self.status())


class Indicator:

    def __init__(self):
        self.battery = Battery()
        self.indicator = appindicator.Indicator.new(
            APPINDICATOR_ID, self.get_icon(), CATEGORY)
        self.indicator.set_status(appindicator.IndicatorStatus.ACTIVE)
        self.indicator.set_menu(self.build_menu())

        gobject.timeout_add(500, self.update)

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

        item = gtk.MenuItem('Toggle theme')
        item.connect('activate', self.toggle_theme)
        menu.append(item)

        item = gtk.MenuItem('Quit')
        item.connect('activate', quit)
        menu.append(item)

        menu.show_all()
        return menu

    def toggle_theme(self, source):
        ui.toggle_theme()
        self.set_icon()

    def run_forever(self):
        gtk.main()

    def update(self):
        self.battery.update()
        self.set_icon()
        self.set_label()
        return True
