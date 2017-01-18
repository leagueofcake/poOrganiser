import unittest
from Poorganiser import Response


class TestResponse(unittest.TestCase):
    def test_constructor_assertions(self):
        # Incorrect responder_id type
        with self.assertRaises(AssertionError):
            Response("asdf", 3)

        with self.assertRaises(AssertionError):
            Response(3.14, 1032)

        with self.assertRaises(AssertionError):
            Response([1], 1032, choice_ids=[3, 4])

        # Incorrect question_id type
        with self.assertRaises(AssertionError):
            Response(24, "qwerty")

        with self.assertRaises(AssertionError):
            Response(952, ["in", "va", "li", "d"])

        with self.assertRaises(AssertionError):
            Response(952, 9.876, choice_ids=[42, 24, 56])

        # Invalid choice_ids type
        with self.assertRaises(AssertionError):
            Response(14, 4, choice_ids="lel")

        with self.assertRaises(AssertionError):
            Response(14, 4, choice_ids=1234)

        with self.assertRaises(AssertionError):
            Response(14, 4, choice_ids=[1, 3, 4, "INVALID"])

        with self.assertRaises(AssertionError):
            Response(14, 4, choice_ids=[1.3, 2, 3, 4])

    def test_get_responder_id(self):
        r = Response(1, 2)
        self.assertEqual(r.get_responder_id(), 1)

        r = Response(32, 9999)
        self.assertEqual(r.get_responder_id(), 32)

        r = Response(56, 64, choice_ids=[64, 34])
        self.assertEqual(r.get_responder_id(), 56)

    def test_get_question_id(self):
        r = Response(1, 2)
        self.assertEqual(r.get_question_id(), 2)

        r = Response(32, 9999)
        self.assertEqual(r.get_question_id(), 9999)

        r = Response(56, 64, choice_ids=[64, 34, 103])
        self.assertEqual(r.get_question_id(), 64)

    def test_get_choice_ids(self):
        r = Response(1, 2)
        self.assertEqual(r.get_choice_ids(), [])

        r = Response(56, 64, choice_ids=[14])
        self.assertEqual(r.get_choice_ids(), [14])

        r = Response(72, 34, choice_ids=[245, 10, 201])
        self.assertEqual(r.get_choice_ids(), [245, 10, 201])

    def test_add_choice_id(self):
        r = Response(1, 64)
        self.assertEqual(r.get_choice_ids(), [])

        r.add_choice_id(14)
        self.assertEqual(r.get_choice_ids(), [14])

        r = Response(290, 34, choice_ids=[10])
        self.assertEqual(r.get_choice_ids(), [10])
        r.add_choice_id(201)
        self.assertEqual(r.get_choice_ids(), [10, 201])
        r.add_choice_id(245)
        self.assertEqual(r.get_choice_ids(), [10, 201, 245])

        # Test adding duplicates
        r.add_choice_id(245)
        r.add_choice_id(245)
        r.add_choice_id(10)
        self.assertEqual(r.get_choice_ids(), [10, 201, 245])

    def test_remove_choice_id(self):
        r = Response(1, 64)
        self.assertEqual(r.get_choice_ids(), [])

        # Add and remove single role
        r.add_choice_id(14)
        self.assertEqual(r.get_choice_ids(), [14])
        r.remove_choice_id(14)
        self.assertEqual(r.get_choice_ids(), [])

        # Add and remove multiple roles
        r = Response(42, 34, choice_ids=[10])
        self.assertEqual(r.get_choice_ids(), [10])
        r.add_choice_id(245)
        self.assertEqual(r.get_choice_ids(), [10, 245])
        r.remove_choice_id(10)
        self.assertEqual(r.get_choice_ids(), [245])
        r.remove_choice_id(245)
        self.assertEqual(r.get_choice_ids(), [])
        r.add_choice_id(10)
        self.assertEqual(r.get_choice_ids(), [10])
        r.add_choice_id(201)
        self.assertEqual(r.get_choice_ids(), [10, 201])
        r.add_choice_id(245)
        self.assertEqual(r.get_choice_ids(), [10, 201, 245])
        r.remove_choice_id(10)
        self.assertEqual(r.get_choice_ids(), [201, 245])
        r.remove_choice_id(245)
        self.assertEqual(r.get_choice_ids(), [201])
        r.remove_choice_id(201)
        self.assertEqual(r.get_choice_ids(), [])

if __name__ == '__main__':
    unittest.main()
