import unittest
from Question import Question


class TestQuestion(unittest.TestCase):
    def test_get_eventid(self):
        q1 = Question(0, "Question 1", ["user 1", "user 2"])
        self.assertEqual(q1.get_eventid(), 0)
        q1 = Question(34, "Question 1", ["user 2342", "user 932rf"])
        self.assertEqual(q1.get_eventid(), 34)

    def test_set_eventid(self):
        q1 = Question(0, "Question 1", ["user 1", "user 2"])
        self.assertEqual(q1.get_eventid(), 0)
        q1.set_eventid(42)
        self.assertEqual(q1.get_eventid(), 42)
        q1.set_eventid(123)
        q1.set_eventid(999)
        self.assertEqual(q1.get_eventid(), 999)

    def test_get_text(self):
        q1 = Question(0, "Question 1", ["user 1", "user 2"])
        self.assertEqual(q1.get_text(), "Question 1")
        q1 = Question(0, "Do you like cheese?", ["user 1"])
        self.assertEqual(q1.get_text(), "Do you like cheese?")

    def test_set_text(self):
        q1 = Question(0, "Question 1", ["user 1", "user 2"])
        self.assertEqual(q1.get_text(), "Question 1")
        q1.set_text("ASDFGHJKL")
        self.assertEqual(q1.get_text(), "ASDFGHJKL")
        q1.set_text("111111sdfsa d")
        q1.set_text("lalalala")
        self.assertEqual(q1.get_text(), "lalalala")

if __name__ == '__main__':
    unittest.main()
