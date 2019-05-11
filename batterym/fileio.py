#!/usr/bin/python
import os
import unittest


def create_missing_dirs(path):
    basedir = os.path.dirname(path)
    if len(basedir) == 0:
        return
    if not os.path.exists(basedir):
        print('creating {0}'.format(basedir))
        os.makedirs(basedir)
        if not os.path.exists(basedir):
            raise FileNotFoundError


def delete_dir_and_content(path):
    print('deleting {0}'.format(path))
    os.removedirs(path)
    if os.path.exists(path):
        raise FileExistsError


def append(text, fname):
    create_missing_dirs(fname)
    with open(fname, 'a') as f:
        f.write(text)


def write(text, fname):
    create_missing_dirs(fname)
    with open(fname, 'w') as f:
        f.write(text)


def read(fname):
    if os.path.isfile(fname):
        with open(fname, 'r') as f:
            return f.read()
    return ''


def write_lines(lines, fname):
    if len(lines) > 0:
        write('\n'.join(lines) + '\n', fname)


def read_lines(fname):
    return read(fname).splitlines()


def remove_front_lines_if_too_many(fname, lines_threshold=None):
    lines = read_lines(fname)
    if lines_threshold is not None and lines_threshold < len(lines):
        lines = lines[-lines_threshold:]
        write_lines(lines, fname)


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
        expected = ''
        write_lines(src, self.fname)
        result = read(self.fname)
        self.assertEqual(result, expected)
        result = read_lines(self.fname)
        self.assertEqual(src, result)

        src = ['abc']
        expected = 'abc\n'
        write_lines(src, self.fname)
        result = read(self.fname)
        self.assertEqual(result, expected)
        result = read_lines(self.fname)
        self.assertEqual(src, result)

        src = ['1', '2', '3']
        expected = '1\n2\n3\n'
        write_lines(src, self.fname)
        result = read(self.fname)
        self.assertEqual(result, expected)
        result = read_lines(self.fname)
        self.assertEqual(src, result)

    def test_append(self):
        src = ''
        append(src, self.fname)
        append(src, self.fname)
        result = read(self.fname)
        self.assertEqual(2*src, result)

        src = 'abc_'
        append(src, self.fname)
        append(src, self.fname)
        result = read(self.fname)
        self.assertEqual(2*src, result)

    def test_create_dirs(self):
        folder = 'tmp_folder/'
        create_missing_dirs(folder)
        self.assertTrue(os.path.exists(folder))

        delete_dir_and_content(folder)
        self.assertFalse(os.path.exists(folder))

    def test_remove_front_lines_if_too_many(self):
        src = [str(x) for x in range(0, 10)]
        write_lines(src, self.fname)
        remove_front_lines_if_too_many(self.fname, 3)
        result = read_lines(self.fname)
        expected = ['7', '8', '9']
        self.assertEqual(result, expected)

        src = [str(x) for x in range(0, 3)]
        write_lines(src, self.fname)
        remove_front_lines_if_too_many(self.fname, 10)
        result = read_lines(self.fname)
        expected = ['0', '1', '2']
        self.assertEqual(result, expected)

        src = [str(x) for x in range(0, 3)]
        write_lines(src, self.fname)
        remove_front_lines_if_too_many(self.fname, 3)
        result = read_lines(self.fname)
        expected = ['0', '1', '2']
        self.assertEqual(result, expected)

        src = [str(x) for x in range(0, 3)]
        write_lines(src, self.fname)
        remove_front_lines_if_too_many(self.fname, 2)
        result = read_lines(self.fname)
        expected = ['1', '2']
        self.assertEqual(result, expected)

        src = [str(x) for x in range(0, 3)]
        write_lines(src, self.fname)
        remove_front_lines_if_too_many(self.fname)
        result = read_lines(self.fname)
        expected = ['0', '1', '2']
        self.assertEqual(result, expected)

        src = [str(x) for x in range(0, 3)]
        write_lines(src, self.fname)
        remove_front_lines_if_too_many(self.fname, None)
        result = read_lines(self.fname)
        expected = ['0', '1', '2']
        self.assertEqual(result, expected)
