#!/usr/bin/env python3.5
import unittest
from Poorganiser import Attendance


class TestAttendance(unittest.TestCase):
    def test_constructor_assertions(self):
        # Incorrect user_id type
        with self.assertRaises(AssertionError):
            Attendance(list(), 2)

        with self.assertRaises(AssertionError):
            Attendance(4.3, 2, going_status='not_going')

        with self.assertRaises(AssertionError):
            Attendance('blah', 2, going_status='going', roles=['bring_food'])

        # Incorrect event_id type
        with self.assertRaises(AssertionError):
            Attendance(4, list())

        with self.assertRaises(AssertionError):
            Attendance(4, 4.3)

        with self.assertRaises(AssertionError):
            Attendance(4, 'blah')

        # Incorrect going_status type
        with self.assertRaises(AssertionError):
            Attendance(4, 2, going_status=34)

        with self.assertRaises(AssertionError):
            Attendance(4, 2, going_status=12.34)

        with self.assertRaises(AssertionError):
            Attendance(4, 2, going_status=['going', 'not going'], roles=['food buyer'])

        # Incorrect roles type
        with self.assertRaises(AssertionError):
            Attendance(4, 2, roles=34)

        with self.assertRaises(AssertionError):
            Attendance(4, 2, roles="food buyer")

        with self.assertRaises(AssertionError):
            Attendance(4, 2, roles=("food buyer",))

    def test_get_user_id(self):
        at = Attendance(4, 2)
        self.assertEqual(at.get_user_id(), 4)
        at = Attendance(999, 1000)
        self.assertEqual(at.get_user_id(), 999)
        at = Attendance(1234, 2345)
        self.assertEqual(at.get_user_id(), 1234)

    def test_get_event_id(self):
        at = Attendance(4, 2)
        self.assertEqual(at.get_event_id(), 2)
        at = Attendance(999, 1000)
        self.assertEqual(at.get_event_id(), 1000)
        at = Attendance(1234, 2345)
        self.assertEqual(at.get_event_id(), 2345)

    def test_get_going_status(self):
        at = Attendance(4, 2)
        self.assertEqual(at.get_going_status(), "invited")

        at = Attendance(194, 37, " ", [])
        self.assertEqual(at.get_going_status(), " ")

        at = Attendance(1, 2, "invited", [])
        self.assertEqual(at.get_going_status(), "invited")

        at = Attendance(1, 2, "going", [])
        self.assertEqual(at.get_going_status(), "going")

        at = Attendance(1, 2, "not_going", [])
        self.assertEqual(at.get_going_status(), "not_going")

    def test_get_roles(self):
        at = Attendance(5, 10)
        self.assertEqual(at.get_roles(), [])

        at = Attendance(32, 198, "going", [])
        self.assertEqual(at.get_roles(), [])

        at = Attendance(48, 3230, "not_going", ['bring food'])
        self.assertEqual(at.get_roles(), ['bring food'])

        at = Attendance(1266, 987, "going", ['bring food', 'drive'])
        self.assertEqual(at.get_roles(), ['bring food', 'drive'])

    def test_set_going_status(self):
        at = Attendance(1, 1)
        self.assertEqual(at.get_going_status(), "invited")
        at.set_going_status("going")
        self.assertEqual(at.get_going_status(), "going")
        at = Attendance(43, 103, "not_going")
        self.assertEqual(at.get_going_status(), "not_going")

        # Test setting going_status with invalid types
        with self.assertRaises(AssertionError):
            at.set_going_status(1234)

        with self.assertRaises(AssertionError):
            at.set_going_status(["going"])

        with self.assertRaises(AssertionError):
            at.set_going_status(at)

    def test_add_role(self):
        at = Attendance(5, 10, "going", [])
        at.add_role('bring food')
        self.assertEqual(at.get_roles(), ['bring food'])
        at.add_role('drive')
        self.assertEqual(at.get_roles(), ['bring food', 'drive'])
        at = Attendance(1032, 39281, "not_going", ['Book venue'])
        at.add_role('do something')
        at.add_role('blah')
        self.assertEqual(at.get_roles(), ['Book venue', 'do something', 'blah'])

        # Test setting role with invalid types
        with self.assertRaises(AssertionError):
            at.add_role(1234)

        with self.assertRaises(AssertionError):
            at.add_role(["food buyer"])

        with self.assertRaises(AssertionError):
            at.add_role(at)

    def test_remove_role(self):
        at = Attendance(5, 10, "going", [])
        at.add_role('bring food')
        at.remove_role('bring food')
        self.assertEqual(at.get_roles(), [])

        at = Attendance(321, 290, "not_going", ['a', 'b'])
        at.remove_role('a')
        self.assertEqual(at.get_roles(), ['b'])
        at.remove_role('b')
        self.assertEqual(at.get_roles(), [])

        # Test removing roles that don't exist - should be None
        self.assertIsNone(at.remove_role(''))
        self.assertIsNone(at.remove_role('lol'))
        self.assertIsNone(at.remove_role(1))
        self.assertIsNone(at.remove_role(True))

if __name__ == '__main__':
    unittest.main()
