#!/usr/bin/env python3.5
import unittest
from Poorganiser import Event, Attendance, Survey
from datetime import datetime


class TestEvent(unittest.TestCase):
    def test_constructor_assertions(self):
        # Incorrect owner_id type
        with self.assertRaises(AssertionError):
            Event("BBQ", "bob",  "Parra Park", datetime(2016, 10, 1))

        with self.assertRaises(AssertionError):
            Event("BBQ", 3.14,  "Parra Park", datetime(2016, 10, 2))

        with self.assertRaises(AssertionError):
            Event("BBQ", tuple(),  "Parra Park", datetime(2016, 10, 3))

        # Incorrect name type
        with self.assertRaises(AssertionError):
            Event(123, 0,  "Parra Park", datetime(2016, 10, 1))

        with self.assertRaises(AssertionError):
            Event(['name 1', 52,  'name 2'], "Parra Park", datetime(2016, 10, 2))

        with self.assertRaises(AssertionError):
            Event(3.14, 245,  "Parra Park", datetime(2016, 10, 3))

        # Incorrect location type
        with self.assertRaises(AssertionError):
            Event("BBQ", 0,  1234, datetime(2016, 10, 1))

        with self.assertRaises(AssertionError):
            Event("BBQ2", 52,  ['loc 1', 'loc 2'], datetime(2016, 10, 2))

        with self.assertRaises(AssertionError):
            Event("BBQ3", 245,  datetime(2017, 1, 1), datetime(2016, 10, 3))

        # Incorrect time type
        with self.assertRaises(AssertionError):
            Event("BBQ", 0,  "Parra Park", "01/01/2017")

        with self.assertRaises(AssertionError):
            Event("BBQ2", 52,  "Parra Park", 3.14)

        with self.assertRaises(AssertionError):
            Event("BBQ3", 245,  "Parra Park 2", [datetime(2017, 1, 1)])

        # Incorrect survey_ids type
        with self.assertRaises(AssertionError):
            Event("BBQ3", 245,  "Parra Park 2", [datetime(2017, 1, 1)], survey_ids=[1, 3, 5, 7.2])

        with self.assertRaises(AssertionError):
            Event("BBQ3", 245, "Parra Park 2", [datetime(2017, 1, 1)], survey_ids="lolol")

    def test_get_owner_id(self):
        e1 = Event("BBQ", 0,  "Parra Park", datetime(2016, 10, 1))
        self.assertEqual(e1.get_owner_id(), 0)
        e1 = Event("", 52,  "house", datetime(2016, 10, 1))
        self.assertEqual(e1.get_owner_id(), 52)

    def test_get_name(self):
        e1 = Event("BBQ", 0,  "Parra Park", datetime(2016, 10, 1))
        self.assertEqual(e1.get_name(), "BBQ")
        e1 = Event("", 0,  "house", datetime(2016, 10, 1))
        self.assertEqual(e1.get_name(), "")

    def test_get_location(self):
        e1 = Event("BBQ", 0,  "Parra Park", datetime(2016, 10, 1))
        self.assertEqual(e1.get_location(), "Parra Park")
        e1 = Event("BBQ", 0,  "", datetime(2016, 10, 1))
        self.assertEqual(e1.get_location(), "")

    def test_get_time(self):
        e1 = Event("BBQ", 0,  "Parra Park", datetime(2016, 10, 1))
        self.assertEqual(e1.get_time(), datetime(2016, 10, 1))
        e1 = Event("BBQ", 0,  "Parra Park", datetime(2017, 1, 1))
        self.assertEqual(e1.get_time(), datetime(2017, 1, 1))

    def test_set_owner_id(self):
        e1 = Event("BBQ", 0,  "Parra Park", datetime(2016, 10, 1))
        e1.set_owner_id(42)
        self.assertEqual(e1.get_owner_id(), 42)
        e1 = Event("", 52,  "house", datetime(2016, 10, 1))
        e1.set_owner_id(10)
        e1.set_owner_id(33)
        self.assertEqual(e1.get_owner_id(), 33)
        e1.set_owner_id(None)
        self.assertIsNone(e1.get_owner_id())

        # Test setting owner_ids with invalid types
        with self.assertRaises(AssertionError):
            e1.set_owner_id("bob")

        with self.assertRaises(AssertionError):
            e1.set_owner_id(e1)

        with self.assertRaises(AssertionError):
            e1.set_owner_id(3.14)

    def test_set_name(self):
        e1 = Event("BBQ", 0,  "Parra Park", datetime(2016, 10, 1))
        e1.set_name("name is wrong")
        self.assertEqual(e1.get_name(), "name is wrong")
        e1.set_name("")
        self.assertEqual(e1.get_name(), "")

        # Test setting names with invalid types
        with self.assertRaises(AssertionError):
            e1.set_name(123)

        with self.assertRaises(AssertionError):
            e1.set_name(1.234)

        with self.assertRaises(AssertionError):
            e1.set_name(e1)

    def test_set_location(self):
        e1 = Event("BBQ", 0,  "Parra Park", datetime(2016, 10, 1))
        e1.set_location("Parramatta Park")
        self.assertEqual(e1.get_location(), "Parramatta Park")
        e1.set_location("")
        self.assertEqual(e1.get_location(), "")

        # Test setting locations with invalid types
        with self.assertRaises(AssertionError):
            e1.set_location(123)

        with self.assertRaises(AssertionError):
            e1.set_location(1.234)

        with self.assertRaises(AssertionError):
            e1.set_location(e1)

    def test_set_time(self):
        e1 = Event("BBQ", 0,  "Parra Park", datetime(2016, 10, 1))
        e1.set_time(datetime(2016, 10, 2))
        self.assertEqual(e1.get_time(), datetime(2016, 10, 2))
        e1.set_time(datetime(2017, 1, 1))
        self.assertEqual(e1.get_time(), datetime(2017, 1, 1))

        # Test setting times with invalid types
        with self.assertRaises(AssertionError):
            e1.set_time(123)

        with self.assertRaises(AssertionError):
            e1.set_time(1.234)

        with self.assertRaises(AssertionError):
            e1.set_time(e1)

        with self.assertRaises(AssertionError):
            e1.set_time("01/01/2001")

    def test_add_attendance_id(self):
        e1 = Event("BBQ", 0,  "Parra Park", datetime(2016, 10, 1))

        # Test adding attendance ids with integers
        e1.add_attendance_id(1)
        self.assertEqual(e1.get_attendance_ids(), [1])
        e1.add_attendance_id(24)
        self.assertEqual(e1.get_attendance_ids(), [1, 24])

        # Test adding attendance ids with mock Attendance objects
        mock_a1 = Attendance(1, 1)
        mock_a1.id = 35
        e1.add_attendance_id(mock_a1)
        self.assertEqual(e1.get_attendance_ids(), [1, 24, 35])

        mock_a2 = Attendance(34, 1)
        mock_a2.id = 490
        e1.add_attendance_id(mock_a2)
        self.assertEqual(e1.get_attendance_ids(), [1, 24, 35, 490])

        # Test adding attendance ids with invalid types
        with self.assertRaises(TypeError):
            e1.add_attendance_id("bob")

        with self.assertRaises(TypeError):
            e1.add_attendance_id(3.14)

        with self.assertRaises(TypeError):
            e1.add_attendance_id([1, 2])

    def test_remove_attendance_id(self):
        e1 = Event("BBQ", 0,  "Parra Park", datetime(2016, 10, 1))
        e1.add_attendance_id(1)
        self.assertEqual(e1.get_attendance_ids(), [1])
        e1.add_attendance_id(24)
        self.assertEqual(e1.get_attendance_ids(), [1, 24])

        # Test removing attendance ids with integers
        e1.remove_attendance_id(1)
        self.assertEqual(e1.get_attendance_ids(), [24])

        mock_a1 = Attendance(1, 1)
        mock_a1.id = 35
        e1.add_attendance_id(mock_a1)
        self.assertEqual(e1.get_attendance_ids(), [24, 35])

        mock_a2 = Attendance(34, 1)
        mock_a2.id = 490
        e1.add_attendance_id(mock_a2)
        self.assertEqual(e1.get_attendance_ids(), [24, 35, 490])

        # Test removing attendance id that doesn't exist
        e1.remove_attendance_id(999)
        self.assertEqual(e1.get_attendance_ids(), [24, 35, 490])

        # Test removing attendance ids with mock Attendance objects
        e1.remove_attendance_id(mock_a1)
        self.assertEqual(e1.get_attendance_ids(), [24, 490])

        e1.remove_attendance_id(24)
        self.assertEqual(e1.get_attendance_ids(), [490])

        e1.remove_attendance_id(490)
        self.assertEqual(e1.get_attendance_ids(), [])

        # Test removing attendance id that doesn't exist
        e1.remove_attendance_id(490)
        self.assertEqual(e1.get_attendance_ids(), [])

        # Test removing attendance ids with invalid types
        with self.assertRaises(TypeError):
            e1.remove_attendance_id("blob")

        with self.assertRaises(TypeError):
            e1.remove_attendance_id(e1)

        with self.assertRaises(TypeError):
            e1.remove_attendance_id(3.14)

    def test_get_attendance_ids(self):
        e1 = Event("BBQ", 0, "Parra Park", datetime(2016, 10, 1))
        self.assertEqual(e1.get_attendance_ids(), [])

        e2 = Event("BBQ", 0, "Parra Park", datetime(2017, 1, 1))
        self.assertEqual(e2.get_attendance_ids(), [])

    def test_get_survey_ids(self):
        e1 = Event("BBQ", 0, "Parra Park", datetime(2016, 10, 1))
        self.assertEqual(e1.get_survey_ids(), [])

        e2 = Event("BBQ", 0, "Parra Park", datetime(2017, 1, 1))
        self.assertEqual(e2.get_survey_ids(), [])

    def test_add_survey_id(self):
        e1 = Event("BBQ", 0, "Parra Park", datetime(2016, 10, 1))
        self.assertEqual(e1.get_survey_ids(), [])
        e1.add_survey_id(123)
        self.assertEqual(e1.get_survey_ids(), [123])
        e1.add_survey_id(123)  # Test adding duplicate
        self.assertEqual(e1.get_survey_ids(), [123])
        e1.add_survey_id(930)
        self.assertEqual(e1.get_survey_ids(), [123, 930])

        # Test adding with mock Survey object
        s_mock = Survey("s1", 3)
        s_mock.id = 29
        e1.add_survey_id(s_mock)
        self.assertEqual(e1.get_survey_ids(), [123, 930, 29])

        # Test adding with invalid survey type
        with self.assertRaises(TypeError):
            e1.add_survey_id(3.14)

        with self.assertRaises(TypeError):
            e1.add_survey_id(e1)

        with self.assertRaises(TypeError):
            e1.add_survey_id("fake event")

    def test_remove_survey_id(self):
        e1 = Event("BBQ", 0, "Parra Park", datetime(2016, 10, 1))
        self.assertEqual(e1.get_survey_ids(), [])
        e1.add_survey_id(123)
        self.assertEqual(e1.get_survey_ids(), [123])
        e1.remove_survey_id(1920)  # Test removing non-existant element
        self.assertEqual(e1.get_survey_ids(), [123])
        e1.add_survey_id(930)
        self.assertEqual(e1.get_survey_ids(), [123, 930])

        # Test removing with mock Survey object
        s_mock = Survey("s1", 3)
        s_mock.id = 29
        e1.remove_survey_id(s_mock)  # Test removing non-existant element
        self.assertEqual(e1.get_survey_ids(), [123, 930])
        s_mock.id = 930
        e1.remove_survey_id(s_mock)
        self.assertEqual(e1.get_survey_ids(), [123])
        e1.remove_survey_id(123)
        self.assertEqual(e1.get_survey_ids(), [])

        # Test removing with invalid survey type
        with self.assertRaises(TypeError):
            e1.remove_survey_id(3.14)

        with self.assertRaises(TypeError):
            e1.remove_survey_id(e1)

        with self.assertRaises(TypeError):
            e1.remove_survey_id("fake event")

if __name__ == '__main__':
    unittest.main()
