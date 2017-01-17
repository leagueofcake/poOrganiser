import unittest
from Poorganiser import Choice


class TestChoice(unittest.TestCase):
    def test_constructor_assertions(self):
        # Incorrect question_id type
        with self.assertRaises(AssertionError):
            Choice("asdf", "qwerty")

        with self.assertRaises(AssertionError):
            Choice(3.14, "some choice")

        # Incorrect choice type
        with self.assertRaises(AssertionError):
            Choice(3, ["lol", "k"])

        with self.assertRaises(AssertionError):
            Choice(3, Choice(101, "blah"))

    def test_get_question_id(self):
        c = Choice(1, "choice text")
        self.assertEqual(c.get_question_id(), 1)

        c = Choice(312, "choice 2")
        self.assertEqual(c.get_question_id(), 312)

        c = Choice(12345, "choice 3")
        self.assertEqual(c.get_question_id(), 12345)

    def test_get_choice(self):
        c = Choice(1, "choice text")
        self.assertEqual(c.get_choice(), "choice text")

        c = Choice(312, "THE seCOND chOICE")
        self.assertEqual(c.get_choice(), "THE seCOND chOICE")

        c = Choice(12345, "choice 3333")
        self.assertEqual(c.get_choice(), "choice 3333")

    def set_question_id(self):
        c = Choice(1, "choice text")
        self.assertEqual(c.get_question_id(), 1)
        c.set_question_id(32)
        self.assertEqual(c.get_question_id(), 32)
        c.set_question_id(999)
        self.assertEqual(c.get_question_id(), 999)
        c.set_question_id(24)
        c.set_question_id(42)
        self.assertEqual(c.get_question_id(), 42)

    def set_choice(self):
        c = Choice(1, "choice text")
        self.assertEqual(c.get_choice(), "choice text")
        c.set_choice("new choice text!")
        self.assertEqual(c.get_choice(), "new choice text!")
        c.set_choice("even_newer_choice_text")
        self.assertEqual(c.get_choice(), "even_newer_choice_text")
        c.set_choice("ignored choice text")
        c.set_choice("ignored choice text v2")
        c.set_choice("NeWeSt_ChOiCe_TeXt")
        self.assertEqual(c.get_choice(), "NeWeSt_ChOiCe_TeXt")

if __name__ == '__main__':
    unittest.main()
