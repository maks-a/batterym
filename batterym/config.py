#!/usr/bin/python
import os
import json
import unittest

from batterym import resource
from batterym import fileio
from batterym.paths import CONFIG_DEFAULT_FILE
from batterym.paths import CONFIG_USER_FILE


def _write_json(data, fname):
    text = json.dumps(data, indent=2)
    fileio.write(text, fname)


def _read_json(fname):
    text = fileio.read(fname)
    if len(text) > 0:
        return json.loads(text)


def _read_dict(fname):
    d = _read_json(fname)
    return d if isinstance(d, dict) else {}


def _read_configs(fnames):
    data = {}
    for f in fnames:
        data.update(_read_dict(f))
    return data


def _get_fnames(fname_default=None, fname_user=None):
    if fname_default is None:
        fname_default = CONFIG_DEFAULT_FILE
    if fname_user is None:
        fname_user = CONFIG_USER_FILE
    return fname_default, fname_user


def write_config(data, fname_default=None, fname_user=None):
    fname_default, fname_user = _get_fnames(fname_default, fname_user)
    _write_json(data, fname_user)


def read_config(fname_default=None, fname_user=None):
    fname_default, fname_user = _get_fnames(fname_default, fname_user)
    return _read_configs([fname_default, fname_user])


def set_entry(key, value, fname_default=None, fname_user=None):
    _, fname_user = _get_fnames(fname_default, fname_user)
    data = read_config(fname_user, fname_user)
    data[key] = value
    write_config(data, fname_user, fname_user)


def get_entry(key, default_value=None, fname_default=None, fname_user=None):
    data = read_config(fname_default, fname_user)
    return data.get(key, default_value)


class JsonTest(unittest.TestCase):

    def setUp(self):
        self.fname = 'tmp.json'
        if os.path.isfile(self.fname):
            os.remove(self.fname)

    def tearDown(self):
        if os.path.isfile(self.fname):
            os.remove(self.fname)

    def test_no_file(self):
        no_file = 'non-existing-file-name'

        result = _read_json(no_file)
        self.assertEqual(result, None)

        result = _read_dict(no_file)
        self.assertEqual(result, {})

    def test_empty_file(self):
        empty_file = self.fname

        result = _read_json(empty_file)
        self.assertEqual(result, None)

        result = _read_dict(empty_file)
        self.assertEqual(result, {})

    def test_write_read(self):
        src = {}
        _write_json(src, self.fname)
        result = _read_json(self.fname)
        self.assertEqual(src, result)
        result = _read_dict(self.fname)
        self.assertEqual(src, result)

        src = {'abc': 1, 'xyz': 2}
        _write_json(src, self.fname)
        result = _read_json(self.fname)
        self.assertEqual(src, result)
        result = _read_dict(self.fname)
        self.assertEqual(src, result)


