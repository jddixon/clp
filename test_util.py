#!/usr/bin/env python3

# clp/test_util.py

import unittest
from clp.py import check_string


class TestUtils(unittest.TestCase):
    """
    """

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_check_string(self):

        name_pairs = {
            'foo': 'bar'
        }

        self.assertEqual(check_string("'foo'", name_pairs), "'bar'")
        self.assertEqual(check_string('"foo"', name_pairs), '"bar"')
        self.assertEqual(check_string('r"foo"', name_pairs), 'r"foo"')

if __name__ == '__main__':
    unittest.main()
