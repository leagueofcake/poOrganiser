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