class ConfigTest(unittest.TestCase):

    def remove_files(self):
        for f in self.files:
            if os.path.isfile(f):
                os.remove(f)

    def setUp(self):
        self.fname = 'config_tmp.json'
        self.file_a = 'file_a'
        self.file_b = 'file_b'
        self.files = [self.fname, self.file_a, self.file_b]
        self.remove_files()

    def tearDown(self):
        self.remove_files()

    def test_no_file(self):
        no_file = 'non-existing-file-name'
        result = read_config(no_file, no_file)
        self.assertEqual(result, {})

    def test_empty_file(self):
        empty_file = self.fname
        result = read_config(empty_file, empty_file)
        self.assertEqual(result, {})

    def test_get_fnames(self):
        result = _get_fnames()
        expected = (CONFIG_DEFAULT_FILE, CONFIG_USER_FILE)
        self.assertEqual(result, expected)

        result = _get_fnames('a')
        expected = ('a', CONFIG_USER_FILE)
        self.assertEqual(result, expected)

        result = _get_fnames('a', 'b')
        expected = ('a', 'b')
        self.assertEqual(result, expected)

        result = _get_fnames(fname_user='a')
        expected = (CONFIG_DEFAULT_FILE, 'a')
        self.assertEqual(result, expected)

        result = _get_fnames(fname_default='a')
        expected = ('a', CONFIG_USER_FILE)
        self.assertEqual(result, expected)

    def test_read_configs(self):
        config_a = {'a': 1}
        config_b = {'b': 2}
        _write_json(config_a, self.file_a)
        _write_json(config_b, self.file_b)
        result = _read_configs([self.file_a, self.file_b])
        expected = {'a': 1, 'b': 2}
        self.assertEqual(result, expected)

        config_a = {'a': 1}
        config_b = {'a': 2}
        _write_json(config_a, self.file_a)
        _write_json(config_b, self.file_b)
        result = _read_configs([self.file_a, self.file_b])
        expected = {'a': 2}
        self.assertEqual(result, expected)

        config_a = {'a': 1}
        config_b = {'a': 2}
        _write_json(config_a, self.file_a)
        _write_json(config_b, self.file_b)
        result = _read_configs([self.file_b, self.file_a])
        expected = {'a': 1}
        self.assertEqual(result, expected)

    def mock_write_config(self, data):
        write_config(data, self.file_a, self.file_b)

    def mock_read_config(self):
        return read_config(self.file_a, self.file_b)

    def mock_set_entry(self, key, value):
        set_entry(key, value, self.file_a, self.file_b)

    def mock_get_entry(self, key, default_value=None):
        return get_entry(key, default_value, self.file_a, self.file_b)

    def test_write_read(self):
        config_default = {}
        config_user = {}
        src = {}
        _write_json(config_default, self.file_a)
        _write_json(config_user, self.file_b)
        self.mock_write_config(src)
        result = self.mock_read_config()
        self.assertEqual(src, result)

        config_default = {}
        config_user = {}
        src = {'abc': 1, 'xyz': 2}
        _write_json(config_default, self.file_a)
        _write_json(config_user, self.file_b)
        self.mock_write_config(src)
        result = self.mock_read_config()
        self.assertEqual(src, result)

        config_default = {'c': 3}
        config_user = {}
        src = {'abc': 1, 'xyz': 2}
        expected = {'abc': 1, 'xyz': 2, 'c': 3}
        _write_json(config_default, self.file_a)
        _write_json(config_user, self.file_b)
        self.mock_write_config(src)
        result = self.mock_read_config()
        self.assertEqual(result, expected)

    def test_set_entry(self):
        config_default = {}
        config_user = {}
        _write_json(config_default, self.file_a)
        _write_json(config_user, self.file_b)

        self.mock_set_entry('aaa', 5)
        result = self.mock_read_config()
        expected = {'aaa': 5}
        self.assertEqual(result, expected)

        config_default = {}
        config_user = {}
        _write_json(config_default, self.file_a)
        _write_json(config_user, self.file_b)

        self.mock_set_entry('bbb', -1)
        self.mock_set_entry('ccc', None)
        result = self.mock_read_config()
        expected = { 'bbb': -1, 'ccc': None }
        self.assertEqual(result, expected)

    def test_get_entry(self):
        config_default = {}
        config_user = {}
        _write_json(config_default, self.file_a)
        _write_json(config_user, self.file_b)

        result = self.mock_get_entry('aaa')
        expected = None
        self.assertEqual(result, expected)

        config_default = {}
        config_user = {}
        _write_json(config_default, self.file_a)
        _write_json(config_user, self.file_b)
        result = self.mock_get_entry('aaa', default_value=True)
        expected = True
        self.assertEqual(result, expected)

        config_default = { 'aaa': 5 }
        config_user = {}
        _write_json(config_default, self.file_a)
        _write_json(config_user, self.file_b)
        result = self.mock_get_entry('aaa')
        expected = 5
        self.assertEqual(result, expected)

