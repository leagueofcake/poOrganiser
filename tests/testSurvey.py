import unittest
from Poorganiser import Survey, Question, Event


class TestSurvey(unittest.TestCase):
    def test_constructor_assertions(self):
        # Incorrect name type
        with self.assertRaises(AssertionError):
            Survey(1, 3)

        with self.assertRaises(AssertionError):
            Survey(["fail"], 20, question_ids=[2, 4, 6])

        with self.assertRaises(AssertionError):
            Survey(10.3, 11, question_ids=[2, 4, 6], event_id=4)

        # Incorrect owner id type
        with self.assertRaises(AssertionError):
            Survey("s1", 3.21)

        with self.assertRaises(AssertionError):
            Survey("s2", "lol", question_ids=[2, 4, 6])

        with self.assertRaises(AssertionError):
            Survey("s3", None, question_ids=[2, 4, 6], event_id=4)

        # Incorrect question ids type
        with self.assertRaises(AssertionError):
            Survey("s1", 3, question_ids="kek")

        with self.assertRaises(AssertionError):
            Survey("s2 and two", 20, question_ids=["just", "blatantly", "wrong"])

        with self.assertRaises(AssertionError):
            Survey(10.3, 11, question_ids=[2, 4, 6.3], event_id=4)

        # Incorrect event_id type
        with self.assertRaises(AssertionError):
            Survey("s1", 3, event_id="kek")

        with self.assertRaises(AssertionError):
            Survey("s2 and two", 20, event_id=12.345)

        with self.assertRaises(AssertionError):
            Survey(10.3, 11, question_ids=[2, 4, 6], event_id=[1, 4, 9])

    def test_get_name(self):
        s = Survey("s1", 2)
        self.assertEqual(s.get_name(), "s1")

        s = Survey("s2", 130, question_ids=[1, 4, 8])
        self.assertEqual(s.get_name(), "s2")

        s = Survey("s3", 339, question_ids=[3, 5, 7, 9, 11], event_id=10)
        self.assertEqual(s.get_name(), "s3")

    def test_get_owner_id(self):
        s = Survey("s1", 2)
        self.assertEqual(s.get_owner_id(), 2)

        s = Survey("s2", 130, question_ids=[1, 4, 8])
        self.assertEqual(s.get_owner_id(), 130)

        s = Survey("s3", 339, question_ids=[3, 5, 7, 9, 11], event_id=10)
        self.assertEqual(s.get_owner_id(), 339)

    def test_get_question_ids(self):
        s = Survey("s1", 2)
        self.assertEqual(s.get_question_ids(), [])

        s = Survey("s2", 130, question_ids=[1, 4, 8])
        self.assertEqual(s.get_question_ids(), [1, 4, 8])

        s = Survey("s3", 339, question_ids=[3, 5, 7, 9, 11], event_id=10)
        self.assertEqual(s.get_question_ids(), [3, 5, 7, 9, 11])

    def test_get_event_id(self):
        s = Survey("s1", 2)
        self.assertEqual(s.get_event_id(), None)

        s = Survey("s2", 130, question_ids=[1, 4, 8])
        self.assertEqual(s.get_event_id(), None)

        s = Survey("s3", 339, question_ids=[3, 5, 7, 9, 11], event_id=10)
        self.assertEqual(s.get_event_id(), 10)

    def test_set_name(self):
        s = Survey("s1", 2)
        self.assertEqual(s.get_name(), "s1")
        s.set_name("new s1")
        self.assertEqual(s.get_name(), "new s1")
        s.set_name("blah")
        self.assertEqual(s.get_name(), "blah")

        s = Survey("s2", 130, question_ids=[1, 4, 8])
        self.assertEqual(s.get_event_id(), None)
        s.set_name("newer s2")
        self.assertEqual(s.get_name(), "newer s2")

        s = Survey("s3", 339, question_ids=[3, 5, 7, 9, 11], event_id=10)
        self.assertEqual(s.get_name(), "s3")
        s.set_name("lalalala")
        self.assertEqual(s.get_name(), "lalalala")

        # Test setting name with invalid type
        with self.assertRaises(AssertionError):
            s.set_name(30142)

        with self.assertRaises(AssertionError):
            s.set_name(["a", "b"])

        with self.assertRaises(AssertionError):
            s.set_name(s)

    def test_set_owner_id(self):
        s = Survey("s1", 2)
        self.assertEqual(s.get_owner_id(), 2)
        s.set_owner_id(34)
        self.assertEqual(s.get_owner_id(), 34)
        s.set_owner_id(912)
        self.assertEqual(s.get_owner_id(), 912)

        s = Survey("s2", 130, question_ids=[1, 4, 8])
        self.assertEqual(s.get_owner_id(), 130)
        s.set_owner_id(222)
        self.assertEqual(s.get_owner_id(), 222)
        s.set_owner_id(31)
        self.assertEqual(s.get_owner_id(), 31)

        s = Survey("s3", 339, question_ids=[3, 5, 7, 9, 11], event_id=10)
        self.assertEqual(s.get_owner_id(), 339)
        s.set_owner_id(20)
        self.assertEqual(s.get_owner_id(), 20)
        s.set_owner_id(9876)
        self.assertEqual(s.get_owner_id(), 9876)

        # Test setting owner id with invalid type
        with self.assertRaises(AssertionError):
            s.set_owner_id(1.234)

        with self.assertRaises(AssertionError):
            s.set_owner_id("LOL OK")

        with self.assertRaises(AssertionError):
            s.set_owner_id(s)

    def test_add_question_id(self):
        s = Survey("s1", 2)
        self.assertEqual(s.get_question_ids(), [])
        s.add_question_id(24)
        self.assertEqual(s.get_question_ids(), [24])
        s.add_question_id(38)
        self.assertEqual(s.get_question_ids(), [24, 38])

        # Try to add with mock Question objects
        q_mock = Question("hello", "lol")
        q_mock.id = 24
        s.add_question_id(q_mock)  # Try add duplicate
        self.assertEqual(s.get_question_ids(), [24, 38])
        q_mock.id = 91
        s.add_question_id(q_mock)
        self.assertEqual(s.get_question_ids(), [24, 38, 91])

        s = Survey("s2", 130, question_ids=[1, 4, 9])
        self.assertEqual(s.get_question_ids(), [1, 4, 9])
        s.add_question_id(16)
        self.assertEqual(s.get_question_ids(), [1, 4, 9, 16])
        s.add_question_id(25)
        self.assertEqual(s.get_question_ids(), [1, 4, 9, 16, 25])

        s = Survey("s3", 339, question_ids=[3, 5, 7, 9, 11], event_id=10)
        self.assertEqual(s.get_question_ids(), [3, 5, 7, 9, 11])
        s.add_question_id(13)
        self.assertEqual(s.get_question_ids(), [3, 5, 7, 9, 11, 13])
        s.add_question_id(15)
        self.assertEqual(s.get_question_ids(), [3, 5, 7, 9, 11, 13, 15])

        # Try add question ids with invalid types:
        with self.assertRaises(TypeError):
            s.add_question_id("top kek")

        with self.assertRaises(TypeError):
            s.add_question_id(3.579)

        with self.assertRaises(TypeError):
            s.add_question_id(s)

    def test_remove_question_id(self):
        s = Survey("s1", 2)
        self.assertEqual(s.get_question_ids(), [])
        s.add_question_id(24)
        self.assertEqual(s.get_question_ids(), [24])
        s.add_question_id(38)
        self.assertEqual(s.get_question_ids(), [24, 38])
        s.remove_question_id(38)
        self.assertEqual(s.get_question_ids(), [24])

        # Try to remove with mock Question objects
        q_mock = Question("hello", "lol")
        q_mock.id = 24
        s.remove_question_id(q_mock)
        self.assertEqual(s.get_question_ids(), [])
        q_mock.id = 91  # Try remove an element that doesn't exist
        s.remove_question_id(q_mock)
        self.assertEqual(s.get_question_ids(), [])

        s = Survey("s2", 130, question_ids=[1, 4, 9])
        self.assertEqual(s.get_question_ids(), [1, 4, 9])
        s.remove_question_id(1)
        self.assertEqual(s.get_question_ids(), [4, 9])
        s.add_question_id(25)
        self.assertEqual(s.get_question_ids(), [4, 9, 25])
        s.remove_question_id(9)
        self.assertEqual(s.get_question_ids(), [4, 25])

        s = Survey("s3", 339, question_ids=[3, 5, 7, 9, 11], event_id=10)
        self.assertEqual(s.get_question_ids(), [3, 5, 7, 9, 11])
        s.add_question_id(13)
        self.assertEqual(s.get_question_ids(), [3, 5, 7, 9, 11, 13])
        s.remove_question_id(3)
        self.assertEqual(s.get_question_ids(), [5, 7, 9, 11, 13])
        s.remove_question_id(11)
        self.assertEqual(s.get_question_ids(), [5, 7, 9, 13])

        # Try remove question ids with invalid types:
        with self.assertRaises(TypeError):
            s.remove_question_id("top kek")

        with self.assertRaises(TypeError):
            s.remove_question_id(3.579)

        with self.assertRaises(TypeError):
            s.remove_question_id(s)

    def test_set_event_id(self):
        s = Survey("s1", 2)
        self.assertEqual(s.get_event_id(), None)
        s.set_event_id(24)
        self.assertEqual(s.get_event_id(), 24)

        # Test setting event id with mock Event object
        e_mock = Event("event 1", 3)
        e_mock.id = 9
        s.set_event_id(e_mock)
        self.assertEqual(s.get_event_id(), 9)
        e_mock.id = 24
        s.set_event_id(e_mock)
        self.assertEqual(s.get_event_id(), 24)

        s = Survey("s2", 130, question_ids=[1, 4, 9])
        self.assertEqual(s.get_event_id(), None)
        s.set_event_id(1234)
        self.assertEqual(s.get_event_id(), 1234)
        e_mock.id = 999
        s.set_event_id(e_mock)
        self.assertEqual(s.get_event_id(), 999)

        s = Survey("s3", 339, question_ids=[3, 5, 7, 9, 11], event_id=10)
        self.assertEqual(s.get_event_id(), 10)
        s.set_event_id(11)
        self.assertEqual(s.get_event_id(), 11)
        e_mock.id = 12
        s.set_event_id(e_mock)
        self.assertEqual(s.get_event_id(), 12)


if __name__ == '__main__':
    unittest.main()
