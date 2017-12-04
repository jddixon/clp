#!/usr/bin/env python3

# clp/test_list_serializer.py

""" Test list srialization. """

import unittest
from clp import serialize_str_list


class TestUtils(unittest.TestCase):
    """ Test list srialization. """

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_serializating0(self):
        """ Test serializing empty list. """
        name = 'scripts'
        indent = 8
        elements = []
        expect0 = "        scripts=[]"
        actual = serialize_str_list(name, indent, elements)
        self.assertEqual(len(actual), 1)
        self.assertEqual(actual[0], expect0)

    def test_serializating1(self):
        """ Test serializing single-line list. """
        name = 'scripts'
        indent = 8
        elements = ['src/bl_check', 'src/bl_createtestdata1', 'src/bl_listgen']
        expect0 = "        scripts=['src/bl_check', " +\
                  "'src/bl_createtestdata1', 'src/bl_listgen']"
        actual = serialize_str_list(name, indent, elements)
        self.assertEqual(len(actual), 1)
        self.assertEqual(actual[0], expect0)

    def test_serializating2(self):
        """ Test serializing two-liner. """
        name = 'scripts'
        indent = 8
        elements = ['src/bl_check', 'src/bl_createtestdata1',
                    'src/bl_listgen', 'src/bl_srcgen']
        expect0 = "        scripts=['src/bl_check', " + \
                  "'src/bl_createtestdata1', 'src/bl_listgen',"
        expect1 = "                 'src/bl_srcgen']"
        actual = serialize_str_list(name, indent, elements)
        self.assertEqual(len(actual), 2)
        self.assertEqual(actual[0], expect0)
        self.assertEqual(actual[1], expect1)

    def test_serializating3(self):
        """ Test serializing three-liner. """
        name = 'scripts'
        indent = 8
        elements = ['src/bl_check', 'src/bl_createtestdata1',
                    'src/bl_listgen', 'src/bl_srcgen',
                    'foo', 'doo', 'bedoo', 'aVeryLongArgumentAtTheEnd']
        expect0 = "        scripts=['src/bl_check', " +\
                  "'src/bl_createtestdata1', 'src/bl_listgen',"
        expect1 = "                 'src/bl_srcgen', 'foo', 'doo', 'bedoo',"
        expect2 = "                 'aVeryLongArgumentAtTheEnd']"
        actual = serialize_str_list(name, indent, elements)
        self.assertEqual(len(actual), 3)
        self.assertEqual(actual[0], expect0)
        self.assertEqual(actual[1], expect1)
        self.assertEqual(actual[2], expect2)


if __name__ == '__main__':
    unittest.main()
