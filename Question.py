#!/usr/bin/env python3.5
from sqlalchemy import Column, Integer, Unicode, UnicodeText, String, Date, Boolean
from create_base import Base

class Question(Base):
    __tablename__ = 'questions'
    questionid = Column(Integer, primary_key=True)
    eventid = Column(Integer)
    text = Column(Unicode(100))
    numchoices = Column(Integer)
    preferential = Column(Boolean)
    yettovote = Column(Unicode(100))

    def __init__(self, eventid, text, yettovote, numchoices=1, pref=False):
        self.questionid = None
        self.eventid = eventid
        self.text = text
        self.yettovote = yettovote
        self.numchoices = numchoices
        self.preferential = pref

    def get_questionid(self):
        return self.questionid

    def get_eventid(self):
        return self.eventid

    def set_eventid(self, eventid):
        self.eventid = eventid

    def get_text(self):
        return self.text

    def set_text(self, text):
        self.text = text

# def run_tests():
#     test_get_text()
#     test_set_text()
    #test_add_option()
    #test_get_options()


# def test_get_text():
#     q1 = Question("") # Empty case
#     assert(q1.get_text() == "")
#
#     q1 = Question(" ") # Whitespace case
#     assert(q1.get_text() == " ")
#
#     q1 = Question("Do you lickadickaday?") # normal case
#     assert(q1.get_text() == "Do you lickadickaday?")
#
#
# def test_set_text():
#     q1 = Question("test")
#     q1.set_text("Do you lickadickaday?")
#     assert(q1.get_text() == "Do you lickadickaday?")
#     q1.set_text(" ")
#     assert(q1.get_text() == " ")
#     q1.set_text("")
#     assert(q1.get_text() == "")

#def test_add_option():
#    q1 = Question("test")
#    assert(q1.get_options() == {})
#    q1.add_option("Yes")
#    assert(q1.get_options()["Yes"] == 0)
#    q1.add_option("No")
#    assert(q1.get_options()["No"] == 0)

#def test_get_options():
#    q1 = Question("")
#    assert(q1.get_options() == {})
#
#    q1 = Question("test")
#    assert(q1.get_options() == {})


#run_tests()

# q = Question("Please answer", ["Dom", "Dennis", "Jeremy"], 1, False)
# q.add_option("A")
# q.add_option("B")
# q.add_option("C")
# q.make_vote("Dom", "C")
# q.has_voted("Dom")
# q.make_vote("Jeremy", "B")
# q.has_voted("Jeremy")
# q.make_vote("Dennis", "B")
# q.has_voted("Dennis")
