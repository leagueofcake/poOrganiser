import unittest
from Poorganiser import Question


class TestQuestion(unittest.TestCase):
    def test_constructor_assertions(self):
        # Incorrect question type
        with self.assertRaises(AssertionError):
            Question(3.14, "free")

        with self.assertRaises(AssertionError):
            Question(["invalid"], "choose_multiple")

        with self.assertRaises(AssertionError):
            Question(('kek', ), "choose_multiple", survey_id=3, allowed_choice_ids=[5, 24])

        # Incorrect question_type type
        with self.assertRaises(AssertionError):
            Question("Hello?", ["choose_multiple"])

        with self.assertRaises(AssertionError):
            Question("do you like cheese?", ["choose_one"])

        with self.assertRaises(AssertionError):
            Question("something", 1122334455, survey_id=24, allowed_choice_ids=[3, 6, 9])

        # Incorrect survey_id type
        with self.assertRaises(AssertionError):
            Question("hi?", 123, survey_id="1")

        with self.assertRaises(AssertionError):
            Question("blah blah", 123, survey_id=1.34, allowed_choice_ids=[2, 103, 24])

        # Incorrect allowed_choice_ids type
        with self.assertRaises(AssertionError):
            Question("lalalala", 47, allowed_choice_ids="totally wrong")

        with self.assertRaises(AssertionError):
            Question("a question", 81, survey_id=134, allowed_choice_ids=[45.6])

        with self.assertRaises(AssertionError):
            Question("lalalala", 47, survey_id=134, allowed_choice_ids=[24, 5, 9, "oops", 10])

    def test_get_question(self):
        q = Question("hello?", "free")
        self.assertEqual(q.get_question(), "hello?")

        q = Question("cool or school?", "choose_one", survey_id=350)
        self.assertEqual(q.get_question(), "cool or school?")

        q = Question("Do you like cake", "choose_one", survey_id=24, allowed_choice_ids=[34, 45])
        self.assertEqual(q.get_question(), "Do you like cake")

    def test_get_question_type(self):
        q = Question("hello?", "free")
        self.assertEqual(q.get_question_type(), "free")

        q = Question("cool or school?", "choose_one", survey_id=350)
        self.assertEqual(q.get_question_type(), "choose_one")

        q = Question("Do you like cake", "choose_many", survey_id=24, allowed_choice_ids=[34, 45])
        self.assertEqual(q.get_question_type(), "choose_many")

    def test_get_survey_id(self):
        q = Question("hello?", "free")
        self.assertEqual(q.get_survey_id(), None)

        q = Question("cool or school?", "choose_one", survey_id=350)
        self.assertEqual(q.get_survey_id(), 350)

        q = Question("Do you like cake", "choose_many", survey_id=24, allowed_choice_ids=[34, 45])
        self.assertEqual(q.get_survey_id(), 24)

    def test_get_allowed_choice_ids(self):
        q = Question("hello?", "free")
        self.assertEqual(q.get_allowed_choice_ids(), [])

        q = Question("cool or school?", "choose_one", survey_id=350, allowed_choice_ids=[20])
        self.assertEqual(q.get_allowed_choice_ids(), [20])

        q = Question("Do you like cake", "choose_many", survey_id=24, allowed_choice_ids=[34, 45])
        self.assertEqual(q.get_allowed_choice_ids(), [34, 45])

    def test_get_response_ids(self):
        q = Question("hello?", "free")
        self.assertEqual(q.get_response_ids(), [])

        q = Question("cool or school?", "choose_one", survey_id=350)
        self.assertEqual(q.get_response_ids(), [])

        q = Question("Do you like cake", "choose_many", survey_id=24, allowed_choice_ids=[34, 45])
        self.assertEqual(q.get_response_ids(), [])

    def test_set_survey_id(self):
        q = Question("hello?", "free")
        self.assertEqual(q.get_survey_id(), None)

        q.set_survey_id(50)
        self.assertEqual(q.get_survey_id(), 50)
        q.set_survey_id(1234)
        self.assertEqual(q.get_survey_id(), 1234)

        q = Question("Do you like cake", "choose_many", survey_id=24, allowed_choice_ids=[34, 45])
        self.assertEqual(q.get_survey_id(), 24)

        q.set_survey_id(24)
        self.assertEqual(q.get_survey_id(), 24)
        q.set_survey_id(350)
        self.assertEqual(q.get_survey_id(), 350)

        # Test setting survey id with invalid type
        with self.assertRaises(AssertionError):
            q.set_survey_id("blah")

        with self.assertRaises(AssertionError):
            q.set_survey_id(q)

        with self.assertRaises(AssertionError):
            q.set_survey_id([24])

    def test_set_question(self):
        q = Question("hello?", "free")
        self.assertEqual(q.get_question(), "hello?")

        q.set_question("blah blah blah")
        self.assertEqual(q.get_question(), "blah blah blah")
        q.set_question("lalala54321")
        self.assertEqual(q.get_question(), "lalala54321")

        # Test setting question with invalid type
        with self.assertRaises(AssertionError):
            q.set_question(19823)

        with self.assertRaises(AssertionError):
            q.set_question(["invalid question"])

        with self.assertRaises(AssertionError):
            q.set_question(q)

    def test_set_question_type(self):
        q = Question("hello?", "free")
        self.assertEqual(q.get_question_type(), "free")

        q.set_question_type("blah blah blah")
        self.assertEqual(q.get_question_type(), "blah blah blah")
        q.set_question_type("lalala54321")
        self.assertEqual(q.get_question_type(), "lalala54321")

        q = Question("Do you like cake", "choose_many", survey_id=24, allowed_choice_ids=[34, 45])
        q.set_question_type("choose many")
        self.assertEqual(q.get_question_type(), "choose many")
        q.set_question_type("dots or something")
        self.assertEqual(q.get_question_type(), "dots or something")

        # Test setting question with invalid type
        with self.assertRaises(AssertionError):
            q.set_question_type(19823)

        with self.assertRaises(AssertionError):
            q.set_question_type(["invalid question type"])

        with self.assertRaises(AssertionError):
            q.set_question_type(q)

    def test_add_allowed_choice_id(self):
        q = Question("hello?", "free")
        self.assertEqual(q.get_allowed_choice_ids(), [])

        q.add_allowed_choice_id(24)
        self.assertEqual(q.get_allowed_choice_ids(), [24])
        q.add_allowed_choice_id(91)
        self.assertEqual(q.get_allowed_choice_ids(), [24, 91])
        q.add_allowed_choice_id(91)  # Try add duplicate
        self.assertEqual(q.get_allowed_choice_ids(), [24, 91])

        q = Question("Do you like cake", "choose_many", survey_id=24, allowed_choice_ids=[34, 45])
        self.assertEqual(q.get_allowed_choice_ids(), [34, 45])
        q.add_allowed_choice_id(56)
        self.assertEqual(q.get_allowed_choice_ids(), [34, 45, 56])
        q.add_allowed_choice_id(56)
        self.assertEqual(q.get_allowed_choice_ids(), [34, 45, 56])
        q.add_allowed_choice_id(67)
        self.assertEqual(q.get_allowed_choice_ids(), [34, 45, 56, 67])

        # Test adding chohice_ids with invalid types
        with self.assertRaises(AssertionError):
            q.add_allowed_choice_id("invalid choice")

        with self.assertRaises(AssertionError):
            q.add_allowed_choice_id(32.1)

        with self.assertRaises(AssertionError):
            q.add_allowed_choice_id(q)

    def test_remove_allowed_choice_id(self):
        q = Question("question text", "question type")
        self.assertEqual(q.get_allowed_choice_ids(), [])
        q.remove_allowed_choice_id(34)  # Remove allowed_choice_id that doesn't exist
        self.assertEqual(q.get_allowed_choice_ids(), [])
        q.remove_allowed_choice_id(1234)  # Remove allowed_choice_id that doesn't exist
        self.assertEqual(q.get_allowed_choice_ids(), [])

        q = Question("question text 2", "question type 2", allowed_choice_ids=[24, 56, 34])
        q.remove_allowed_choice_id(1234)  # Remove allowed_choice_id that doesn't exist
        self.assertEqual(q.get_allowed_choice_ids(), [24, 56, 34])
        q.remove_allowed_choice_id(24)
        self.assertEqual(q.get_allowed_choice_ids(), [56, 34])
        q.remove_allowed_choice_id(34)
        self.assertEqual(q.get_allowed_choice_ids(), [56])
        q.add_allowed_choice_id(50)
        self.assertEqual(q.get_allowed_choice_ids(), [56, 50])
        q.remove_allowed_choice_id(56)
        self.assertEqual(q.get_allowed_choice_ids(), [50])
        q.remove_allowed_choice_id(50)
        self.assertEqual(q.get_allowed_choice_ids(), [])

        # Try remove choice ids with invalid types
        with self.assertRaises(AssertionError):
            q.remove_allowed_choice_id(40.6)

        with self.assertRaises(AssertionError):
            q.remove_allowed_choice_id("something lel")

        with self.assertRaises(AssertionError):
            q.remove_allowed_choice_id(q)

    def test_add_response_id(self):
        q = Question("question text", "question type")
        self.assertEqual(q.get_response_ids(), [])
        q.add_response_id(34)
        self.assertEqual(q.get_response_ids(), [34])
        q.add_response_id(34)  # Try add duplicate response_id
        self.assertEqual(q.get_response_ids(), [34])
        q.add_response_id(40)
        self.assertEqual(q.get_response_ids(), [34, 40])
        q.add_response_id(751)
        self.assertEqual(q.get_response_ids(), [34, 40, 751])

        q = Question("question text 2", "question type 2", allowed_choice_ids=[1, 2, 3])
        self.assertEqual(q.get_response_ids(), [])
        q.add_response_id(99)
        self.assertEqual(q.get_response_ids(), [99])
        q.add_response_id(29)
        self.assertEqual(q.get_response_ids(), [99, 29])

        # Try add choice ids with invalid types
        with self.assertRaises(AssertionError):
            q.add_response_id(40.6)

        with self.assertRaises(AssertionError):
            q.add_response_id("something lel")

        with self.assertRaises(AssertionError):
            q.add_response_id(q)

    def test_remove_response_id(self):
        q = Question("question text", "question type")
        self.assertEqual(q.get_response_ids(), [])
        q.add_response_id(34)
        self.assertEqual(q.get_response_ids(), [34])
        q.add_response_id(34)  # Try add duplicate response_id
        self.assertEqual(q.get_response_ids(), [34])
        q.add_response_id(40)
        self.assertEqual(q.get_response_ids(), [34, 40])
        q.remove_response_id(40)
        self.assertEqual(q.get_response_ids(), [34])
        q.remove_response_id(999)  # Try remove response_id that isn't in list
        self.assertEqual(q.get_response_ids(), [34])
        q.add_response_id(751)
        self.assertEqual(q.get_response_ids(), [34, 751])
        q.remove_response_id(34)
        self.assertEqual(q.get_response_ids(), [751])
        q.remove_response_id(751)
        self.assertEqual(q.get_response_ids(), [])

        q = Question("question text 2", "question type 2", allowed_choice_ids=[1, 2, 3])
        self.assertEqual(q.get_response_ids(), [])
        q.add_response_id(99)
        self.assertEqual(q.get_response_ids(), [99])
        q.add_response_id(29)
        self.assertEqual(q.get_response_ids(), [99, 29])

        # Try add choice ids with invalid types
        with self.assertRaises(AssertionError):
            q.remove_response_id(10.5)

        with self.assertRaises(AssertionError):
            q.remove_response_id("something else lol")

        with self.assertRaises(AssertionError):
            q.remove_response_id(q)

if __name__ == '__main__':
    unittest.main()
