#!/usr/bin/python


class Observable(object):

    def __init__(self):
        self.callbacks = []

    def register_callback(self, callback):
        if not callback in self.callbacks:
            self.callbacks.append(callback)

    def unregister_callback(self, callback):
        if callback in self.callbacks:
            self.callbacks.remove(callback)

    def unregister_all_callbacks(self):
        self.callbacks = []

    def update_callbacks(self, message):
        for callback in self.callbacks:
            callback(message)
