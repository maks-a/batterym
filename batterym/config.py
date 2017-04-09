#!/usr/bin/python
import os
import json
import misc
import resource
import unittest

from paths import CONFIG_FILE


def write_json(data, fname):
    text = json.dumps(data, indent=2)
    misc.write_to_file(text, fname)


def read_json(fname):
    text = misc.read_from_file(fname)
    if len(text) > 0:
        return json.loads(text)
    return None


def write_config(data, fname=None):
    if fname is None:
        fname = CONFIG_FILE
    write_json(data, fname)


def read_config(fname=None):
    if fname is None:
        fname = CONFIG_FILE
    data = read_json(fname)
    return data if isinstance(data, dict) else {}


def set_entry(key, value, fname=None):
    data = read_config(fname)
    data[key] = value
    write_config(data, fname)


def get_entry(key, fname=None, default_value=None):
    data = read_config(fname)
    return data.get(key, default_value)


class JsonTest(unittest.TestCase):

    def setUp(self):
        self.fname = 'tmp.json'
        if os.path.isfile(self.fname):
            os.remove(self.fname)

    def tearDown(self):
        if os.path.isfile(self.fname):
            os.remove(self.fname)

    def test_write_read(self):
        src = {}
        write_json(src, self.fname)
        result = read_json(self.fname)
        self.assertEqual(src, result)

        src = {
            'abc': 1,
            'xyz': 2
        }
        write_json(src, self.fname)
        result = read_json(self.fname)
        self.assertEqual(src, result)


class ConfigTest(unittest.TestCase):

    def setUp(self):
        self.fname = 'config_tmp.json'
        if os.path.isfile(self.fname):
            os.remove(self.fname)

    def tearDown(self):
        if os.path.isfile(self.fname):
            os.remove(self.fname)

    def test_read_no_file(self):
        result = read_config('non_existing_file')
        expected = {}
        self.assertEqual(result, expected)

    def test_write_read(self):
        src = {}
        write_config(src, self.fname)
        result = read_config(self.fname)
        self.assertEqual(src, result)

        src = {
            'abc': 1,
            'xyz': 2
        }
        write_config(src, self.fname)
        result = read_config(self.fname)
        self.assertEqual(src, result)

    def test_set_entry(self):
        write_config({}, self.fname)
        set_entry('aaa', 5, self.fname)
        result = read_config(self.fname)
        expected = {
            'aaa': 5
        }
        self.assertEqual(result, expected)

        write_config({}, self.fname)
        set_entry('bbb', -1, self.fname)
        set_entry('ccc', None, self.fname)
        result = read_config(self.fname)
        expected = {
            'bbb': -1,
            'ccc': None
        }
        self.assertEqual(result, expected)

    def test_get_entry(self):
        src = {}
        write_config(src, self.fname)
        result = get_entry('aaa', self.fname)
        expected = None
        self.assertEqual(result, expected)

        src = {}
        write_config(src, self.fname)
        result = get_entry('aaa', self.fname, default_value=True)
        expected = True
        self.assertEqual(result, expected)

        src = {
            'aaa': 5
        }
        write_config(src, self.fname)
        result = get_entry('aaa', self.fname)
        expected = 5
        self.assertEqual(result, expected)
