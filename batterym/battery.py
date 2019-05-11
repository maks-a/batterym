#!/usr/bin/python
from batterym import osdata
from batterym import observable


class Battery(observable.Observable):

    def __init__(self):
        observable.Observable.__init__(self)
        self._data = {}

    def data(self, key=None):
        return self._data if key is None else self._data.get(key)

    def status(self):
        return self.data('status')

    def capacity(self):
        return self.data('capacity')

    def is_charging(self):
        return self.status() == 'Charging'

    def update(self):
        data = {
            'status': osdata.battery_status(),
            'capacity': osdata.battery_capacity()
        }

        # send only changed parameter names
        if self._data != data:
            params = [k for k in data if self.data(k) != data[k]]
            self.update_callbacks(params)

        self._data = data
