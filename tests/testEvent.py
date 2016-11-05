#!/usr/bin/env python3.5
import unittest
from Event import Event


class TestEvent(unittest.TestCase):
    def test_get_ownerid(self):
        e1 = Event(0, "BBQ", "Parra Park", "01/10/2016")
        self.assertEqual(e1.get_ownerid(), 0)
        e1 = Event(52, "", "house", "01/10/2016")
        self.assertEqual(e1.get_ownerid(), 52)

    def test_set_ownerid(self):
        e1 = Event(0, "BBQ", "Parra Park", "01/10/2016")
        e1.set_ownerid(42)
        self.assertEqual(e1.get_ownerid(), 42)
        e1 = Event(52, "", "house", "01/10/2016")
        e1.set_ownerid(10)
        e1.set_ownerid(33)
        self.assertEqual(e1.get_ownerid(), 33)

    def test_get_name(self):
        e1 = Event(0, "BBQ", "Parra Park", "01/10/2016")
        self.assertEqual(e1.get_name(), "BBQ")
        e1 = Event(0, "", "house", "01/10/2016")
        self.assertEqual(e1.get_name(), "")

    def test_set_name(self):
        e1 = Event(0, "BBQ", "Parra Park", "01/10/2016")
        e1.set_name("name is wrong")
        self.assertEqual(e1.get_name(), "name is wrong")
        e1.set_name("")
        self.assertEqual(e1.get_name(), "")

    def test_get_location(self):
        e1 = Event(0, "BBQ", "Parra Park", "01/10/2016")
        self.assertEqual(e1.get_location(), "Parra Park")
        e1 = Event(0, "BBQ", "", "01/10/2016")
        self.assertEqual(e1.get_location(), "")

    def test_set_location(self):
        e1 = Event(0, "BBQ", "Parra Park", "01/10/2016")
        e1.set_location("Parramatta Park")
        self.assertEqual(e1.get_location(), "Parramatta Park")
        e1.set_location("")
        self.assertEqual(e1.get_location(), "")

    def test_get_time(self):
        e1 = Event(0, "BBQ", "Parra Park", "01/10/2016")
        self.assertEqual(e1.get_time(), "01/10/2016")
        e1 = Event(0, "BBQ", "Parra Park", "")
        self.assertEqual(e1.get_time(), "")

    def test_set_time(self):
        e1 = Event(0, "BBQ", "Parra Park", "01/10/2016")
        e1.set_time("02/10/2016")
        self.assertEqual(e1.get_time(), "02/10/2016")
        e1.set_time("")
        self.assertEqual(e1.get_time(), "")

if __name__ == '__main__':
    unittest.main()
