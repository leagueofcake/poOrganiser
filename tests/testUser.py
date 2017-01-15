import unittest
from User import User
from Event import Event


class TestUser(unittest.TestCase):
    def test_get_username(self):
        u = User("")
        self.assertEqual(u.get_username(), "")  # Empty case

        u = User(" ")
        self.assertEqual(u.get_username(), " ")  # Whitespace case

        u = User("Jeremy")
        self.assertEqual(u.get_username(), "Jeremy")  # Normal string

        u = User("   Dave and Friends ")
        self.assertEqual(u.get_username(), "   Dave and Friends ")  # Normal string with whitespace

    def test_set_username(self):
        u = User("test")
        self.assertEqual(u.get_username(), "test")  # Check initialisation

        u.set_username("")
        self.assertEqual(u.get_username(), "")  # Blank case

        u.set_username(" ")
        self.assertEqual(u.get_username(), " ")  # Single whitespace

        u.set_username("Dennis")
        self.assertEqual(u.get_username(), "Dennis")  # Normal string

        u.set_username("   Dave and Friends ")
        self.assertEqual(u.get_username(), "   Dave and Friends ")  # Normal string with whitespace

    def test_get_events_organised(self):
        u = User("test")
        self.assertEqual(u.get_events_organised_ids(), [])  # Blank case

        u = User("blahblahblah")
        self.assertEqual(u.get_events_organised_ids(), [])  # Blank case 2

    def test_get_events_attending(self):
        u = User("test")
        self.assertEqual(u.get_events_attending_ids(), [])  # Blank case

        u = User("blahblahblah")
        self.assertEqual(u.get_events_attending_ids(), [])  # Blank case 2

    def test_add_event_organised(self):
        # Adding events with event ids (integers)
        u = User("test")
        u.add_event_organised(1)
        self.assertEqual(u.get_events_organised_ids(), [1])
        u.add_event_organised(4)
        self.assertEqual(u.get_events_organised_ids(), [1, 4])
        u.add_event_organised(2)
        self.assertEqual(u.get_events_organised_ids(), [1, 4, 2])

        # Adding events with Event objects
        e = Event(1, "event", "location", "time")
        e.id = 34
        u.add_event_organised(e)
        self.assertEqual(u.get_events_organised_ids(), [1, 4, 2, 34])

        e = Event(93, "event2", "location2", "time2")
        e.id = 1234
        u.add_event_organised(e)
        self.assertEqual(u.get_events_organised_ids(), [1, 4, 2, 34, 1234])

        # Test adding events with invalid type
        with self.assertRaises(TypeError):
            u.add_event_organised("lol")

        with self.assertRaises(TypeError):
            u.add_event_organised("1234")

        with self.assertRaises(TypeError):
            u.add_event_organised([1, 3, 4])

        with self.assertRaises(TypeError):
            u.add_event_organised(u)

    def test_add_event_attending(self):
        # Adding events with event ids (integers)
        u = User("test")
        u.add_event_attending(1)
        self.assertEqual(u.get_events_attending_ids(), [1])
        u.add_event_attending(4)
        self.assertEqual(u.get_events_attending_ids(), [1, 4])
        u.add_event_attending(2)
        self.assertEqual(u.get_events_attending_ids(), [1, 4, 2])

        # Adding events with Event objects
        e = Event(1, "event", "location", "time")  # Add event using Event object
        e.id = 34
        u.add_event_attending(e)
        self.assertEqual(u.get_events_attending_ids(), [1, 4, 2, 34])

        e = Event(93, "event2", "location2", "time2")
        e.id = 1234
        u.add_event_attending(e)
        self.assertEqual(u.get_events_attending_ids(), [1, 4, 2, 34, 1234])

        # Test adding events with invalid type
        with self.assertRaises(TypeError):
            u.add_event_attending("lol")

        with self.assertRaises(TypeError):
            u.add_event_attending("1234")

        with self.assertRaises(TypeError):
            u.add_event_attending([1, 3, 4])

        with self.assertRaises(TypeError):
            u.add_event_attending(u)

    def test_remove_event_organised(self):
        # Removing events with event ids (integers)
        u = User("test")
        u.add_event_organised(1)
        u.add_event_organised(4)
        u.remove_event_organised(1)
        self.assertEqual(u.get_events_organised_ids(), [4])
        u.add_event_organised(2)
        u.add_event_organised(99)
        u.add_event_organised(1234)
        u.remove_event_organised(99)
        self.assertEqual(u.get_events_organised_ids(), [4, 2, 1234])
        u.remove_event_organised(4)
        self.assertEqual(u.get_events_organised_ids(), [2, 1234])

        # Removing events with Event objects
        e = Event(35, "e", "l", "t")
        e.id = 1234
        u.remove_event_organised(e)
        self.assertEqual(u.get_events_organised_ids(), [2])
        u.remove_event_organised(2)
        self.assertEqual(u.get_events_organised_ids(), [])

        e = Event(1, "event", "location", "time")
        e.id = 34
        u.add_event_organised(e)
        self.assertEqual(u.get_events_organised_ids(), [34])

        e2 = Event(1234, "event2", "location2", "time2")
        e2.id = 834
        u.add_event_organised(e2)
        self.assertEqual(u.get_events_organised_ids(), [34, 834])

        e3 = Event(999, "event3", "location3", "time3")
        e3.id = 99
        u.add_event_organised(e3)
        self.assertEqual(u.get_events_organised_ids(), [34, 834, 99])

        # Finish removing with event ids (integers)
        u.remove_event_organised(e2)
        self.assertEqual(u.get_events_organised_ids(), [34, 99])
        u.remove_event_organised(34)
        self.assertEqual(u.get_events_organised_ids(), [99])
        u.remove_event_organised(e3)
        self.assertEqual(u.get_events_organised_ids(), [])

        # Test removing events that don't exist
        with self.assertRaises(ValueError):
            u.remove_event_organised(e)

        with self.assertRaises(ValueError):
            u.remove_event_organised(e3)

        with self.assertRaises(ValueError):
            u.remove_event_organised(2)

        with self.assertRaises(ValueError):
            u.remove_event_organised(1234)

        with self.assertRaises(ValueError):
            u.remove_event_organised(2)

        # Test removing events with invalid type
        with self.assertRaises(TypeError):
            u.remove_event_organised("lol")

        with self.assertRaises(TypeError):
            u.remove_event_organised("1234")

        with self.assertRaises(TypeError):
            u.remove_event_organised([1, 3, 4])

        with self.assertRaises(TypeError):
            u.remove_event_organised(u)

    def test_remove_event_attending(self):
        u = User("test")
        u.add_event_attending(1)
        u.add_event_attending(4)
        u.remove_event_attending(1)
        self.assertEqual(u.get_events_attending_ids(), [4])
        u.add_event_attending(2)
        u.add_event_attending(99)
        u.add_event_attending(1234)
        u.remove_event_attending(99)
        self.assertEqual(u.get_events_attending_ids(), [4, 2, 1234])
        u.remove_event_attending(4)
        self.assertEqual(u.get_events_attending_ids(), [2, 1234])

        # Removing events with Event objects
        e = Event(35, "e", "l", "t")
        e.id = 1234
        u.remove_event_attending(e)
        self.assertEqual(u.get_events_attending_ids(), [2])
        u.remove_event_attending(2)
        self.assertEqual(u.get_events_attending_ids(), [])

        e = Event(1, "event", "location", "time")
        e.id = 34
        u.add_event_attending(e)
        self.assertEqual(u.get_events_attending_ids(), [34])

        e2 = Event(1234, "event2", "location2", "time2")
        e2.id = 834
        u.add_event_attending(e2)
        self.assertEqual(u.get_events_attending_ids(), [34, 834])

        e3 = Event(999, "event3", "location3", "time3")
        e3.id = 99
        u.add_event_attending(e3)
        self.assertEqual(u.get_events_attending_ids(), [34, 834, 99])

        # Finish removing with event ids (integers)
        u.remove_event_attending(e2)
        self.assertEqual(u.get_events_attending_ids(), [34, 99])
        u.remove_event_attending(34)
        self.assertEqual(u.get_events_attending_ids(), [99])
        u.remove_event_attending(e3)
        self.assertEqual(u.get_events_attending_ids(), [])

        # Test removing events that don't exist
        with self.assertRaises(ValueError):
            u.remove_event_attending(e)

        with self.assertRaises(ValueError):
            u.remove_event_attending(e3)

        with self.assertRaises(ValueError):
            u.remove_event_attending(2)

        with self.assertRaises(ValueError):
            u.remove_event_attending(1234)

        with self.assertRaises(ValueError):
            u.remove_event_attending(2)

        # Test removing events with invalid type
        with self.assertRaises(TypeError):
            u.remove_event_attending("lol")

        with self.assertRaises(TypeError):
            u.remove_event_attending("1234")

        with self.assertRaises(TypeError):
            u.remove_event_attending([1, 3, 4])

        with self.assertRaises(TypeError):
            u.remove_event_attending(u)


if __name__ == '__main__':
    unittest.main()
