#!/usr/bin/python
import os
import unittest


def create_missing_dirs(path):
    basedir = os.path.dirname(path)
    if len(basedir) == 0:
        return
    if not os.path.exists(basedir):
        os.makedirs(basedir)


def append_to_file(text, fname):
    create_missing_dirs(fname)
    with open(fname, 'a') as f:
        f.write(text)


def write_to_file(text, fname):
    create_missing_dirs(fname)
    with open(fname, 'w') as f:
        f.write(text)


def read_from_file(fname):
    if os.path.isfile(fname):
        with open(fname, 'r') as f:
            return f.read()
    return ''


def write_lines_to_file(lines, fname):
    write_to_file('\n'.join(lines), fname)


def read_lines_from_file(fname):
    return read_from_file(fname).splitlines()


class MyTest(unittest.TestCase):

    def setUp(self):
        self.fname = 'tmp.txt'
        if os.path.isfile(self.fname):
            os.remove(self.fname)

    def tearDown(self):
        if os.path.isfile(self.fname):
            os.remove(self.fname)

    def test_write_read(self):
        src = []
        write_lines_to_file(src, self.fname)
        result = read_lines_from_file(self.fname)
        self.assertEqual(src, result)

        src = ['abc']
        write_lines_to_file(src, self.fname)
        result = read_lines_from_file(self.fname)
        self.assertEqual(src, result)

    def test_append(self):
        src = ''
        append_to_file(src, self.fname)
        append_to_file(src, self.fname)
        result = read_from_file(self.fname)
        self.assertEqual(2*src, result)

        src = 'abc_'
        append_to_file(src, self.fname)
        append_to_file(src, self.fname)
        result = read_from_file(self.fname)
        self.assertEqual(2*src, result)
