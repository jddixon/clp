#!/usr/bin/env python3

# clp/test_util.py

""" Test CLP Utilities. """

import unittest
from clp.py import check_string, check_name, CLPError


class TestUtils(unittest.TestCase):
    """ Test CLP Utilities. """

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_check_name(self):
        """ Test the check_name() function. """
        with self.assertRaises(CLPError):
            check_name(None)
        with self.assertRaises(CLPError):
            check_name('')
        with self.assertRaises(CLPError):
            check_name('123')
        with self.assertRaises(CLPError):
            check_name('a.b')   # no dots please
        with self.assertRaises(CLPError):
            check_name('a?')

        check_name('_123')          # ok if first char is underscore
        check_name('_')             # or just single underscore

    def test_check_string(self):
        """ Test the check_string() function. """

        name_pairs = {
            'foo': 'bar'
        }

        self.assertEqual(check_string("'foo'", name_pairs), "'bar'")
        self.assertEqual(check_string('"foo"', name_pairs), '"bar"')
        self.assertEqual(check_string('r"foo"', name_pairs), 'r"foo"')


if __name__ == '__main__':
    unittest.main()
