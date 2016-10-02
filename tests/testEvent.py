#!/usr/bin/env python3.5
import unittest
from Event import Event

class TestEvent(unittest.TestCase):
    pass
    # def test_get_name(self):
    #     e1 = Event("BBQ", "Parra Park", "01/10/2016")
    #     self.assertEqual(e1.get_name(), "BBQ")
    #     e1 = Event("", "house", "01/10/2016")
    #     self.assertEqual(e1.get_name(), "")
    #
    # def test_set_name(self):
    #     e1 = Event("BBQ", "Parra Park", "01/10/2016")
    #     e1.set_name("name is wrong")
    #     self.assertEqual(e1.get_name(), "name is wrong")
    #     e1.set_name("")
    #     self.assertEqual(e1.get_name(), "")
    #
    # def test_get_location(self):
    #     e1 = Event("BBQ", "Parra Park", "01/10/2016")
    #     self.assertEqual(e1.get_location(), "Parra Park")
    #     e1 = Event("BBQ", "", "01/10/2016")
    #     self.assertEqual(e1.get_location(), "")
    #
    # def test_get_attendee(self):
    #     e1 = Event("BBQ", "Parra Park", "01/10/2016")
    #     self.assertIsNone(e1.get_attendee('Bob'))
    #     e1 = Event("", "", "")
    #     self.assertIsNone(e1.get_attendee('Jane'))
    #
    # def test_get_attendees(self):
    #     e1 = Event("BBQ", "Parra Park", "01/10/2016")
    #     self.assertEqual(e1.get_attendees(), {})
    #     e1 = Event("", "", "")
    #     self.assertEqual(e1.get_attendees(), {})
    #
    # def test_add_attendee(self):
    #     e1 = Event("BBQ", "Parra Park", "01/10/2016")
    #     self.assertIsNone(e1.get_attendee('Bob'))
    #     e1.add_attendee('Bob')
    #     self.assertEqual(e1.get_attendee('Bob').get_username(), 'Bob')
    #     self.assertNotEqual(e1.get_attendees, {})
    #
    #     e1.add_attendee('Jane')
    #     assert(e1.get_attendee('Jane').get_username() == 'Jane')
    #
    # def test_set_location(self):
    #     e1 = Event("BBQ", "Parra Park", "01/10/2016")
    #     e1.set_location("Parramatta Park")
    #     self.assertEqual(e1.get_location(), "Parramatta Park")
    #     e1.set_location("")
    #     self.assertEqual(e1.get_location(), "")
    #
    # def test_get_time(self):
    #     e1 = Event("BBQ", "Parra Park", "01/10/2016")
    #     self.assertEqual(e1.get_time(), "01/10/2016")
    #     e1 = Event("BBQ", "Parra Park", "")
    #     self.assertEqual(e1.get_time(), "")
    #
    # def test_set_time(self):
    #     e1 = Event("BBQ", "Parra Park", "01/10/2016")
    #     e1.set_time("02/10/2016")
    #     self.assertEqual(e1.get_time(), "02/10/2016")
    #     e1.set_time("")
    #     self.assertEqual(e1.get_time(), "")

if __name__ == '__main__':
    unittest.main()
