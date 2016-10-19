#!/usr/bin/env python3

# clp/test_infile_a.py

import io
import os
import unittest

from clp.py import get_name_pairs, rename_in_file, CLPError
from xlattice import Q

FROM_NAME_PAIRS = """# used to go from original to checkpoint
clp newCLP         # new program name (appears three times in strings)
description desc
file foo           # appears twice as variable, three times in comments
"""

BACK_NAME_PAIRS = """# from checkpoint back to original
newCLP clp
desc description
foo file
"""

INPUT_FILE = os.path.join('test_files', 'file_a.py')
OUTPUT_FILE = os.path.join('tmp', 'file_a_output.py')
ROUNDTRIPPED = os.path.join('tmp', 'file_a_roundtripped.py')


class TestFileA(unittest.TestCase):
    """
    Try to round trip files, giving new names to variables and then
    replacing the new names with old ones.
    """

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def do_from_file_a(self):
        """
        Create a set of name pairs, verify that they have expected values.
        """
        in_stream = io.StringIO(FROM_NAME_PAIRS)
        from_pairs = get_name_pairs(in_stream)
        self.assertEqual(len(from_pairs), 3)

        self.assertTrue('clp' in from_pairs)
        self.assertTrue('description' in from_pairs)
        self.assertTrue('file' in from_pairs)

        self.assertEqual(from_pairs['clp'], 'newCLP')
        self.assertEqual(from_pairs['description'], 'desc')
        self.assertEqual(from_pairs['file'], 'foo')

        # read in a program fragment, replace named variables
        os.makedirs('tmp', exist_ok=True)
        self.assertTrue(os.path.exists(INPUT_FILE))

        data_out, counts, old_hash, new_hash = rename_in_file(
            INPUT_FILE, from_pairs, Q.USING_SHA1, OUTPUT_FILE)

        self.assertTrue('clp' in counts)
        self.assertEqual(counts['clp'], 2)

        self.assertTrue('description' in counts)
        self.assertEqual(counts['description'], 1)

        self.assertTrue('file' in counts)
        self.assertEqual(counts['file'], 2)

        return old_hash, new_hash

    def do_back_to_file_a(self):
        """
        Create a set of name pairs, verify that they have expected values.
        """
        in_stream = io.StringIO(BACK_NAME_PAIRS)
        back_pairs = get_name_pairs(in_stream)
        self.assertEqual(len(back_pairs), 3)

        self.assertTrue('newCLP' in back_pairs)
        self.assertTrue('desc' in back_pairs)
        self.assertTrue('foo' in back_pairs)

        self.assertEqual(back_pairs['newCLP'], 'clp')
        self.assertEqual(back_pairs['desc'], 'description')
        self.assertEqual(back_pairs['foo'], 'file')

        # read in a program fragment, replace named variables
        self.assertTrue(os.path.exists(OUTPUT_FILE))

        data_out, counts, old_hash, new_hash = rename_in_file(
            OUTPUT_FILE, back_pairs, Q.USING_SHA1, ROUNDTRIPPED)

        self.assertTrue('newCLP' in counts)
        self.assertEqual(counts['newCLP'], 2)

        self.assertTrue('desc' in counts)
        self.assertEqual(counts['desc'], 1)

        self.assertTrue('foo' in counts)
        self.assertEqual(counts['foo'], 2)

        return old_hash, new_hash

    def test_file_a(self):
        orig_hash, out_hash = self.do_from_file_a()
        out_hash2, rt_hash = self.do_back_to_file_a()
        self.assertEqual(out_hash2, out_hash)       # should be trivial
        self.assertEqual(orig_hash, rt_hash)        # roundtrip is OK

if __name__ == '__main__':
    unittest.main()
