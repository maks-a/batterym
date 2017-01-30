#!/usr/bin/python
import os  # temp
import ui
import log
import osdata
import resource

from datetime import datetime, timedelta

from gi.repository import Gtk as gtk
from gi.repository import GObject as gobject
from gi.repository import AppIndicator3 as appindicator


APPINDICATOR_ID = 'batteryindicator'
CATEGORY = appindicator.IndicatorCategory.SYSTEM_SERVICES
BATTERY_MONITOR_ICON = '/usr/share/icons/Humanity/devices/48/battery.svg'
CAPACITY_HISTORY_CHART = os.path.abspath('capacity_history_12h.svg')


class Battery:

    def __init__(self):
        self._status = None
        self._capacity = None
        self._update_period = timedelta(minutes=10)
        self._last_update = datetime.now() - self._update_period
        self.observers = []
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
        is_new_status = self._status != status
        is_new_capacity = self._capacity != capacity
        is_new_data = is_new_status or is_new_capacity
        self._status = status
        self._capacity = capacity

        current_time = datetime.now()
        past_time = current_time - self._last_update
        is_update_time = past_time >= self._update_period

        if is_new_data or is_update_time:
            self._last_update = current_time
            self.log()

        if is_new_status:
            self.notify_observers('status', status)
        if is_new_capacity:
            self.notify_observers('capacity', capacity)

    def log(self):
        log.battery(self.capacity(), self.status())

    def notify_observers(self, message, value):
        for observer in self.observers:
            observer.get_update(message, value)

    def register_observer(self, observer):
        self.observers.append(observer)


class Indicator:

    def __init__(self):
        self.battery = Battery()
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
