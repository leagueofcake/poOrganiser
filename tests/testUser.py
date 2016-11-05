import unittest
from User import User


class TestUser(unittest.TestCase):
    def test_get_username(self):
        u1 = User("") # Empty case
        self.assertEqual(u1.get_username(),"")

        u1 = User(" ") # Whitespace case
        self.assertEqual(u1.get_username(), " ")

        u1 = User("Jeremy") # Whitespace case
        self.assertEqual(u1.get_username(), "Jeremy")

    def test_set_username(self):
        u1 = User("test")
        u1.set_username("Dennis")
        self.assertEqual(u1.get_username(), "Dennis")
        u1.set_username(" ")
        self.assertEqual(u1.get_username(), " ")
        u1.set_username("")
        self.assertEqual(u1.get_username(), "")

if __name__ == '__main__':
    unittest.main()
