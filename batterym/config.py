#!/usr/bin/python
import os
import json
import misc
import resource
import unittest


CONFIG_FILE = os.path.join(
    resource.RESOURCES_DIRECTORY_PATH, 'config/config.json')


def write_json(data, fname):
    text = json.dumps(data, indent=2)
    misc.write_to_file(text, fname)


def read_json(fname):
    text = misc.read_from_file(fname)
    return json.loads(text)


def write_config(data):
    write_json(text, CONFIG_FILE)


def read_config():
    return read_json(CONFIG_FILE)


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
