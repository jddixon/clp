#!/usr/bin/env python3

# clp/test_name_pair_reader.py

import io

import os
import unittest

from clp.py import get_name_pairs, CLPError

# -- bad input ------------------------------------------------------

NO_TAB_INPUT = """
hello\tthere
explosion_here  # no tab in this line
"""

# -- more bad input -------------------------------------------------
DUPE_LEFT_VALUE_INPUT = """
abc\\tdef        # this gets overridden
ghi\tjkl
abc\tmno
"""

# -- good input -----------------------------------------------------
TEST_DATA = """# silly comment at top of file



# comment at start of line
\t\t\t\t\t\t\t\t# comment over here

  abc\t   def\t\t\t\t # two tabs there
ghi\tjkl\t\t\t\t\t\t # single tab
foo\t\t bar
baz\t\t that_sort-of-thing\t\t  # tabs on right side
"""
# -- end good input -------------------------------------------------


class TestNamePairReader(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_empty_in_stream(self):
        in_stream = io.StringIO('')
        try:
            pairs = get_name_pairs(in_stream)
            self.fail("didn't raise on empty input")
        except CLPError as err:
            pass

    def test_ill_formed_input(self):
        in_stream = io.StringIO(NO_TAB_INPUT)
        with self.assertRaises(CLPError):
            pairs = get_name_pairs(in_stream)

    def test_dupe_left_input(self):
        in_stream = io.StringIO(DUPE_LEFT_VALUE_INPUT)
        with self.assertRaises(CLPError):
            pairs = get_name_pairs(in_stream)

    def test_name_pair_reader(self):

        in_stream = io.StringIO(TEST_DATA)
        pairs = get_name_pairs(in_stream)
        self.assertEqual(len(pairs), 4)

        self.assertTrue('abc' in pairs)
        self.assertTrue('baz' in pairs)
        self.assertTrue('foo' in pairs)
        self.assertTrue('ghi' in pairs)

        self.assertEqual(pairs['abc'], 'def')
        self.assertEqual(pairs['baz'], 'that_sort-of-thing')
        self.assertEqual(pairs['foo'], 'bar')
        self.assertEqual(pairs['ghi'], 'jkl')

if __name__ == '__main__':
    unittest.main()
