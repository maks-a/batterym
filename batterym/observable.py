#!/usr/bin/python
import unittest


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


#####################################################################
class AnObserver(object):

    def __init__(self):
        self.message = None

    def update(self, message):
        self.message = message


class MyTest(unittest.TestCase):

    def setUp(self):
        self.observable = Observable()

        self.observer1 = AnObserver()
        self.observer2 = AnObserver()
        self.observer3 = AnObserver()

    def test_register_callback(self):
        self.observable.register_callback(self.observer1.update)
        self.observable.register_callback(self.observer2.update)
        self.observable.register_callback(self.observer3.update)

        self.assertEqual(len(self.observable.callbacks), 3)

    def test_unregister_callback(self):
        self.observable.register_callback(self.observer1.update)
        self.observable.register_callback(self.observer2.update)
        self.observable.register_callback(self.observer3.update)

        self.observable.unregister_callback(self.observer1.update)
        self.observable.unregister_callback(self.observer1.update)
        self.observable.unregister_callback(self.observer1.update)

        self.assertEqual(len(self.observable.callbacks), 2)

    def test_unregister_all_callbacks(self):
        self.observable.register_callback(self.observer1.update)
        self.observable.register_callback(self.observer2.update)
        self.observable.register_callback(self.observer3.update)

        self.observable.unregister_all_callbacks()

        self.assertEqual(len(self.observable.callbacks), 0)

    def test_update_callbacks(self):
        self.observable.register_callback(self.observer1.update)
        self.observable.register_callback(self.observer2.update)
        self.observable.register_callback(self.observer3.update)

        self.observable.update_callbacks('one')
        self.assertEqual(self.observer1.message, 'one')
        self.assertEqual(self.observer2.message, 'one')
        self.assertEqual(self.observer3.message, 'one')

        self.observable.update_callbacks(2)
        self.assertEqual(self.observer1.message, 2)
        self.assertEqual(self.observer2.message, 2)
        self.assertEqual(self.observer3.message, 2)
