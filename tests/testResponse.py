import unittest
from Poorganiser import Response, Choice


class TestResponse(unittest.TestCase):
    def test_constructor_assertions(self):
        # Incorrect responder_id type
        with self.assertRaises(AssertionError):
            Response("asdf", 3)

        with self.assertRaises(AssertionError):
            Response(3.14, 1032)

        with self.assertRaises(AssertionError):
            Response([1], 1032, choices=[Choice(1, "blah")])

        # Incorrect question_id type
        with self.assertRaises(AssertionError):
            Response(24, "qwerty")

        with self.assertRaises(AssertionError):
            Response(952, ["in", "va", "li", "d"])

        with self.assertRaises(AssertionError):
            Response(952, 9.876, choices=[Choice(42, "answer")])

        # Invalid choices type
        with self.assertRaises(AssertionError):
            Response(14, 4, choices="lel")

        with self.assertRaises(AssertionError):
            Response(14, 4, choices=1234)

        with self.assertRaises(AssertionError):
            Response(14, 4, choices=[Choice(4, "choice 1"), Choice(4, "choice 2"), "INVALID"])

        with self.assertRaises(AssertionError):
            Response(14, 4, choices=[1, 2, 3, 4])

    def test_get_responder_id(self):
        r = Response(1, 2)
        self.assertEqual(r.get_responder_id(), 1)

        r = Response(32, 9999)
        self.assertEqual(r.get_responder_id(), 32)

        r = Response(56, 64, choices=[Choice(64, "blah")])
        self.assertEqual(r.get_responder_id(), 56)

    def test_get_question_id(self):
        r = Response(1, 2)
        self.assertEqual(r.get_question_id(), 2)

        r = Response(32, 9999)
        self.assertEqual(r.get_question_id(), 9999)

        r = Response(56, 64, choices=[Choice(64, "blah")])
        self.assertEqual(r.get_question_id(), 64)

    def test_get_choices(self):
        r = Response(1, 2)
        self.assertEqual(r.get_choices(), [])

        c1 = Choice(64, "blah")
        c2 = Choice(34, "the choice")
        c3 = Choice(34, "is")
        c4 = Choice(34, "a lie")

        r = Response(56, 64, choices=[c1])
        self.assertEqual(r.get_choices(), [c1])

        r = Response(72, 34, choices=[c2, c3, c4])
        self.assertEqual(r.get_choices(), [c2, c3, c4])

    def test_add_choice(self):
        r = Response(1, 64)
        self.assertEqual(r.get_choices(), [])

        c1 = Choice(64, "blah")
        c2 = Choice(34, "the choice")
        c3 = Choice(34, "is")
        c4 = Choice(34, "a lie")

        r.add_choice(c1)
        self.assertEqual(r.get_choices(), [c1])

        r = Response(290, 34, choices=[c3])
        self.assertEqual(r.get_choices(), [c3])
        r.add_choice(c4)
        self.assertEqual(r.get_choices(), [c3, c4])
        r.add_choice(c2)
        self.assertEqual(r.get_choices(), [c3, c4, c2])

        # Test adding duplicates
        r.add_choice(c2)
        r.add_choice(c2)
        r.add_choice(c3)
        self.assertEqual(r.get_choices(), [c3, c4, c2])

    def test_remove_choice(self):
        r = Response(1, 64)
        self.assertEqual(r.get_choices(), [])

        c1 = Choice(64, "blah")
        c2 = Choice(34, "the choice")
        c3 = Choice(34, "is")
        c4 = Choice(34, "a lie")

        # Add and remove single role
        r.add_choice(c1)
        self.assertEqual(r.get_choices(), [c1])
        r.remove_choice(c1)
        self.assertEqual(r.get_choices(), [])

        # Add and remove multiple roles
        r = Response(42, 34, choices=[c3])
        self.assertEqual(r.get_choices(), [c3])
        r.add_choice(c2)
        self.assertEqual(r.get_choices(), [c3, c2])
        r.remove_choice(c3)
        self.assertEqual(r.get_choices(), [c2])
        r.remove_choice(c2)
        self.assertEqual(r.get_choices(), [])
        r.add_choice(c3)
        self.assertEqual(r.get_choices(), [c3])
        r.add_choice(c4)
        self.assertEqual(r.get_choices(), [c3, c4])
        r.add_choice(c2)
        self.assertEqual(r.get_choices(), [c3, c4, c2])
        r.remove_choice(c3)
        self.assertEqual(r.get_choices(), [c4, c2])
        r.remove_choice(c2)
        self.assertEqual(r.get_choices(), [c4])
        r.remove_choice(c4)
        self.assertEqual(r.get_choices(), [])







if __name__ == '__main__':
    unittest.main()
