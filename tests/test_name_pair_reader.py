#!/usr/bin/env python3

# clp/test_name_pair_reader.py

import io

import os
import unittest

from clp.py import get_name_pairs, CLPError

# -- bad input ------------------------------------------------------

NO_DELIMITER_INPUT = """
hello there
explosion_here  # no space in this line
"""

# -- more bad input -------------------------------------------------
DUPE_LEFT_VALUE_INPUT = """
abc def         # this gets overridden
ghi jkl
abc mno
"""

# -- good input -----------------------------------------------------
TEST_DATA = """# silly comment at top of file



# comment at start of line
        # comment over here

  abc    def                # two spaces there
ghi jkl                     # single space
foo   bar
baz   that_sort_of_thing    # spaces on right side
"""
# -- end good input -------------------------------------------------


class TestNamePairReader(unittest.TestCase):
    """ Confirm that a readable name-pair list behaves as expected. """

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_empty_in_stream(self):
        """ Verify that an empty input stream raises an exception. """
        in_stream = io.StringIO('')
        try:
            _ = get_name_pairs(in_stream)
            self.fail("didn't raise on empty input")
        except CLPError as err:
            pass

    def test_ill_formed_input(self):
        """ Verify that an input line without a delimiter raises an exception. """
        in_stream = io.StringIO(NO_DELIMITER_INPUT)
        with self.assertRaises(CLPError):
            pairs = get_name_pairs(in_stream)

    def test_dupe_left_input(self):
        """ Verify that input with duplicate keys raises. """
        in_stream = io.StringIO(DUPE_LEFT_VALUE_INPUT)
        with self.assertRaises(CLPError):
            pairs = get_name_pairs(in_stream)

    def test_name_pair_reader(self):
        """ Verify that good input produces the expected list of pairs. """

        in_stream = io.StringIO(TEST_DATA)
        pairs = get_name_pairs(in_stream)
        self.assertEqual(len(pairs), 4)

        self.assertTrue('abc' in pairs)
        self.assertTrue('baz' in pairs)
        self.assertTrue('foo' in pairs)
        self.assertTrue('ghi' in pairs)

        self.assertEqual(pairs['abc'], 'def')
        self.assertEqual(pairs['baz'], 'that_sort_of_thing')
        self.assertEqual(pairs['foo'], 'bar')
        self.assertEqual(pairs['ghi'], 'jkl')


if __name__ == '__main__':
    unittest.main()
