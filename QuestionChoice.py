#!/usr/bin/env python3.5
import ast
from sqlalchemy import Column, Integer, Unicode, UnicodeText, String, Date
from create_base import Base

class QuestionChoice(Base):
    __tablename__ = 'choices'
    choice_id = Column(Integer, primary_key=True)
    question_id = Column(Integer)
    choice_text = Column(Unicode(100))
    votes = Column(Unicode(100))

    def __init__(self, question_id, choice_text, votes=[]):
        self.choice_id = None
        self.question_id = question_id
        self.choice_text = choice_text
        self.votes = votes

    def get_id(self):
        return self.choice_id

    def get_question_id(self):
        return self.question_id

    def get_choice_text(self):
        return self.choice_text

    def get_votes(self):
        return self.votes

    def set_choice_text(self, choice_text):
        self.choice_text = choice_text

    def add_vote(self, user):
        self.votes = ast.literal_eval(str(self.votes)) # Convert to list before appending
        if user in self.votes:
            return None
        self.votes.append(user)
        return True

    def remove_vote(self, user):
        self.votes = ast.literal_eval(str(self.votes)) # Convert to list before appending
        if user in self.votes:
            self.votes.remove(user)
        else:
            return None
