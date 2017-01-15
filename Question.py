#!/usr/bin/env python3.5
from sqlalchemy import Column, Integer, Unicode, UnicodeText, String, Date, Boolean
from create_base import Base


class Question(Base):
    __tablename__ = 'questions'
    question_id = Column(Integer, primary_key=True)
    event_id = Column(Integer)
    text = Column(Unicode(100))
    num_choices = Column(Integer)
    preferential = Column(Boolean)
    yet_to_vote = Column(Unicode(100))

    def __init__(self, event_id, text, yet_to_vote, num_choices=1, pref=False):
        self.question_id = None
        self.event_id = event_id
        self.text = text
        self.yet_to_vote = yet_to_vote
        self.num_choices = num_choices
        self.preferential = pref

    def get_question_id(self):
        return self.question_id

    def get_event_id(self):
        return self.event_id

    def set_event_id(self, event_id):
        self.event_id = event_id

    def get_text(self):
        return self.text

    def set_text(self, text):
        self.text = text
