import unittest
from QuestionChoice import QuestionChoice

class TestQuestionChoice(unittest.TestCase):
    def test_get_id(self):
        qc1 = QuestionChoice(1, "Choice 1")
        self.assertEqual(qc1.get_id(), None)

        qc2 = QuestionChoice(2, "Choice 2", ['lol', 'blah'])
        self.assertEqual(qc2.get_id(), None)

    def test_get_questionid(self):
        qc1 = QuestionChoice(1, "Choice 1")
        self.assertEqual(qc1.get_questionid(), 1)

        qc2 = QuestionChoice(2, "Choice 2", ['lol', 'blah'])
        self.assertEqual(qc2.get_questionid(), 2)

    def test_get_choicetext(self):
        qc1 = QuestionChoice(1, "Choice 1")
        self.assertEqual(qc1.get_choicetext(), "Choice 1")

        qc2 = QuestionChoice(2, "Choice 2", ['lol', 'blah'])
        self.assertEqual(qc2.get_choicetext(), "Choice 2")

    def test_get_votes(self):
        qc1 = QuestionChoice(1, "LOL", [])
        self.assertEqual(qc1.get_votes(), [])

        qc2 = QuestionChoice(2, "Choice 2", ['lol', 'blah'])
        self.assertEqual(qc2.get_votes(), ['lol', 'blah'])

    def test_set_choicetext(self):
        qc1 = QuestionChoice(1, "Choice 1")
        self.assertEqual(qc1.get_choicetext(), "Choice 1")
        qc1.set_choicetext("Choice 11")
        self.assertEqual(qc1.get_choicetext(), "Choice 11")

        qc2 = QuestionChoice(2, "Choice 2", ['lol', 'blah'])
        self.assertEqual(qc2.get_choicetext(), "Choice 2")
        qc2.set_choicetext("hello there")
        self.assertEqual(qc2.get_choicetext(), "hello there")
        qc2.set_choicetext("some choice")
        self.assertEqual(qc2.get_choicetext(), "some choice")

    def test_add_vote(self):
        qc1 = QuestionChoice(1, "Choice 1")
        qc1.add_vote('user 1')
        self.assertEqual(qc1.get_votes(), ['user 1'])

        qc2 = QuestionChoice(2, "Choices are real", ['haha', 'lmao'])
        qc2.add_vote('top')
        qc2.add_vote('kek')
        self.assertEqual(qc2.get_votes(), ['haha', 'lmao', 'top', 'kek'])

    def test_remove_vote(self):
        qc1 = QuestionChoice(1, "Choice 1")
        qc1.add_vote('user 1')
        qc1.remove_vote('user 1')
        self.assertEqual(qc1.get_votes(), [])

        qc2 = QuestionChoice(2, "Choices are real", ['haha', 'lmao'])
        qc2.add_vote('top')
        qc2.add_vote('kek')
        qc2.remove_vote('top')
        self.assertEqual(qc2.get_votes(), ['haha', 'lmao', 'kek'])
        qc2.remove_vote('haha')
        self.assertEqual(qc2.get_votes(), ['lmao', 'kek'])
        qc2.remove_vote('aweofiwahef')
        self.assertEqual(qc2.get_votes(), ['lmao', 'kek'])
        qc2.remove_vote(None)
        self.assertEqual(qc2.get_votes(), ['lmao', 'kek'])

if __name__ == '__main__':
    unittest.main()
