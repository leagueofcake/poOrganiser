import unittest
from Poorganiser import Question, Survey, Choice, Response


class TestQuestion(unittest.TestCase):
    def test_constructor_assertions(self):
        # Incorrect owner_id type
        with self.assertRaises(AssertionError):
            Question("lol", "question", "free")

        with self.assertRaises(AssertionError):
            Question(3.42, "question", "free")

        with self.assertRaises(AssertionError):
            Question([3], "question", "free")

        # Incorrect question type
        with self.assertRaises(AssertionError):
            Question(2, 3.14, "free")

        with self.assertRaises(AssertionError):
            Question(42, ["invalid"], "choose_multiple")

        with self.assertRaises(AssertionError):
            Question(79, ('kek', ), "choose_multiple", survey_id=3, allowed_choice_ids=[5, 24])

        # Incorrect question_type type
        with self.assertRaises(AssertionError):
            Question(192, "Hello?", ["choose_multiple"])

        with self.assertRaises(AssertionError):
            Question(71, "do you like cheese?", ["choose_one"])

        with self.assertRaises(AssertionError):
            Question(2, "something", 1122334455, survey_id=24, allowed_choice_ids=[3, 6, 9])

        # Incorrect survey_id type
        with self.assertRaises(AssertionError):
            Question(33, "hi?", 123, survey_id="1")

        with self.assertRaises(AssertionError):
            Question(52, "blah blah", 123, survey_id=1.34, allowed_choice_ids=[2, 103, 24])

        # Incorrect allowed_choice_ids type
        with self.assertRaises(AssertionError):
            Question(91, "lalalala", 47, allowed_choice_ids="totally wrong")

        with self.assertRaises(AssertionError):
            Question(8, "a question", 81, survey_id=134, allowed_choice_ids=[45.6])

        with self.assertRaises(AssertionError):
            Question(111, "lalalala", 47, survey_id=134, allowed_choice_ids=[24, 5, 9, "oops", 10])

    def test_get_owner_id(self):
        q = Question(52, "hello?", "free")
        self.assertEqual(q.get_owner_id(), 52)

        q = Question(32, "cool or school?", "choose_one", survey_id=350)
        self.assertEqual(q.get_owner_id(), 32)

        q = Question(12, "Do you like", "choose_one", survey_id=24, allowed_choice_ids=[34, 45])
        self.assertEqual(q.get_owner_id(), 12)

    def test_get_question(self):
        q = Question(52, "hello?", "free")
        self.assertEqual(q.get_question(), "hello?")

        q = Question(32, "cool or school?", "choose_one", survey_id=350)
        self.assertEqual(q.get_question(), "cool or school?")

        q = Question(12, "Do you like", "choose_one", survey_id=24, allowed_choice_ids=[34, 45])
        self.assertEqual(q.get_question(), "Do you like")

    def test_get_question_type(self):
        q = Question(52, "hello?", "free")
        self.assertEqual(q.get_question_type(), "free")

        q = Question(32, "cool or school?", "choose_one", survey_id=350)
        self.assertEqual(q.get_question_type(), "choose_one")

        q = Question(12, "Do you like", "choose_many", survey_id=24, allowed_choice_ids=[34, 45])
        self.assertEqual(q.get_question_type(), "choose_many")

    def test_get_survey_id(self):
        q = Question(52, "hello?", "free")
        self.assertEqual(q.get_survey_id(), None)

        q = Question(32, "cool or school?", "choose_one", survey_id=350)
        self.assertEqual(q.get_survey_id(), 350)

        q = Question(12, "Do you like", "choose_many", survey_id=24, allowed_choice_ids=[34, 45])
        self.assertEqual(q.get_survey_id(), 24)

    def test_get_allowed_choice_ids(self):
        q = Question(52, "hello?", "free")
        self.assertEqual(q.get_allowed_choice_ids(), [])

        q = Question(32, "cool or school?", "choose_one", survey_id=350, allowed_choice_ids=[20])
        self.assertEqual(q.get_allowed_choice_ids(), [20])

        q = Question(12, "Do you like", "choose_many", survey_id=24, allowed_choice_ids=[34, 45])
        self.assertEqual(q.get_allowed_choice_ids(), [34, 45])

    def test_get_response_ids(self):
        q = Question(52, "hello?", "free")
        self.assertEqual(q.get_response_ids(), [])

        q = Question(32, "cool or school?", "choose_one", survey_id=350)
        self.assertEqual(q.get_response_ids(), [])

        q = Question(12, "Do you like", "choose_many", survey_id=24, allowed_choice_ids=[34, 45])
        self.assertEqual(q.get_response_ids(), [])

    def test_set_owner_id(self):
        q = Question(52, "hello?", "free")
        self.assertEqual(q.get_owner_id(), 52)
        q.set_owner_id(123)
        self.assertEqual(q.get_owner_id(), 123)

        q = Question(32, "cool or school?", "choose_one", survey_id=350)
        self.assertEqual(q.get_owner_id(), 32)
        q.set_owner_id(999)
        self.assertEqual(q.get_owner_id(), 999)
        q.set_owner_id(24)
        self.assertEqual(q.get_owner_id(), 24)

        q = Question(12, "Do you like", "choose_one", survey_id=24, allowed_choice_ids=[34, 45])
        self.assertEqual(q.get_owner_id(), 12)
        q.set_owner_id(9876)
        self.assertEqual(q.get_owner_id(), 9876)

    def test_set_survey_id(self):
        q = Question(52, "hello?", "free")
        self.assertEqual(q.get_survey_id(), None)

        q.set_survey_id(50)
        self.assertEqual(q.get_survey_id(), 50)

        # Test adding with mock Survey object
        s_mock = Survey("blah", 1)
        s_mock.id = 1234
        q.set_survey_id(s_mock)
        self.assertEqual(q.get_survey_id(), 1234)

        q = Question(32, "Do you like", "choose_many", survey_id=24, allowed_choice_ids=[34, 45])
        self.assertEqual(q.get_survey_id(), 24)

        q.set_survey_id(24)
        self.assertEqual(q.get_survey_id(), 24)
        q.set_survey_id(350)
        self.assertEqual(q.get_survey_id(), 350)

        # Test setting survey id with invalid type
        with self.assertRaises(TypeError):
            q.set_survey_id("blah")

        with self.assertRaises(TypeError):
            q.set_survey_id(q)

        with self.assertRaises(TypeError):
            q.set_survey_id([24])

    def test_set_question(self):
        q = Question(52, "hello?", "free")
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
        q = Question(52, "hello?", "free")
        self.assertEqual(q.get_question_type(), "free")

        q.set_question_type("blah blah blah")
        self.assertEqual(q.get_question_type(), "blah blah blah")
        q.set_question_type("lalala54321")
        self.assertEqual(q.get_question_type(), "lalala54321")

        q = Question(32, "Do you like", "choose_many", survey_id=24, allowed_choice_ids=[34, 45])
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
        q = Question(52, "hello?", "free")
        self.assertEqual(q.get_allowed_choice_ids(), [])

        q.add_allowed_choice_id(24)
        self.assertEqual(q.get_allowed_choice_ids(), [24])
        q.add_allowed_choice_id(91)
        self.assertEqual(q.get_allowed_choice_ids(), [24, 91])
        q.add_allowed_choice_id(91)  # Try add duplicate
        self.assertEqual(q.get_allowed_choice_ids(), [24, 91])

        q = Question(32, "Do you like", "choose_many", survey_id=24, allowed_choice_ids=[34, 45])
        self.assertEqual(q.get_allowed_choice_ids(), [34, 45])
        q.add_allowed_choice_id(56)

        # Test adding allowed choice ids with mock Choice objects
        c_mock = Choice(3, "lol")
        c_mock.id = 56
        q.add_allowed_choice_id(c_mock)
        self.assertEqual(q.get_allowed_choice_ids(), [34, 45, 56])
        q.add_allowed_choice_id(56)
        self.assertEqual(q.get_allowed_choice_ids(), [34, 45, 56])
        c_mock.id = 67
        q.add_allowed_choice_id(c_mock)
        self.assertEqual(q.get_allowed_choice_ids(), [34, 45, 56, 67])

        # Test adding chohice_ids with invalid types
        with self.assertRaises(TypeError):
            q.add_allowed_choice_id("invalid choice")

        with self.assertRaises(TypeError):
            q.add_allowed_choice_id(32.1)

        with self.assertRaises(TypeError):
            q.add_allowed_choice_id(q)

    def test_remove_allowed_choice_id(self):
        q = Question(52, "question text", "question type")
        self.assertEqual(q.get_allowed_choice_ids(), [])
        q.remove_allowed_choice_id(34)  # Remove allowed_choice_id that doesn't exist
        self.assertEqual(q.get_allowed_choice_ids(), [])
        q.remove_allowed_choice_id(1234)  # Remove allowed_choice_id that doesn't exist
        self.assertEqual(q.get_allowed_choice_ids(), [])

        q = Question(32, "question text 2", "question type 2", allowed_choice_ids=[24, 56, 34])
        q.remove_allowed_choice_id(1234)  # Remove allowed_choice_id that doesn't exist
        self.assertEqual(q.get_allowed_choice_ids(), [24, 56, 34])
        q.remove_allowed_choice_id(24)
        self.assertEqual(q.get_allowed_choice_ids(), [56, 34])
        q.remove_allowed_choice_id(34)
        self.assertEqual(q.get_allowed_choice_ids(), [56])
        q.add_allowed_choice_id(50)
        self.assertEqual(q.get_allowed_choice_ids(), [56, 50])

        # Test removing allowed choice ids with mock Choice objects
        c_mock = Choice(3, "lol")
        c_mock.id = 56
        q.remove_allowed_choice_id(c_mock)
        self.assertEqual(q.get_allowed_choice_ids(), [50])
        q.remove_allowed_choice_id(50)
        self.assertEqual(q.get_allowed_choice_ids(), [])

        # Try remove choice ids with invalid types
        with self.assertRaises(TypeError):
            q.remove_allowed_choice_id(40.6)

        with self.assertRaises(TypeError):
            q.remove_allowed_choice_id("something lel")

        with self.assertRaises(TypeError):
            q.remove_allowed_choice_id(q)

    def test_add_response_id(self):
        q = Question(52, "question text", "question type")
        self.assertEqual(q.get_response_ids(), [])
        # Test adding response id with mock Response object
        r_mock = Response(3, 4)
        r_mock.id = 34
        q.add_response_id(r_mock)
        self.assertEqual(q.get_response_ids(), [34])
        q.add_response_id(34)  # Try add duplicate response_id
        self.assertEqual(q.get_response_ids(), [34])
        q.add_response_id(40)
        self.assertEqual(q.get_response_ids(), [34, 40])
        r_mock.id = 751
        q.add_response_id(r_mock)
        self.assertEqual(q.get_response_ids(), [34, 40, 751])

        q = Question(32, "question text 2", "question type 2", allowed_choice_ids=[1, 2, 3])
        self.assertEqual(q.get_response_ids(), [])
        q.add_response_id(99)
        self.assertEqual(q.get_response_ids(), [99])
        q.add_response_id(29)
        self.assertEqual(q.get_response_ids(), [99, 29])

        # Try add choice ids with invalid types
        with self.assertRaises(TypeError):
            q.add_response_id(40.6)

        with self.assertRaises(TypeError):
            q.add_response_id("something lel")

        with self.assertRaises(TypeError):
            q.add_response_id(q)

    def test_remove_response_id(self):
        q = Question(246, "question text", "question type")
        self.assertEqual(q.get_response_ids(), [])
        q.add_response_id(34)
        self.assertEqual(q.get_response_ids(), [34])
        q.add_response_id(34)  # Try add duplicate response_id
        self.assertEqual(q.get_response_ids(), [34])
        q.add_response_id(40)
        self.assertEqual(q.get_response_ids(), [34, 40])

        # Test removing response id with mock Response object
        r_mock = Response(92, 5, choice_ids=[1, 4])
        r_mock.id = 40
        q.remove_response_id(r_mock)
        self.assertEqual(q.get_response_ids(), [34])
        q.remove_response_id(999)  # Try remove response_id that isn't in list
        r_mock.id = 12345
        q.remove_response_id(r_mock)
        self.assertEqual(q.get_response_ids(), [34])
        q.add_response_id(751)
        self.assertEqual(q.get_response_ids(), [34, 751])
        q.remove_response_id(34)
        self.assertEqual(q.get_response_ids(), [751])
        q.remove_response_id(751)
        self.assertEqual(q.get_response_ids(), [])

        q = Question(321, "question text 2", "question type 2", allowed_choice_ids=[1, 2, 3])
        self.assertEqual(q.get_response_ids(), [])
        q.add_response_id(99)
        self.assertEqual(q.get_response_ids(), [99])
        q.add_response_id(29)
        self.assertEqual(q.get_response_ids(), [99, 29])

        # Try add choice ids with invalid types
        with self.assertRaises(TypeError):
            q.remove_response_id(10.5)

        with self.assertRaises(TypeError):
            q.remove_response_id("something else lol")

        with self.assertRaises(TypeError):
            q.remove_response_id(q)

if __name__ == '__main__':
    unittest.main()
