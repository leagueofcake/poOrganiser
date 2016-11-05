#!/usr/bin/env python3.5
import unittest
from EventUser import EventUser


class TestEvent(unittest.TestCase):
    def test_get_isgoing(self):
        eu1 = EventUser(4, 2)
        self.assertEqual(eu1.get_isgoing(), "Invited")

        eu1 = EventUser(1, 2, "Invited", [])
        self.assertEqual(eu1.get_isgoing(), "Invited")

        eu1 = EventUser(1, 2, "Going", [])
        self.assertEqual(eu1.get_isgoing(), "Going")

        eu1 = EventUser(1, 2, "Not Going", [])
        self.assertEqual(eu1.get_isgoing(), "Not Going")

    def test_get_roles(self):
        eu1 = EventUser(5, 10)
        self.assertEqual(eu1.get_roles(), [])

        eu1 = EventUser(32, 198, True, [])
        self.assertEqual(eu1.get_roles(), [])

        eu1 = EventUser(48, 3230, False, ['bring food'])
        self.assertEqual(eu1.get_roles(), ['bring food'])

        eu1 = EventUser(1266, 987, True, ['bring food', 'drive'])
        self.assertEqual(eu1.get_roles(), ['bring food', 'drive'])

    def test_set_isgoing(self):
        eu1 = EventUser(1, 1)
        self.assertEqual(eu1.get_isgoing(), "Invited")
        eu1.set_isgoing("Going")
        self.assertEqual(eu1.get_isgoing(), "Going")
        eu1 = EventUser(43, 103, "Not Going")
        self.assertEqual(eu1.get_isgoing(), "Not Going")

    def test_add_role(self):
        eu1 = EventUser(5, 10, True, [])
        eu1.add_role('bring food')
        self.assertEqual(eu1.get_roles(), ['bring food'])
        eu1.add_role('drive')
        self.assertEqual(eu1.get_roles(), ['bring food', 'drive'])
        eu1 = EventUser(1032, 39281, False, ['Book venue'])
        eu1.add_role('do something')
        eu1.add_role('blah')
        self.assertEqual(eu1.get_roles(), ['Book venue', 'do something', 'blah'])

    def test_remove_role(self):
        eu1 = EventUser(5, 10, True, [])
        eu1.add_role('bring food')
        eu1.remove_role('bring food')
        self.assertEqual(eu1.get_roles(), [])

        eu1 = EventUser(321, 290, False, ['a', 'b'])
        eu1.remove_role('a')
        self.assertEqual(eu1.get_roles(), ['b'])
        eu1.remove_role('b')
        self.assertEqual(eu1.get_roles(), [])

        # Test removing roles that don't exist - should be None
        self.assertIsNone(eu1.remove_role(''))
        self.assertIsNone(eu1.remove_role('lol'))
        self.assertIsNone(eu1.remove_role(1))
        self.assertIsNone(eu1.remove_role(True))

if __name__ == '__main__':
    unittest.main()
