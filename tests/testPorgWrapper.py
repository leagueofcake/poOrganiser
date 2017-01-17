#!/usr/bin/env python3.5
import sqlite3
import unittest
from datetime import datetime, timedelta

import sqlalchemy.exc
from config import porg_config
from gen_db import generate as generate_db
from Poorganiser import User, Event, Attendance
from PorgWrapper import PorgWrapper
from PorgExceptions import *


class TestPorgWrapper(unittest.TestCase):
    def setUp(self):
        generate_db(c)  # Generate blank database

    def tearDown(self):
        pass
        # generate_db(c)  # Generate blank database

    def test_get_user_by_username(self):
        self.assertIsNone(p.get_user_by_username("bob"))
        self.assertIsNone(p.get_user_by_username("jane"))

    def test_register_user(self):
        # Check that no users currently exist with usernames "bob"/"dave and friends"
        self.assertIsNone(p.get_user_by_username("bob"))
        self.assertIsNone(p.get_user_by_username("dave and friends"))

        u = p.register_user("bob")
        self.assertEqual(u.get_username(), "bob")
        self.assertEqual(u.get_events_organised_ids(), [])
        self.assertEqual(u.get_events_attending_ids(), [])

        u = p.register_user("dave and friends")
        self.assertEqual(u.get_username(), "dave and friends")
        self.assertEqual(u.get_events_organised_ids(), [])
        self.assertEqual(u.get_events_attending_ids(), [])

        # Test querying created users from database
        u2 = p.get_user_by_username("bob")
        self.assertTrue(isinstance(u2, User))
        self.assertEqual(u2.get_username(), "bob")
        self.assertEqual(u2.get_events_organised_ids(), [])
        self.assertEqual(u2.get_events_attending_ids(), [])

        u2 = p.get_user_by_username("dave and friends")
        self.assertTrue(isinstance(u2, User))
        self.assertEqual(u2.get_username(), "dave and friends")
        self.assertEqual(u2.get_events_organised_ids(), [])
        self.assertEqual(u2.get_events_attending_ids(), [])

        # Check that re-registering same username raises UserRegisteredError
        with self.assertRaises(UserRegisteredError):
            p.register_user("bob")

        with self.assertRaises(UserRegisteredError):
            p.register_user("dave and friends")

    def test_unregister_user(self):
        # Register some users
        u1 = p.register_user("bob")
        u2 = p.register_user("jane")
        u3 = p.register_user("noot noot")

        # Create some events
        e1 = p.create_event(u1, "event 1")
        e2 = p.create_event(u2.get_id(), "event 2")
        e3 = p.create_event(u2, "event 3", location="blob street")
        self.assertEqual(u1.get_events_organised_ids(), [e1.get_id()])
        self.assertEqual(u2.get_events_organised_ids(), [e2.get_id(), e3.get_id()])

        # Unregister created users
        p.unregister_user(u1)  # Only delete attendances - event should still exist
        self.assertIsNone(e1.get_owner_id())  # Check owner_id is removed from Event
        self.assertIsNotNone(p.db_interface.get_obj(e1.get_id(), Event))
        self.assertIsNone(p.get_attendance(u1.get_id(), e1.get_id()))  # Check attendance deleted

        p.unregister_user("jane", delete_events=True)  # Delete attedances and events
        self.assertIsNone(p.db_interface.get_obj(e2.get_id(), Event))
        self.assertIsNone(p.db_interface.get_obj(e2.get_id(), Event))
        self.assertIsNone(p.get_attendance(u2.get_id(), e2.get_id()))  # Check attendance deleted
        self.assertIsNone(p.get_attendance(u2.get_id(), e3.get_id()))  # Check attendance deleted

        p.unregister_user(u3)

        # Try unregister users that have already been unregistered
        with self.assertRaises(UserNotFoundError):
            p.unregister_user("bob")

        with self.assertRaises(UserNotFoundError):
            p.unregister_user(u2)

        with self.assertRaises(UserNotFoundError):
            p.unregister_user("noot noot")

        # Try unregister users that don't exist
        with self.assertRaises(UserNotFoundError):
            p.unregister_user("blargh")

        with self.assertRaises(UserNotFoundError):
            p.unregister_user("1234")

        with self.assertRaises(UserNotFoundError):
            p.unregister_user(1234)

    def test_get_curr_events(self):
        # Sanity check - no events initially
        curr_events = p.get_curr_events()
        self.assertEqual(curr_events, [])

        # Create some users
        u1 = p.register_user("bob")
        u2 = p.register_user("josh")

        # Sanity checks - u1 and u2 have correct ids
        self.assertEqual(u1.get_id(), 1)
        self.assertEqual(u2.get_id(), 2)

        # Create some events
        e1 = p.create_event(1, "event 1")
        e2 = p.create_event(2, "event 2", location="location 2")
        e3 = p.create_event(2, "event 3", time=datetime.today() + timedelta(days=10))

        # Check current events are as expected
        curr_events = p.get_curr_events()
        self.assertEqual(curr_events, [e1, e2, e3])

        # Create events dated before today, check they don't appear in curr_events
        before_yesterday = datetime.today() - timedelta(days=134)
        yesterday = datetime.today() - timedelta(days=1)
        p.create_event(1, "event 4", time=yesterday, location="location 4")
        p.create_event(1, "event 5", time=before_yesterday)
        curr_events = p.get_curr_events()
        self.assertEqual(curr_events, [e1, e2, e3])

    def test_get_events_by_user(self):
        # Create some users
        u1 = p.register_user("jane")
        u2 = p.register_user("user 2")

        # Sanity checks - u1 and u2 have correct ids
        self.assertEqual(u1.get_id(), 1)
        self.assertEqual(u2.get_id(), 2)

        # Check that u1 and u2 don't have events
        u1_events = p.get_events_by_user(u1)
        u2_events = p.get_events_by_user(u2.get_id())
        self.assertEqual(u1_events, [])
        self.assertEqual(u2_events, [])

        # Create some events for u1
        e1 = p.create_event(u1.get_id(), "event 1a")
        u1_events = p.get_events_by_user(u1)
        self.assertEqual(u1_events, [e1])

        e2 = p.create_event(u1, "event 2a")
        u1_events = p.get_events_by_user(u1.get_id())
        self.assertEqual(u1_events, [e1, e2])

        # Create some events for u2, check none of u1's events were added to u2
        u2_events = p.get_events_by_user(u2)
        self.assertEqual(u2_events, [])
        e3 = p.create_event(u2, "event 1b")
        u2_events = p.get_events_by_user(u2)
        self.assertEqual(u2_events, [e3])

        e4 = p.create_event(u2.get_id(), "event 2b")
        u2_events = p.get_events_by_user(u2)
        self.assertEqual(u2_events, [e3, e4])

        # Check event deletions
        p.delete_event(e4)
        u2_events = p.get_events_by_user(u2)
        self.assertEqual(u2_events, [e3])

        p.delete_event(e3)
        u2_events = p.get_events_by_user(u2)
        self.assertEqual(u2_events, [])

    def test_get_all_events(self):
        # Check there are no events at the beginning
        events = p.get_all_events()
        self.assertEqual(events, [])

        # Create some users
        u1 = p.register_user("user 1")

        # Add some events
        e1 = p.create_event(u1.get_id(), "event 1")

        all_events = p.get_all_events()
        self.assertEqual(all_events, [e1])

        e2 = p.create_event(u1.get_id(), "event 2", location="loc1")
        all_events = p.get_all_events()
        self.assertEqual(all_events, [e1, e2])

        yesterday = datetime.today() - timedelta(days=1)
        e3 = p.create_event(u1.get_id(), "event 3", time=yesterday)
        all_events = p.get_all_events()
        self.assertEqual(all_events, [e1, e2, e3])

    def test_create_event(self):
        # Create some users
        u1 = p.register_user("user_1")
        u2 = p.register_user("the second UsEr")

        # Sanity checks
        self.assertEqual(u1.get_id(), 1)
        self.assertEqual(u2.get_id(), 2)

        # Create some events
        # No specified location/time
        e1 = p.create_event(u1.get_id(), "event 1")
        a1 = p.get_attendance(u1.get_id(), e1.get_id())
        self.assertEqual(e1.get_id(), 1)
        self.assertEqual(e1.get_name(), "event 1")
        self.assertIsNone(e1.get_location())
        self.assertIsNone(e1.get_time())
        self.assertEqual(p.get_attendances(e1), [a1])

        # Check events_organised_ids and events_attending_ids for u1
        self.assertEqual(u1.get_events_organised_ids(), [e1.get_id()])
        self.assertEqual(u1.get_events_attending_ids(), [e1.get_id()])

        # Check auto-created attendance for e1
        self.assertEqual(a1.get_user_id(), u1.get_id())
        self.assertEqual(a1.get_event_id(), e1.get_id())
        self.assertEqual(a1.get_going_status(), "going")
        self.assertEqual(a1.get_roles(), ["organiser"])

        # Specified location, no specified time
        e2 = p.create_event(u1.get_id(), "event 2", location="somewhere over there")
        a2 = p.get_attendance(u1.get_id(), e2.get_id())
        self.assertEqual(e2.get_name(), "event 2")
        self.assertEqual(e2.get_location(), "somewhere over there")
        self.assertIsNone(e2.get_time())
        self.assertEqual(p.get_attendances(e2), [a2])

        # Check events_organised_ids and events_attending_ids for u1
        self.assertEqual(u1.get_events_organised_ids(), [e1.get_id(), e2.get_id()])
        self.assertEqual(u1.get_events_attending_ids(), [e1.get_id(), e2.get_id()])

        # Check auto-created attendance for e2
        self.assertEqual(a2.get_user_id(), u1.get_id())
        self.assertEqual(a2.get_event_id(), e2.get_id())
        self.assertEqual(a2.get_going_status(), "going")
        self.assertEqual(a2.get_roles(), ["organiser"])

        # Specified time, no specified location
        third_time = datetime(year=2016, month=4, day=1)
        e3 = p.create_event(u1.get_id(), "events are cool", time=third_time)
        a3 = p.get_attendance(u1.get_id(), e3.get_id())
        self.assertEqual(e3.get_name(), "events are cool")
        self.assertIsNone(e3.get_location())
        self.assertEqual(e3.get_time(), third_time)
        self.assertEqual(p.get_attendances(e3), [a3])

        # Check events_organised_ids and events_attending_ids for u1
        self.assertEqual(u1.get_events_organised_ids(), [e1.get_id(), e2.get_id(), e3.get_id()])
        self.assertEqual(u1.get_events_attending_ids(), [e1.get_id(), e2.get_id(), e3.get_id()])

        # Check auto-created attendance for e3
        self.assertEqual(a3.get_user_id(), u1.get_id())
        self.assertEqual(a3.get_event_id(), e3.get_id())
        self.assertEqual(a3.get_going_status(), "going")
        self.assertEqual(a3.get_roles(), ["organiser"])

        # Specified location and time
        fourth_time = datetime(year=2017, month=10, day=25)
        e4 = p.create_event(u2.get_id(), "THE (4th) EVENT", location="not here", time=fourth_time)
        a4 = p.get_attendance(u2.get_id(), e4.get_id())
        self.assertEqual(e4.get_name(), "THE (4th) EVENT")
        self.assertEqual(e4.get_location(), "not here")
        self.assertEqual(e4.get_time(), fourth_time)
        self.assertEqual(p.get_attendances(e4), [a4])

        # Check events_organised_ids and events_attending_ids for u1 and u2
        self.assertEqual(u1.get_events_organised_ids(), [e1.get_id(), e2.get_id(), e3.get_id()])
        self.assertEqual(u1.get_events_attending_ids(), [e1.get_id(), e2.get_id(), e3.get_id()])
        self.assertEqual(u2.get_events_organised_ids(), [e4.get_id()])
        self.assertEqual(u2.get_events_attending_ids(), [e4.get_id()])

        # Check auto-created attendance for e4
        self.assertEqual(a4.get_user_id(), u2.get_id())
        self.assertEqual(a4.get_event_id(), e4.get_id())
        self.assertEqual(a4.get_going_status(), "going")
        self.assertEqual(a4.get_roles(), ["organiser"])

        # Test creating events with user ids that don't exist
        with self.assertRaises(UserNotFoundError):
            p.create_event(0, "fourth invalid event")
        with self.assertRaises(UserNotFoundError):
            p.create_event(1023, "something", location="blah")
        with self.assertRaises(UserNotFoundError):
            p.create_event(-321, "lalalalal", location="alalala", time=fourth_time)

        # Check correct all_events
        all_events = p.get_all_events()
        self.assertEqual(all_events, [e1, e2, e3, e4])

        # Check u1 and u2 still have correct events_organised_ids and events_attending_ids
        self.assertEqual(u1.get_events_organised_ids(), [e1.get_id(), e2.get_id(), e3.get_id()])
        self.assertEqual(u1.get_events_attending_ids(), [e1.get_id(), e2.get_id(), e3.get_id()])
        self.assertEqual(u2.get_events_organised_ids(), [e4.get_id()])
        self.assertEqual(u2.get_events_attending_ids(), [e4.get_id()])

    def test_delete_event(self):
        # Create some users
        u1 = p.register_user("user1")
        u2 = p.register_user("ThE sEcOnD uSeR")

        # Create some events
        e1 = p.create_event(u1.get_id(), "event 1")
        e2 = p.create_event(u2.get_id(), "two to 2 too")
        e3 = p.create_event(u1.get_id(), "free threes")

        a1 = p.get_attendance(u1.get_id(), e1.get_id())
        a2 = p.get_attendance(u2.get_id(), e2.get_id())
        a3 = p.get_attendance(u1.get_id(), e3.get_id())

        # Check events_organising_ids and events_attending_ids for u1 and u2
        self.assertEqual(u1.get_events_organised_ids(), [e1.get_id(), e3.get_id()])
        self.assertEqual(u1.get_events_attending_ids(), [e1.get_id(), e3.get_id()])
        self.assertEqual(u2.get_events_organised_ids(), [e2.get_id()])
        self.assertEqual(u2.get_events_attending_ids(), [e2.get_id()])

        # Check attendances for created events
        self.assertEqual(p.get_attendances(e1), [a1])
        self.assertEqual(p.get_attendances(e2), [a2])
        self.assertEqual(p.get_attendances(e3), [a3])

        # Delete e1
        p.delete_event(e1)

        # Check user's events_organised_ids and events_attending_ids were removed
        self.assertEqual(u1.get_events_organised_ids(), [e3.get_id()])
        self.assertEqual(u1.get_events_attending_ids(), [e3.get_id()])

        # Check attendances were removed
        self.assertIsNone(p.get_attendance(u1.get_id(), e1.get_id()))

        # Delete e2 by id
        p.delete_event(e2.get_id())

        # Check user's events_organised_ids and events_attending_ids were removed
        self.assertEqual(u2.get_events_organised_ids(), [])
        self.assertEqual(u2.get_events_attending_ids(), [])

        # Check attendances were removed
        self.assertIsNone(p.get_attendance(u2.get_id(), e2.get_id()))

        # Delete e3
        p.delete_event(e3)

        # Check user's events_organised_ids and events_attending_ids were removed
        self.assertEqual(u1.get_events_organised_ids(), [])
        self.assertEqual(u1.get_events_attending_ids(), [])

        # Check attendances were removed
        self.assertIsNone(p.get_attendance(u1.get_id(), e3.get_id()))

        # Try delete events that don't exist in database
        with self.assertRaises(EventNotFoundError):
            p.delete_event(e1)

        with self.assertRaises(EventNotFoundError):
            p.delete_event(e3)

        with self.assertRaises(EventNotFoundError):
            p.delete_event(103)

        with self.assertRaises(EventNotFoundError):
            p.delete_event(Event(u1.get_id(), "some event"))

        # Try delete events with owners that no longer exist in database
        e4 = p.create_event(u1.get_id(), "event_to_be_deleted")
        p.unregister_user(u1)
        p.delete_event(e4)

        # Check no more events returned by get_curr_events and get_all_events
        self.assertEqual(p.get_curr_events(), [])
        self.assertEqual(p.get_all_events(), [])

    def test_get_attendance(self):
        # Create some users
        u1 = p.register_user("u1")
        u2 = p.register_user("u2")
        u3 = p.register_user("u3")

        # Create some events
        e1 = p.create_event(u1, "e1")
        a1 = p.get_attendance(u1.get_id(), e1.get_id())

        # Check fields for auto-created Attendance for e1
        self.assertEqual(a1.get_user_id(), u1.get_id())
        self.assertEqual(a1.get_event_id(), e1.get_id())
        self.assertEqual(a1.get_going_status(), "going")
        self.assertEqual(a1.get_roles(), ['organiser'])

        # Create attendance
        a2 = p.create_attendance(u2, e1)
        a2_gotten = p.get_attendance(u2, e1)
        self.assertEqual(a2_gotten.get_user_id(), u2.get_id())
        self.assertEqual(a2_gotten.get_event_id(), e1.get_id())
        self.assertEqual(a2.get_going_status(), "invited")
        self.assertEqual(a2.get_roles(), [])
        self.assertEqual(a2, a2_gotten)

        e2 = p.create_event(u3, "e2")
        a2 = p.get_attendance(u3, e2)

        # Check fields for auto-created Attendance for e2
        self.assertEqual(a2.get_user_id(), u3.get_id())
        self.assertEqual(a2.get_event_id(), e2.get_id())
        self.assertEqual(a2.get_going_status(), "going")
        self.assertEqual(a2.get_roles(), ['organiser'])

        # Create attendance
        a3 = p.create_attendance(u2, e2, going_status="maybe")
        a3_gotten = p.get_attendance(u2, e2)
        self.assertEqual(a3.get_user_id(), u2.get_id())
        self.assertEqual(a3.get_event_id(), e2.get_id())
        self.assertEqual(a3.get_going_status(), "maybe")
        self.assertEqual(a3.get_roles(), [])
        self.assertEqual(a3, a3_gotten)

        a4 = p.create_attendance(u1, e2, going_status="invited", roles=["food buyer", "driver"])
        a4_gotten = p.get_attendance(u1, e2)
        self.assertEqual(a4.get_user_id(), u1.get_id())
        self.assertEqual(a4.get_event_id(), e2.get_id())
        self.assertEqual(a4.get_going_status(), "invited")
        self.assertEqual(a4.get_roles(), ['food buyer', 'driver'])
        self.assertEqual(a4, a4_gotten)

    def test_get_attendances(self):
        # TODO
        pass

    def test_create_attendance(self):
        # TODO
        pass

    def test_delete_attendance(self):
        # TODO
        pass

# Generate empty test database
conn = sqlite3.connect(porg_config.DB_NAME)
c = conn.cursor()
generate_db(c)

# Create PorgWrapper
p = PorgWrapper()

if __name__ == '__main__':
    unittest.main()
