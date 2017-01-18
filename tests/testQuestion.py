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
        pass

    def test_get_question_type(self):
        pass

    def test_get_survey_id(self):
        pass

    def test_get_allowed_choice_ids(self):
        pass

    def test_get_response_choice_ids(self):
        pass

    def test_set_survey_id(self):
        pass

    def test_set_question(self):
        pass

    def test_set_question_type(self):
        pass

    def test_add_allowed_choice_id(self):
        pass

    def test_remove_allowed_choice_id(self):
        pass

if __name__ == '__main__':
    unittest.main()
