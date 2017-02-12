#!/usr/bin/python
import log
import osdata

from datetime import datetime, timedelta

class Battery:

    def __init__(self):
        self._data = {}
        self._update_period = timedelta(minutes=10)
        self._last_update = datetime.now() - self._update_period
        self.observers = []
        self.update()

    def data(self, key=None):
        return self._data if key == None else self._data.get(key)

    def status(self):
        return self.data('status')

    def capacity(self):
        return self.data('capacity')

    def is_charging(self):
        return self.status() == 'Charging'

    def update(self):
        new_data = {
            'status' : osdata.battery_status(),
            'capacity' : osdata.battery_capacity()        
        }

        for k in new_data:
            if self.data(k) != new_data[k]:
                self.notify_observers(k, new_data[k])

        is_new_data = self._data != new_data
        self._data = new_data

        current_time = datetime.now()
        past_time = current_time - self._last_update
        is_update_time = past_time >= self._update_period

        if is_new_data or is_update_time:
            self._last_update = current_time
            self.log()

    def log(self):
        log.battery(self.capacity(), self.status())

    def notify_observers(self, message, value):
        for observer in self.observers:
            observer.get_update(message, value)

    def register_observer(self, observer):
        self.observers.append(observer)
