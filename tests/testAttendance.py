#!/usr/bin/env python3.5
import unittest
from Poorganiser import Attendance


class TestAttendance(unittest.TestCase):
    def test_get_going_status(self):
        at1 = Attendance(4, 2)
        self.assertEqual(at1.get_going_status(), "invited")

        at1 = Attendance(1, 2, "invited", [])
        self.assertEqual(at1.get_going_status(), "invited")

        at1 = Attendance(1, 2, "Going", [])
        self.assertEqual(at1.get_going_status(), "Going")

        at1 = Attendance(1, 2, "Not Going", [])
        self.assertEqual(at1.get_going_status(), "Not Going")

    def test_get_roles(self):
        at1 = Attendance(5, 10)
        self.assertEqual(at1.get_roles(), [])

        at1 = Attendance(32, 198, True, [])
        self.assertEqual(at1.get_roles(), [])

        at1 = Attendance(48, 3230, False, ['bring food'])
        self.assertEqual(at1.get_roles(), ['bring food'])

        at1 = Attendance(1266, 987, True, ['bring food', 'drive'])
        self.assertEqual(at1.get_roles(), ['bring food', 'drive'])

    def test_set_going_status(self):
        at1 = Attendance(1, 1)
        self.assertEqual(at1.get_going_status(), "invited")
        at1.set_going_status("Going")
        self.assertEqual(at1.get_going_status(), "Going")
        at1 = Attendance(43, 103, "Not Going")
        self.assertEqual(at1.get_going_status(), "Not Going")

    def test_add_role(self):
        at1 = Attendance(5, 10, True, [])
        at1.add_role('bring food')
        self.assertEqual(at1.get_roles(), ['bring food'])
        at1.add_role('drive')
        self.assertEqual(at1.get_roles(), ['bring food', 'drive'])
        at1 = Attendance(1032, 39281, False, ['Book venue'])
        at1.add_role('do something')
        at1.add_role('blah')
        self.assertEqual(at1.get_roles(), ['Book venue', 'do something', 'blah'])

    def test_remove_role(self):
        at1 = Attendance(5, 10, True, [])
        at1.add_role('bring food')
        at1.remove_role('bring food')
        self.assertEqual(at1.get_roles(), [])

        at1 = Attendance(321, 290, False, ['a', 'b'])
        at1.remove_role('a')
        self.assertEqual(at1.get_roles(), ['b'])
        at1.remove_role('b')
        self.assertEqual(at1.get_roles(), [])

        # Test removing roles that don't exist - should be None
        self.assertIsNone(at1.remove_role(''))
        self.assertIsNone(at1.remove_role('lol'))
        self.assertIsNone(at1.remove_role(1))
        self.assertIsNone(at1.remove_role(True))

if __name__ == '__main__':
    unittest.main()
