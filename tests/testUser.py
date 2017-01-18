import unittest
from Poorganiser import User, Event, Survey, Question
from datetime import datetime


class TestUser(unittest.TestCase):
    def test_constructor_assertions(self):
        # Incorrect username type
        with self.assertRaises(AssertionError):
            User(1234)

        with self.assertRaises(AssertionError):
            User(User("bob"))

        with self.assertRaises(AssertionError):
            User(User(3.14))

        with self.assertRaises(AssertionError):
            User(list())

    def test_get_username(self):
        u = User("")
        self.assertEqual(u.get_username(), "")  # Empty case

        u = User(" ")
        self.assertEqual(u.get_username(), " ")  # Whitespace case

        u = User("Jeremy")
        self.assertEqual(u.get_username(), "Jeremy")  # Normal string

        u = User("   Dave and Friends ")
        self.assertEqual(u.get_username(), "   Dave and Friends ")  # Normal string with whitespace

    def test_get_events_organised_ids(self):
        u = User("test")
        self.assertEqual(u.get_events_organised_ids(), [])  # Blank case

        u = User("blahblahblah")
        self.assertEqual(u.get_events_organised_ids(), [])  # Blank case 2

    def test_get_events_attending_ids(self):
        u = User("test")
        self.assertEqual(u.get_events_attending_ids(), [])  # Blank case

        u = User("blahblahblah")
        self.assertEqual(u.get_events_attending_ids(), [])  # Blank case 2

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

        # Test setting usernames with invalid types
        with self.assertRaises(AssertionError):
            u.set_username(3)

        with self.assertRaises(AssertionError):
            u.set_username(3.14)

        with self.assertRaises(AssertionError):
            u.set_username(u)

        with self.assertRaises(AssertionError):
            u.set_username(Event(1, 2))

    def test_add_event_organised(self):
        # Adding events with event ids (integers)
        u = User("test")
        u.add_event_organised(1)
        self.assertEqual(u.get_events_organised_ids(), [1])
        u.add_event_organised(4)
        self.assertEqual(u.get_events_organised_ids(), [1, 4])
        u.add_event_organised(2)
        self.assertEqual(u.get_events_organised_ids(), [1, 4, 2])

        # Adding duplicates
        u.add_event_organised(2)
        self.assertEqual(u.get_events_organised_ids(), [1, 4, 2])

        u.add_event_organised(4)
        self.assertEqual(u.get_events_organised_ids(), [1, 4, 2])

        # Adding events with Event objects
        e = Event("event", 1,  "location", datetime(2017, 1, 1))
        e.id = 34
        u.add_event_organised(e)
        self.assertEqual(u.get_events_organised_ids(), [1, 4, 2, 34])

        e = Event("event2", 93,  "location2", datetime(2017, 1, 2))
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

        # Adding duplicates
        u.add_event_attending(2)
        self.assertEqual(u.get_events_attending_ids(), [1, 4, 2])

        u.add_event_attending(4)
        self.assertEqual(u.get_events_attending_ids(), [1, 4, 2])

        # Adding events with Event objects
        e = Event("event", 1,  "location", datetime(2017, 1, 1))  # Add event using Event object
        e.id = 34
        u.add_event_attending(e)
        self.assertEqual(u.get_events_attending_ids(), [1, 4, 2, 34])

        e = Event("event2", 93,  "location2", datetime(2017, 1, 2))
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
        u.add_event_organised(1)
        u.add_event_organised(4)
        u.remove_event_organised(1)
        self.assertEqual(u.get_events_organised_ids(), [4])
        u.add_event_organised(2)
        u.add_event_organised(99)
        u.add_event_organised(99)
        u.add_event_organised(1234)
        u.remove_event_organised(99)
        self.assertEqual(u.get_events_organised_ids(), [4, 2, 1234])
        u.remove_event_organised(4)
        self.assertEqual(u.get_events_organised_ids(), [2, 1234])

        # Removing events with Event objects
        e = Event("e", 35,  "l", datetime(2017, 1, 1))
        e.id = 1234
        u.remove_event_organised(e)
        self.assertEqual(u.get_events_organised_ids(), [2])
        u.remove_event_organised(2)
        self.assertEqual(u.get_events_organised_ids(), [])

        e = Event("event", 1,  "location", datetime(2017, 1, 1))
        e.id = 34
        u.add_event_organised(e)
        self.assertEqual(u.get_events_organised_ids(), [34])

        e2 = Event("event2", 1234,  "location2", datetime(2017, 1, 2))
        e2.id = 834
        u.add_event_organised(e2)
        self.assertEqual(u.get_events_organised_ids(), [34, 834])

        e3 = Event("event3", 999,  "location3", datetime(2017, 1, 3))
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
        self.assertIsNone(u.remove_event_organised(e))
        self.assertIsNone(u.remove_event_organised(e3))
        self.assertIsNone(u.remove_event_organised(2))
        self.assertIsNone(u.remove_event_organised(1234))
        self.assertIsNone(u.remove_event_organised(2))

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
        # Removing events with event ids (integers)
        u = User("test")
        u.add_event_attending(1)
        u.add_event_attending(1)
        u.add_event_attending(4)
        u.remove_event_attending(1)
        self.assertEqual(u.get_events_attending_ids(), [4])
        u.add_event_attending(2)
        u.add_event_attending(99)
        u.add_event_attending(99)
        u.add_event_attending(1234)
        u.remove_event_attending(99)
        self.assertEqual(u.get_events_attending_ids(), [4, 2, 1234])
        u.remove_event_attending(4)
        self.assertEqual(u.get_events_attending_ids(), [2, 1234])

        # Removing events with Event objects
        e = Event("e", 35,  "l", datetime(2017, 1, 1))
        e.id = 1234
        u.remove_event_attending(e)
        self.assertEqual(u.get_events_attending_ids(), [2])
        u.remove_event_attending(2)
        self.assertEqual(u.get_events_attending_ids(), [])

        e = Event("event", 1,  "location", datetime(2017, 1, 1))
        e.id = 34
        u.add_event_attending(e)
        self.assertEqual(u.get_events_attending_ids(), [34])

        e2 = Event("event2", 1234,  "location2", datetime(2017, 1, 2))
        e2.id = 834
        u.add_event_attending(e2)
        self.assertEqual(u.get_events_attending_ids(), [34, 834])

        e3 = Event("event3", 999,  "location3", datetime(2017, 1, 3))
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
        self.assertIsNone(u.remove_event_organised(e))
        self.assertIsNone(u.remove_event_organised(e3))
        self.assertIsNone(u.remove_event_organised(2))
        self.assertIsNone(u.remove_event_organised(1234))
        self.assertIsNone(u.remove_event_organised(2))

        # Test removing events with invalid type
        with self.assertRaises(TypeError):
            u.remove_event_attending("lol")

        with self.assertRaises(TypeError):
            u.remove_event_attending("1234")

        with self.assertRaises(TypeError):
            u.remove_event_attending([1, 3, 4])

        with self.assertRaises(TypeError):
            u.remove_event_attending(u)

    def test_add_survey_id(self):
        u = User("user 1")
        self.assertEqual(u.get_survey_ids(), [])
        u.add_survey_id(3)
        self.assertEqual(u.get_survey_ids(), [3])
        u.add_survey_id(3)  # Test adding duplicate
        self.assertEqual(u.get_survey_ids(), [3])

        # Test adding with mock Survey object
        s_mock = Survey("blob", 1)
        s_mock.id = 129
        u.add_survey_id(s_mock)
        self.assertEqual(u.get_survey_ids(), [3, 129])

        s_mock.id = 123
        u.add_survey_id(s_mock)
        self.assertEqual(u.get_survey_ids(), [3, 129, 123])

        # Test adding with invalid survey_obj type
        with self.assertRaises(TypeError):
            u.add_survey_id(3.14)

        with self.assertRaises(TypeError):
            u.add_survey_id("blah blah blah")

    def test_add_question_id(self):
        u = User("user 1")
        self.assertEqual(u.get_question_ids(), [])
        u.add_question_id(13)
        self.assertEqual(u.get_question_ids(), [13])
        u.add_question_id(26)
        self.assertEqual(u.get_question_ids(), [13, 26])
        u.add_question_id(26)  # Test adding duplicate
        self.assertEqual(u.get_question_ids(), [13, 26])

        # Test adding with mock Question object
        q_mock = Question(1, "lol", "free")
        q_mock.id = 39
        u.add_question_id(q_mock)
        self.assertEqual(u.get_question_ids(), [13, 26, 39])

        q_mock.id = 999
        u.add_question_id(q_mock)
        self.assertEqual(u.get_question_ids(), [13, 26, 39, 999])

        # Test adding with invalid question_obj type
        with self.assertRaises(TypeError):
            u.add_question_id(3.14)

        with self.assertRaises(TypeError):
            u.add_question_id("blah blah blah")

    def test_remove_survey_id(self):
        u = User("user 1")
        self.assertEqual(u.get_survey_ids(), [])
        u.add_survey_id(3)
        self.assertEqual(u.get_survey_ids(), [3])
        u.remove_survey_id(3)
        self.assertEqual(u.get_survey_ids(), [])
        u.remove_survey_id(29)  # Test removing non-existant element
        self.assertEqual(u.get_survey_ids(), [])
        u.add_survey_id(912)
        self.assertEqual(u.get_survey_ids(), [912])

        # Test removing with mock Survey object
        s_mock = Survey("blob", 1)
        s_mock.id = 3
        u.add_survey_id(s_mock)
        self.assertEqual(u.get_survey_ids(), [912, 3])

        s_mock.id = 912
        u.remove_survey_id(s_mock)
        self.assertEqual(u.get_survey_ids(), [3])

        u.remove_survey_id(3)
        self.assertEqual(u.get_survey_ids(), [])

        # Test removing with invalid survey_obj type
        with self.assertRaises(TypeError):
            u.remove_survey_id(3.14)

        with self.assertRaises(TypeError):
            u.remove_survey_id("blah blah blah")

    def test_remove_question_id(self):
        u = User("user 1")
        self.assertEqual(u.get_question_ids(), [])
        u.add_question_id(13)
        self.assertEqual(u.get_question_ids(), [13])
        u.add_question_id(26)
        self.assertEqual(u.get_question_ids(), [13, 26])
        u.remove_question_id(29)  # Test removing non-existant element
        self.assertEqual(u.get_question_ids(), [13, 26])

        # Test removing with mock Question object
        q_mock = Question(1, "lol", "free")
        q_mock.id = 13
        u.remove_question_id(q_mock)
        self.assertEqual(u.get_question_ids(), [26])

        q_mock.id = 999
        u.add_question_id(q_mock)
        self.assertEqual(u.get_question_ids(), [26, 999])

        u.remove_question_id(999)
        self.assertEqual(u.get_question_ids(), [26])

        q_mock.id = 26
        u.remove_question_id(q_mock)
        self.assertEqual(u.get_question_ids(), [])

        # Test removing with invalid question_obj type
        with self.assertRaises(TypeError):
            u.remove_question_id(3.14)

        with self.assertRaises(TypeError):
            u.remove_question_id("blah blah blah")



if __name__ == '__main__':
    unittest.main()
